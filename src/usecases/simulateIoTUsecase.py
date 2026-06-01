import pandas as pd
import requests
import numpy as np

from src.models.models import IoTData

class SimulateIoTUsecase:

    def __init__(self, db_queue):

        self.session = requests.Session()
        self.db_queue = db_queue

    def load_excel(self, path):

        df = pd.read_excel(path)

        df = self._preprocess_data(df)

        return df.to_dict(orient="records")


    def _preprocess_data(self, df):

        df.columns = df.columns.str.strip()

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.strip()

        df = df.replace({np.nan: None})

        bool_cols = df.select_dtypes(include=["bool"]).columns
        for col in bool_cols:
            df[col] = df[col].astype(bool)

        return df

    def simulate(self, item):

        data = IoTData(
            log_id=item['log_id'],
            farm_id=item['farm_id'],
            farm_region=item['farm_region'],
            sensor_id=item['sensor_id'],
            device_type=item['device_type'],
            failure_category=item['failure_category'],
            failure_timestamp=item['failure_timestamp'],
            downtime_hours=item['downtime_hours'],
            resolution_action=item['resolution_action'],
            temperature_celsius=item['temperature_celsius'],
            humidity_percent=item['humidity_percent'],
            weather_condition=item['weather_condition'],
            soil_moisture_percent=item['soil_moisture_percent'],
            maintenance_team=item['maintenance_team'],
            resolved=item['resolved'],
            estimated_loss_usd=item['estimated_loss_usd']
        )

        response = self.session.post(
            "http://localhost:8000/send-iot-data",
            json=data.model_dump()
        )

        if response.status_code != 200:
            return
        
        self.db_queue.put(data.model_dump())