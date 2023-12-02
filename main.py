import os
from settings import *
from prepare_database import *
from wunderground import *
from weather import *


def get_settings_or_die(config: Settings):
    status = config.read("settings.json")
    if status[0] is False:
        print(f"FATAL: Unable to read settings.\n{str(status[1])}")
        os._exit(1)
    else:
        config.populate_values(status[1])


if __name__ == "__main__":
    config = Settings()
    get_settings_or_die(config)

    # check for database accessibility or die
    print(f"Checking for database at \"{config.values['database']}\"")
    status = check_for_db(config.values["database"])
    if status[0] == False:
        print(
            f"FATAL: Unable to access database or file does not exist.\n{str(status[1])}"
        )
        os._exit(1)

    weathers = []
    for url in config.values["urls"]:
        weathers.append(scrape(url))

    write_to_database(config.values["database"], weathers)
