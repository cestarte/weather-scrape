from datetime import datetime
import sqlite3


class Weather:
    def __init__(self):
        self.id = None
        self.high_temp = None
        self.low_temp = None
        self.current_temp = None
        self.degree_unit = None
        self.condition = None
        self.elevation = None
        self.elevation_unit = None
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.lat = None
        self.lon = None
        self.hrap_x = None
        self.hrap_y = None
        self.location = ""
        self.station = ""
        self.url = ""
        self.when_collected = datetime.now()
        self.last_modified = datetime.now()
        self.who_modified = "APP"

    def print(self):
        print(f"Id = {self.id}")
        print(f"High = {self.high_temp}")
        print(f"Low = {self.low_temp}")
        print(f"Current = {self.current_temp}")
        print(f"Degree Unit = {self.degree_unit}")
        print(f"Condition = {self.condition}")
        print(f"Elevation = {self.elevation}")
        print(f"Elevation Unit = {self.elevation_unit}")
        print(f"North = {self.north}")
        print(f"South = {self.south}")
        print(f"East = {self.east}")
        print(f"West = {self.west}")
        print(f"Lat = {self.lat}")
        print(f"Lon = {self.lon}")
        print(f"HRAP X = {self.hrap_x}")
        print(f"HRAP Y = {self.hrap_y}")
        print(f"Location = {self.location}")
        print(f"Station = {self.station}")
        print(f"URL = {self.url}")
        print(f"WhenCollected = {self.when_collected}")
        print(f"LastModified = {self.last_modified}")
        print(f"WhoModified = {self.who_modified}")


def write_to_database(database_path, weathers):
    print("Inserting weathers to database...")
    try:
        con = sqlite3.connect(
            database_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        cur = con.cursor()

        for weather in weathers:
            data = (
                weather.id,
                weather.high_temp,
                weather.low_temp,
                weather.current_temp,
                weather.degree_unit,
                weather.condition,
                weather.elevation,
                weather.elevation_unit,
                weather.north,
                weather.south,
                weather.east,
                weather.west,
                weather.lat,
                weather.lon,
                weather.hrap_x,
                weather.hrap_y,
                weather.location,
                weather.station,
                weather.url,
                weather.when_collected,
                weather.last_modified,
                weather.who_modified,
            )
            cur.execute(
                """
    INSERT INTO Weather (Id, HighTemp, LowTemp, CurrentTemp, DegreeUnit, 
    Condition, Elevation, ElevationUnit, North, South, East, West, Lat, Lon,
    HrapX, HrapY, Location, Station, Url, WhenCollected, LastModified, WhoModified) 
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                data,
            )
        con.commit()
    except sqlite3.Error as error:
        print("Error while inserting weathers into sqlite.", error)
    finally:
        if con:
            con.close()
