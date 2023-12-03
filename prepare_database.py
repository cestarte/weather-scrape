import sqlite3
import os
import argparse
from settings import *


def check_for_db(full_path: str):
    success = True
    message = ""
    full_path_exists = os.path.exists(full_path)
    full_path_is_accessible = os.access(full_path, os.W_OK)

    if not full_path_exists or not full_path_is_accessible:
        success = False
        message = f'File does not exist or is not accessible. "{full_path}"'
        return (success, message)

    return (success, message)


def drop_tables(database_path):
    weather_query = """
    DROP TABLE IF EXISTS "Weather"
    """

    log_query = """
    DROP TABLE IF EXISTS "Log"
    """

    drop_queries = [
        ("Weather", weather_query),
        ("Log", log_query),
    ]

    print("Dropping tables...")
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        for query in drop_queries:
            print("\t" + query[0])
            cur.execute(query[1])
            con.commit()
    except sqlite3.Error as error:
        print("ERROR while dropping tables from sqlite", error)
    finally:
        if con:
            con.close()
    print("...done.")


def create_tables(database_path):
    weather_query = """
CREATE TABLE IF NOT EXISTS "Weather" (
  "Id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  "HighTemp" integer NULL,
  "LowTemp" integer NULL,
  "CurrentTemp" integer NULL,
  "DegreeUnit" varchar(15) NULL,
  "Condition" varchar(256) NULL,
  "Humidity" integer NULL,
  "DewPoint" integer NULL,
  "Elevation" integer NULL,
  "ElevationUnit" varchar(15) NULL,
  "North" decimal NULL,
  "South" decimal NULL,
  "East" decimal NULL,
  "West" decimal NULL,
  "Lat" decimal NULL,
  "Lon" decimal NULL,
  "HrapX" decimal NULL,
  "HrapY" decimal NULL,
  "Location" varchar(256) NULL,
  "Station" varchar(256) NULL,
  "Url" varchar(256) NOT NULL,
  "WhenCollected" timestamp NOT NULL,
  "LastModified" timestamp NOT NULL,
  "WhoModified" varchar(128) NOT NULL
);
    """

    log_query = """
    CREATE TABLE IF NOT EXISTS "Log" (
      "Id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
      "Message" varchar(256),
      "Data" varchar(128),
      "WeatherId" integer NULL,
      "LastModified" timestamp NOT NULL,
      "WhoModified" varchar(128) NOT NULL
    );
    """

    create_queries = [
        ("Weather", weather_query),
        ("Log", log_query),
    ]

    print("Creating tables...")
    try:
        con = sqlite3.connect(database_path)
        cur = con.cursor()
        for query in create_queries:
            print("\t" + query[0])
            cur.execute(query[1])
            con.commit()
    except sqlite3.Error as error:
        print("ERROR while creating sqlite tables.", error)
    finally:
        if con:
            con.close()
    print("...done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare the database schema.")
    parser.add_argument(
        "-d",
        "--drop",
        action="store_true",
        help="If specified, will drop tables before creating. You will lose all existing data.",
    )

    # read settings file to get full path to database
    settings_path = os.environ.get("SETTINGS_PATH", "settings.json")
    config = Settings.read(settings_path)
    print(f"Database: {config.database}")

    # parse the args
    args = parser.parse_args()
    # print(args)
    if args.drop:
        drop_tables(config.database)

    create_tables(config.database)
