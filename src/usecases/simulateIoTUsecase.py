import pandas as pd
import requests
import numpy as np

from src.models.models import IoTData

class SimulateIoTUsecase:

    def __init__(self, db_queue):

        self.session = requests.Session()
        self.db_queue = db_queue

    def load_excel(self, path):

        if ".csv" in path:
            df = pd.read_csv(path)
        else:
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
            udi=item['UDI'],
            product_ID=item['Product ID'],
            type=item['Type'],
            air_temperature=item['Air temperature [K]'],
            process_temperature=item['Process temperature [K]'],
            rotational_speed=item['Rotational speed [rpm]'],
            torque=item['Torque [Nm]'],
            tool_wear=item['Tool wear [min]'],
            machine_failure=item['Machine failure'],
            TWF=item['TWF'],
            HDF=item['HDF'],
            PWF=item['PWF'],
            OSF=item['OSF'],
            RNF=item['RNF'],
        )

        response = self.session.post(
            "http://localhost:8000/send-iot-data",
            json=data.model_dump()
        )

        if response.status_code != 200:
            return
        
        self.db_queue.put(data.model_dump())