from fastapi import FastAPI
from src.models.models import IoTData

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


    