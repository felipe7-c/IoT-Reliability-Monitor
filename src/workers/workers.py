from queue import Empty


def worker(queue, simulate_usecase):

    while not queue.empty():

        try:
            item = queue.get()

            simulate_usecase.simulate(item)

            queue.task_done()

        except Exception as e:
            print(e)


def db_worker(queue, db_manage, batch_size, tb_name):

    batch = []

    while True:

        try:
            item = queue.get(timeout=1)

            batch.append(item)

            queue.task_done()

            if len(batch) >= batch_size:

                db_manage.insert_data(tb_name, batch.copy())

                batch.clear()

        except Empty:

            if batch:

                db_manage.insert_data(tb_name, batch.copy())

                batch.clear()