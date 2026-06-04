from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import logging
from typing import Any

logger = logging.getLogger(__name__)


class DatabaseManage:
    def __init__(self, user, password, host, port, database_name):
        # credenciais só pra bootstrap interno (não expõe engine extra)
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self._ensure_database_exists(database_name)

        db_url = URL.create(
            drivername="postgresql+psycopg",
            username=user,
            password=password,
            host=host,
            port=int(port),
            database=database_name
        )

        self.engine = create_engine(db_url)

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
            database='postgres'  
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

    def create_table(self, table_name: str):

        sql_create_table = text(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                log_id VARCHAR(20) PRIMARY KEY,
                farm_id VARCHAR(20) NOT NULL,
                farm_region VARCHAR(100),
                sensor_id VARCHAR(20) NOT NULL,
                device_type VARCHAR(50),
                failure_category VARCHAR(100),
                failure_timestamp TIMESTAMP,
                downtime_hours FLOAT,
                resolution_action VARCHAR(150),
                temperature_celsius FLOAT,
                humidity_percent FLOAT,
                weather_condition VARCHAR(50),
                soil_moisture_percent FLOAT,
                maintenance_team VARCHAR(100),
                resolved BOOLEAN,
                estimated_loss_usd DECIMAL(10, 2)
            );
        """)

        with self.engine.begin() as conn:
            try:
                conn.execute(sql_create_table)
            except Exception as e:
                return f"Erro ao criar tabela: {e}"

        return

    def insert_data(self, table_name: str, data: list[dict]):

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