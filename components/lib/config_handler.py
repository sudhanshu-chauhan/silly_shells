from configparser import ConfigParser

from conf import settings


class DBConfiguration:
    def __init__(self):
        self.config_file_path = settings.CONFIG_FILE_PATH
        self.config_parser = ConfigParser()
        self.config_parser.read(self.config_file_path)

    def get_db_configuration(self, section, data=None):
        config_dict = dict()
        if data is not None:
            for key in data:
                config_dict[key] = self.config_parser.get(section,
                                                          key)
            return config_dict
        else:
            return dict(self.config_parser.items(section))

    def set_db_configuration(self, section, data):
        if data is not None:
            for key, value in data.items():
                self.config_parser.set(section, key, value)
            with open(self.config_file_path, "wb") as config_file_handle:
                self.config_parser.write(config_file_handle)
