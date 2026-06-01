from src.usecases.simulateIoTUsecase import SimulateIoTUsecase
from src.infra.databaseManage import databaseManage
from src.infra.postgreSqlConn import PostgreSqlConn
import threading
import queue
import uvicorn
import time
from dotenv import load_dotenv
import os

load_dotenv()
admin = os.getenv("DB_ADMIN")
pssw = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")

def start_api():

    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )

def worker(queue, simulate_usecase):

    while not queue.empty():

        try:

            item = queue.get()

            simulate_usecase.simulate(item)

            queue.task_done()

        except Exception as e:
            raise Exception(f"Error no worker de simulação: {e}")

def db_worker(queue, db_manage, batch_size):
    
    batch = []

    while True:

        if not queue.empty():

            item = queue.get()

            if len(batch) >= batch_size:
                db_manage.insert_data("iot_data_table", batch)
                batch.clear()

            batch.append(item) 
            queue.task_done()

def main():

    #Conexão com o banco de dados
    database = PostgreSqlConn(
        user = admin,
        password = pssw, 
        host = host,
        port = port, 
        database = db
    )

    db_manage = databaseManage(database.get_engine())

    #Worker de API em paralelo
    path = "assets/50_rows_simulate.xlsx"

    api_thread = threading.Thread(
        target=start_api,
        daemon=True
    )

    api_thread.start()

    time.sleep(3)

    #Worker de banco de dados em paralelo

    queue_db = queue.Queue(maxsize = 20)

    db_thread = threading.Thread(
        target = db_worker, 
        args = (queue_db, db_manage, 20),
        daemon = True
    )

    db_thread.start()

    #Worker de simulação em paralelo

    simulate_usecase = SimulateIoTUsecase(queue_db)

    data = simulate_usecase.load_excel(path)

    q = queue.Queue()

    for item in data:
        q.put(item)

    threads = []

    num_threads = 10

    for _ in range(num_threads):

        t = threading.Thread(
            target=worker,
            args=(q, simulate_usecase)
        )

        t.start()

        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()