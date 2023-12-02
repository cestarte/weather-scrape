from datetime import datetime
import sqlite3


class Log:
    def __init__(self):
        self.id = None
        self.message = ""
        self.data = ""
        self.weather_id = None
        self.last_modified = datetime.now()
        self.who_modified = "APP"

    def print(self):
        print(f"Id = {self.id}")
        print(f"Message = {self.message}")
        print(f"Data = {self.data}")
        print(f"WeatherId = {self.weather_id}")
        print(f"LastModified = {self.last_modified}")
        print(f"WhoModified = {self.who_modified}")


def write_to_database(database_path, logs):
    print("Inserting logs to database...")
    try:
        con = sqlite3.connect(
            database_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        cur = con.cursor()

        for log in logs:
            data = (
                log.id,
                log.message,
                log.data,
                log.weather_id,
                log.last_modified,
                log.who_modified,
            )
            cur.execute(
                "INSERT INTO Log (Id, Message, Data, WeatherId, LastModified, WhoModified) VALUES(?, ?, ?, ?, ?, ?)",
                data,
            )
        con.commit()
    except sqlite3.Error as error:
        print("Error while inserting logs into sqlite.", error)
    finally:
        if con:
            con.close()
