import queue
import threading

from src.usecases.simulateIoTUsecase import SimulateIoTUsecase
from src.workers.workers import worker, db_worker


class Scheduler:

    def __init__(self, db_manage):
        self.db_manage = db_manage
    
    def load_database(self, tb_name):

        self.db_manage.create_table(tb_name)

        queue_db = queue.Queue(maxsize=20)

        threading.Thread(
            target=db_worker,
            args=(queue_db, self.db_manage, 20, tb_name),
            daemon=True
        ).start()

        simulate = SimulateIoTUsecase(queue_db)

        data = simulate.load_excel("assets/ai4i2020.csv")

        q = queue.Queue()

        for item in data:
            q.put(item)

        threads = []

        for _ in range(10):
            t = threading.Thread(
                target=worker,
                args=(q, simulate)
            )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()