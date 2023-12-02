import json
import os


class Settings:
    def __init__(self):
        self.values = {"database": "", "urls": []}

    def read_and_populate(self, path):
        ret = self.read(path)
        if ret[0] is True:
            self.populate_values(ret[1])

    def populate_values(self, dict):
        # TODO validate that we have the expected variables
        # and that the values contained appear to be proper.
        self.values = dict

    def read(self, full_path):
        """Read JSON settings from the specified file path"""
        read_success = True
        fail_message = ""
        file_content = ""
        json_settings = ""

        # Are we going to have trouble?
        full_path_exists = os.path.exists(full_path)
        full_path_is_accessible = os.access(full_path, os.R_OK)

        if not full_path_exists or not full_path_is_accessible:
            read_success = False
            fail_message = f'File does not exist or is not accessible. "{full_path}"'

        # Perform the IO if haven't failed yet
        if read_success:
            try:
                with open(full_path, "rt") as f:
                    file_content = f.read()
            except Exception as ex:
                read_success = False
                if hasattr(ex, "message"):
                    fail_message = str(ex.message)
                else:
                    fail_message = f'An exception occurred while attempting to read the file. "{full_path}"'

        # File content expected to be JSON
        if read_success:
            try:
                json_settings = json.loads(file_content)
            except Exception as ex:
                read_success = False
                if hasattr(ex, "message"):
                    fail_message = str(ex.message)
                else:
                    fail_message = f'Failed to load JSON from file content. "{str(ex)}"'

        if not read_success:
            return (read_success, fail_message)
        else:
            return (read_success, json_settings)

    def persist(self, full_path):
        try:
            with open(full_path, "w") as f:
                json.dump(self.values, f)
        except Exception as ex:
            fail_message = (
                f'An exception occurred when opening or writing to "{full_path}"'
            )
            # If we have a better fail message available to us, use it.
            if hasattr(ex, "message"):
                fail_message = str(ex.message + f'\n"{full_path}"')

            return (False, fail_message)

        return (True, full_path)
