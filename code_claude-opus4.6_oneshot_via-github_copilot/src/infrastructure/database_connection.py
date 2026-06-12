import psycopg2
import os


class DatabaseConnection:
    """SQL-Verbindung - Verwaltet die Datenbankverbindung"""

    def __init__(self, host: str = None, port: int = None, database: str = None,
                 user: str = None, password: str = None):
        self.host = host or os.environ.get("DATABASE_HOST", "localhost")
        self.port = port or int(os.environ.get("DATABASE_PORT", "5432"))
        self.database = database or os.environ.get("DATABASE_NAME", "smarthome")
        self.user = user or os.environ.get("DATABASE_USER", "smarthome")
        self.password = password or os.environ.get("DATABASE_PASSWORD", "smarthome")
        self._connection = None

    def get_connection(self):
        if self._connection is None or self._connection.closed:
            self._connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            self._connection.autocommit = True
        return self._connection

    def close(self):
        if self._connection and not self._connection.closed:
            self._connection.close()
