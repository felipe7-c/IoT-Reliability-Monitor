import pandas as pd
import requests as req
from src.models.models import IoTData
import time
import json

class SimulateIoTUsecase:
    def __init__(self, repository_path):
        self.repository_path = repository_path
        self.data = None
        try: 
            df = pd.read_excel(repository_path)
            self.data = df
        except Exception as e:
            print(f"Erro ao ler o arquivo de dados IoT: {e}")
    def simulate(self):
        if self.data is None:
            print("Nenhum dado disponível para simulação")
            return
        
        for _, row in self.data.iterrows():

            data = IoTData(
                log_id = row['log_id'],
                farm_id = row['farm_id'],
                farm_region = row['farm_region'],
                sensor_id = row['sensor_id'],
                device_type = row['device_type'],
                failure_category = row['failure_category'],
                failure_timestamp = row['failure_timestamp'],
                downtime_hours = row['downtime_hours'],
                resolution_action = row['resolution_action'],
                temperature_celsius = row['temperature_celsius'],
                humidity_percent = row['humidity_percent'],
                weather_condition = row['weather_condition'],
                soil_moisture_percent = row['soil_moisture_percent'],
                maintenance_team = row['maintenance_team'],
                resolved = row['resolved'],
                estimated_loss_usd = row['estimated_loss_usd']
            )

            response = req.post("http://localhost:8000/send-iot-data", json = data.dict())
            if response.status_code != 200:
                raise Exception(f"Erro ao enviar dados: {response.status_code} - {response.text}")
    def verifyHealth(self):
        while True:
            response = req.get("http://localhost:8000/health")
            if response.status_code == 200:
                break
            else:
                time.sleep(2)
                self.verifyHealth()
            
