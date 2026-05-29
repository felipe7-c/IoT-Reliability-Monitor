from src.usecases.simulateIoTUsecase import SimulateIoTUsecase

import pandas as pd
import threading
import queue
import uvicorn
import time

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
            print(e)

def main():

    #Worker de API em paralelo
    path = "assets/50_rows_simulate.xlsx"

    api_thread = threading.Thread(
        target=start_api,
        daemon=True
    )

    api_thread.start()

    time.sleep(3)

    simulate_usecase = SimulateIoTUsecase()

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