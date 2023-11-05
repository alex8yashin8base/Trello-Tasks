import concurrent.futures
import threading
import queue

class MyThreadPoolExecutor:
    def __init__(self, max_workers):
        # лучше переименовывать те атрибуты к которым доступ не жалетелен из вне
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
            # Empty error здесь не возникнет тк нет timeout'a
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
        # стоило реализовать функцию close или stop такую же. А в __exit__ вызывать уже ее.
        # Просто далеко не всегда люди используют with выражение. Допустим thread pool где-то инициализируется в одном месте, а уже в другом стопится
        # Пример: обычный бэкенд какого-нидуь приложения. Во время startup создается пул, а уже при shutdown он закрывается
        self.shutdown = True
        for _ in range(self.max_workers):
            self.task_queue.put(None)

        # я бы перенес join'ы в отедльную функцию. Для того чтобы сделать какую-то работу параллельно пока стопятся потоки. Так уменьшается время остановки
        for thread in self.thread_pool:
            thread.join()

def some_function(x):
    return x * 2

with MyThreadPoolExecutor(max_workers=3) as executor:
    results = [executor.submit(some_function, i) for i in range(10)]

    for future in concurrent.futures.as_completed(results):
        result = future.result()
        print(result)
