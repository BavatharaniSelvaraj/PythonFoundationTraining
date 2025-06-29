import configparser

class DBPropertyUtil:
    @staticmethod
    def getPropertyString(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)
        props = config['DEFAULT']
        return {
            'host': props['host'],
            'port': props['port'],
            'database': props['database'],
            'username': props['username'],
            'password': props['password']
        }
