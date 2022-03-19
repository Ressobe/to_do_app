import mysql.connector as mysql


class ConnectionError(Exception):
    pass


class CredentialsError(Exception):
    pass


class SqlError(Exception):
    pass


class UseDatabase:
    def __init__(self, conf: dict) -> None:
        self.configuration = conf

    def __enter__(self):
        try:
            self.conn = mysql.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.errors.ProgrammingError as err:
            raise CredentialsError(err)

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.errors.ProgrammingError:
            raise SqlError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)
