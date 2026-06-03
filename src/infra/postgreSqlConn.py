from sqlalchemy import create_engine
from sqlalchemy.engine import URL

class PostgreSqlConn:

    _engine = None

    def __init__(self, user, password, host, port, database):

        if PostgreSqlConn._engine is None:

            url = URL.create(
                drivername="postgresql+psycopg",
                username=user,
                password=password,
                host=host,
                port=int(port),
                database=database
            )

            PostgreSqlConn._engine = create_engine(
                url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True
            )

    def get_engine(self):
        return PostgreSqlConn._engine