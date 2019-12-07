import configparser

class Settings():
    
    def __init__(self, file):
        self._settingsfile = file
        self._config = configparser.RawConfigParser()
        self._config.read(file)
    
    def get_sections(self):
        return self._config.sections()
    
    def get_format(self):
        return self._config.get("FORMAT", "format")
    
    def get_txt(self):
        return [self._config.get("TEXTFILES", "books"), self._config.get("TEXTFILES", "clients"), self._config.get("TEXTFILES", "rentals")]
    
    def get_bynary(self):
        return [self._config.get("BYNARYFILES", "books"), self._config.get("BYNARYFILES", "clients"), self._config.get("BYNARYFILES", "rentals")]
    
    def get_json(self):
        return [self._config.get("JSONFILES", "books"), self._config.get("JSONFILES", "clients"), self._config.get("JSONFILES", "rentals")]
    
    def get_sql(self):
        return [self._config.get("SQLDATABASE", "books"), self._config.get("SQLDATABASE", "clients"), self._config.get("SQLDATABASE", "rentals")]
    