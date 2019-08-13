from collections import deque


class BasicPriest:
    def __init__(self, delay, router, rng):
        self.delay = delay
        self.router = router
        self.rng = rng
        self.queue = deque()
        self.time = 0

    def want_to_act(self):
        return self.rng.sample_boolean()

    def receive(self, message):
        if self.want_to_act():
            self.queue.append((self.time, message))

    def next_queue_element_ready(self):
        return self.queue[-1][0] + self.delay == self.time

    def need_to_send_something(self):
        queue_not_empty = len(self.queue) > 0
        if queue_not_empty:
            return self.next_queue_element_ready()
        else:
            return False

    def distribute(self):
        while self.need_to_send_something():
            self.router.send(self.queue.popleft())
        self.time += 1

