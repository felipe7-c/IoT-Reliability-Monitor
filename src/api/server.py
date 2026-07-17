from fastapi import FastAPI
from src.models.models import IoTData
from src.infra.databaseManage import DatabaseManage

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "Bem vindo a API de Monitoramento de Confibilidade"}

@app.get("/health")
def health_check():
    return {"status" : "OK"}

@app.post("/send-iot-data")
def receive_data(iot_data : IoTData):
    if iot_data is None:
        return {"message" : "Nenhum dado recebido"}
    
    return {"message" : "Dados recebidos com sucesso! \n " + str(iot_data)}

@app.get("/get-info-iot-data")
def get_info_iot_data():
    return {"message" : "Informações sobre os dados de IoT"}


    