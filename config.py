import configparser

class GenshinConfig:
    key = 'GENSHIN'
    def __init__(self, path):
        self.path = path
        self.config_object = configparser.ConfigParser()
        self.config_object.read(self.path)
        self._config = self.config_object[self.key]

        self.user_id = self.get_property('user_id')
        self.lang = self.get_property('lang')

    def get_property(self, property_name):
        if (property_name not in self._config.keys()) or (self._config[property_name] == ''):
            prop = input('%s = '%(property_name))
            self._config[property_name] = prop
            with open(self.path, 'w') as configfile:
                self.config_object.write(configfile)
            return prop
        return self._config[property_name]


class GoogleConfig:
    key = 'GOOGLE_SHEETS'
    def __init__(self, path):
        self.path = path
        self.config_object = configparser.ConfigParser()
        self.config_object.read(self.path)
        self._config = self.config_object[self.key]

        self.spreadsheet_id = self.get_property('spreadsheet_id')

    def get_property(self, property_name):
        if (property_name not in self._config.keys()) or (self._config[property_name] == ''):
            prop = input('%s = '%(property_name))
            self._config[property_name] = prop
            with open(self.path, 'w') as configfile:
                self.config_object.write(configfile)
            return prop
        return self._config[property_name]