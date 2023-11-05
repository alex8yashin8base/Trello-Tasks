import concurrent.futures
import threading
import queue

class MyThreadPoolExecutor:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.thread_pool = []
        self.task_queue = queue.Queue()
        self.shutdown = False

        for _ in range(max_workers):
            thread = threading.Thread(target=self._worker)
            thread.start()
            self.thread_pool.append(thread)

    def _worker(self):
        while not self.shutdown:
            try:
                task = self.task_queue.get()
            except queue.Empty:
                continue

            if task is None:
                break

            func, args, kwargs, future = task
            try:
                result = func(*args, **kwargs)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                self.task_queue.task_done()

    def submit(self, func, *args, **kwargs):
        if self.shutdown:
            raise RuntimeError("Cannot submit tasks after shutdown")

        future = concurrent.futures.Future()
        self.task_queue.put((func, args, kwargs, future))
        return future

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.shutdown = True
        for _ in range(self.max_workers):
            self.task_queue.put(None)

        for thread in self.thread_pool:
            thread.join()

def some_function(x):
    return x * 2

with MyThreadPoolExecutor(max_workers=3) as executor:
    results = [executor.submit(some_function, i) for i in range(10)]

    for future in concurrent.futures.as_completed(results):
        result = future.result()
        print(result)