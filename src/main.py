from src.usecases.simulateIoTUsecase import SimulateIoTUsecase
import uvicorn
import threading
import time


def run_simulation():
    path = "assets/50_rows_simulate.xlsx"
    simulate_iot_usecase = SimulateIoTUsecase(path)
    simulate_iot_usecase.verifyHealth()
    simulate_iot_usecase.simulate()


def start_api():
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )


def main():

    api_thread = threading.Thread(
        target=start_api,
        daemon=True
    )

    api_thread.start()

    time.sleep(2)

    run_simulation()


if __name__ == "__main__":
    main()