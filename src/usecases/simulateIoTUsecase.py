import pandas as pd
import requests

from src.models.models import IoTData

class SimulateIoTUsecase:

    def __init__(self):

        self.session = requests.Session()

    def load_excel(self, path):

        df = pd.read_excel(path)

        return df.to_dict(orient="records")

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

        print(f"{response.status_code}\n")