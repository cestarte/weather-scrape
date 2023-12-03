import os
from settings import *
from prepare_database import *
from wunderground import *
from weather import *
from dotenv import load_dotenv
from json import JSONDecodeError
from datetime import datetime


def read_settings(full_path):
    if os.path.exists(full_path) == False:
        print(f'FATAL: Settings file does not exist at path "{full_path}"')
        os._exit(1)
    if os.access(full_path, os.R_OK) == False:
        print(f'FATAL: Settings file is not accessible at path "{full_path}"')
        os._exit(1)

    try:
        return Settings.read(full_path)
    except JSONDecodeError as ex:
        print("FATAL: Settings JSON failed to decode.")
        if hasattr(ex, "message"):
            print(str(ex.message))
        os._exit(1)
    except Exception as ex:
        print(f'FATAL: Settings could not be read at path "{full_path}".')
        print(ex)
        os._exit(1)


def find_unused_urls(database_path, urls):
    filtered_urls = []
    today = datetime.today()
    for url in urls:
        if Weather.already_exists(database_path, url, today) == False:
            filtered_urls.append(url)
    return filtered_urls


if __name__ == "__main__":
    load_dotenv()
    config = read_settings(os.environ["SETTINGS_PATH"])

    # check for database accessibility or die
    print(f'Checking for database at "{config.database}"')
    status = check_for_db(config.database)
    if status[0] == False:
        print(
            f"FATAL: Unable to access database or file does not exist.\n{str(status[1])}"
        )
        os._exit(1)

    # Rule: don't spam requests. Limit each URL to 1x/day
    filtered_urls = find_unused_urls(config.database, config.urls)
    if len(config.urls) != len(filtered_urls):
        print(
            f"NOTICE: There are already results for today. To prevent spamming, we're only going to run the {len(filtered_urls)} URLs which haven't already been collected today."
        )
    print(filtered_urls)

    # if we have anything to collect, do it.
    if len(filtered_urls) > 0:
        weathers = []
        for url in filtered_urls:
            try:
                weathers.append(scrape(url))
            except Exception as ex:
                print(f"WARNING: Failed to scrape URL {url}")
                print(ex)

        Weather.persist(config.database, weathers)
