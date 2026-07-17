import uvicorn
import os
import threading
from src.workers.scheduler import Scheduler
from src.infra.databaseManage import DatabaseManage
from dotenv import load_dotenv

load_dotenv()

pssw = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")
tb_name = os.getenv("TB_NAME")

def run_api():
    """Roda a API em uma thread separada"""
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

def run_scheduler(pssw, host, port, db, tb_name):
    """Roda o scheduler em uma thread separada"""
    db_manage = DatabaseManage.get_instance(
        "postgres",
        pssw,
        host,
        port,
        db
    )

    scheduler = Scheduler(db_manage)
    scheduler.load_database(tb_name)

def main():
    # Cria thread para a API
    api_thread = threading.Thread(
        target=run_api,
        daemon=True
    )
    
    # Cria thread para o scheduler
    scheduler_thread = threading.Thread(
        target=run_scheduler,
        args=(pssw, host, port, db, tb_name),
        daemon=True
    )
    
    # Inicia ambas as threads
    api_thread.start()
    scheduler_thread.start()
    
    # Mantém o programa rodando
    try:
        api_thread.join()
    except KeyboardInterrupt:
        print("\nEncerrando aplicação...")

if __name__ == "__main__":
    main()