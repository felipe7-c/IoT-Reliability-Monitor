from sqlalchemy import create_engine
from sqlalchemy.engine import URL

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Felps@2661",
    host="localhost",
    port=5433,
    database="iot_reliability_monitor"
)

print(url)

engine = create_engine(url)

with engine.connect() as conn:
    print("OK")