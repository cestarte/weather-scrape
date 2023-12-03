import json


class Settings:
    def __init__(self):
        self.database = ""
        self.urls = []

    @staticmethod
    def read(full_path):
        """Read JSON settings from the specified file path"""
        with open(full_path, "rt") as f:
            file_content = f.read()

        json_settings = json.loads(file_content)

        s = Settings()
        s.database = json_settings["database"]
        s.urls = json_settings["urls"]
        return s
