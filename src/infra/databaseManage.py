from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import logging
from typing import Any

logger = logging.getLogger(__name__)


class DatabaseManage:
    def __init__(self, engine, user, password, host, port):
        self.engine = engine

        # credenciais só pra bootstrap interno (não expõe engine extra)
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def _sanitize_value(self, v: Any) -> Any:
        if isinstance(v, (bytes, bytearray)):
            b = bytes(v)
            try:
                return b.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    return b.decode("latin-1")
                except Exception:
                    return b.decode("utf-8", errors="replace")
        return v

    def _ensure_database_exists(self, database_name: str):

        admin_url = URL.create(
            drivername="postgresql+psycopg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
            database="postgres"  # obrigatório
        )

        admin_engine = create_engine(admin_url)

        check_sql = text("SELECT 1 FROM pg_database WHERE datname = :db")

        with admin_engine.connect() as conn:
            exists = conn.execute(check_sql, {"db": database_name}).scalar()

        if not exists:
            with admin_engine.execution_options(
                isolation_level="AUTOCOMMIT"
            ).connect() as conn:
                conn.execute(text(f"CREATE DATABASE {database_name}"))

        admin_engine.dispose()

    def insert_data(self, table_name: str, data: list[dict], database_name: str = None):

        if database_name:
            self._ensure_database_exists(database_name)

        if not data:
            return

        columns = list(data[0].keys())
        cols = ", ".join(columns)
        vals = ", ".join(f":{c}" for c in columns)

        query = text(f"""
            INSERT INTO {table_name}
            ({cols})
            VALUES ({vals})
        """)

        sanitized_rows = []

        for i, row in enumerate(data):
            new_row = {}

            for k, v in row.items():
                new_row[k] = self._sanitize_value(v)

            sanitized_rows.append(new_row)

        try:
            with self.engine.begin() as conn:
                conn.execute(query, sanitized_rows)

        except Exception:
            print("Erro no bulk insert. Tentando linha a linha.")

            with self.engine.begin() as conn:
                for idx, single in enumerate(sanitized_rows):
                    try:
                        conn.execute(query, single)
                    except Exception as row_error:
                        print(f"Erro na linha {idx}")
                        print(single)
                        raise Exception(f"Erro na linha {idx}: {row_error}") from row_error