import select

class EventLoop:
    def __init__(self):
        self.tasks = []
        self.read_waiting = {}
        self.write_waiting = {}

    def create_task(self, coro):
        self.tasks.append(coro)

    def run(self):
        while self.tasks:
            task = self.tasks.pop(0)
            try:
                fd, action = next(task)
                if action == 'read':
                    self.read_waiting[fd] = task
                elif action == 'write':
                    self.write_waiting[fd] = task
            except StopIteration:
                continue

            if self.read_waiting or self.write_waiting:
                can_read, can_write, _ = select.select(self.read_waiting, self.write_waiting, [])
                for fd in can_read:
                    self.tasks.append(self.read_waiting.pop(fd))
                for fd in can_write:
                    self.tasks.append(self.write_waiting.pop(fd))

def my_coroutine(fd):
    yield fd, 'read'
    print("Data is ready to read.")

loop = EventLoop()
loop.create_task(my_coroutine(0))
loop.run()