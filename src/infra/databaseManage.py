from sqlalchemy import text
import logging
from typing import Any

logger = logging.getLogger(__name__)


class databaseManage:
    def __init__(self, engine):
        self.engine = engine

    def _sanitize_value(self, v: Any) -> Any:

        if isinstance(v, (bytes, bytearray)):
            b = bytes(v)
            try:
                return b.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return b.decode('latin-1')
                except Exception:
                    return b.decode('utf-8', errors='replace')
        return v

    def insert_data(self, table_name, data : list[dict]):
        if not data:
            return

        try:
            columns = list(data[0].keys())
            cols = ", ".join(columns)
            vals = ", ".join(f":{c}" for c in columns)

            query = text(f"""
                INSERT INTO {table_name}
                ({cols})
                VALUES ({vals})
            """)

            sanitized_rows: list[dict] = []
            for i, row in enumerate(data):
                new_row = {}
                for k, v in row.items():
                    try:
                        new_row[k] = self._sanitize_value(v)
                    except Exception as e:
                        logger.exception("Failed to sanitize row %s column %s", i, k)
                        raise
                sanitized_rows.append(new_row)

            try:
                with self.engine.begin() as conn:
                    conn.execute(query, sanitized_rows)
            except UnicodeDecodeError as ude:
                logger.exception("Bulk insert raised UnicodeDecodeError, falling back to per-row inserts to identify bad row")
                with self.engine.begin() as conn:
                    for idx, single in enumerate(sanitized_rows):
                        try:
                            conn.execute(query, single)
                        except UnicodeDecodeError:
                            logger.exception("UnicodeDecodeError inserting row %s: %r", idx, single)
                            raise Exception(f"Error inserting data (UnicodeDecodeError) at row {idx}: {single}") from ude
                        except Exception as e:
                            logger.exception("Error inserting row %s: %s", idx, e)

                raise

        except UnicodeDecodeError as ude:
            logger.exception("Unicode decode error while inserting into %s", table_name)
            raise Exception(f"Error inserting data (UnicodeDecodeError): {ude}")
        except Exception as e:
            logger.exception("Error inserting data into %s", table_name)
            raise Exception(f"Error inserting data: {e}")