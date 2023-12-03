import os
from settings import *
from prepare_database import *
from wunderground import *
from weather import *
from dotenv import load_dotenv
from json import JSONDecodeError


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

    weathers = []
    # for url in config.urls:
    #    weathers.append(scrape(url))

    # write_to_database(config.database, weathers)
