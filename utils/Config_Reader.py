import configparser


def read_config(file: str):
    config = configparser.ConfigParser(allow_unnamed_section=True)
    config.read(file)
    api_key = config.get(configparser.UNNAMED_SECTION, 'CARTO_KEY')
    use_cache = config.getboolean(configparser.UNNAMED_SECTION, 'USE_CACHE')
    sqlite_path = config.get(configparser.UNNAMED_SECTION, 'SQLITE_PATH')
    map_path = config.get(configparser.UNNAMED_SECTION, 'MAP_PATH')
    config_values = {
            'CARTO_KEY': api_key,
            'USE_CACHE': use_cache,
            'SQLITE_PATH': sqlite_path,
            'MAP_PATH': map_path
    }
    return config_values
