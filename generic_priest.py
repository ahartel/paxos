from collections import deque


class GenericPriest:
    def __init__(self):
        self.router = None
        self.time = 0
        self.queue = deque()
        self.decree = None

    def get_decree(self):
        return self.decree

    def connect_to(self, router):
        self.router = router
        router.add_endpoint(self)

    def distribute(self):
        self.time += 1
        if len(self.queue) > 0:
            message = self.queue.popleft()
            if message.is_broadcast():
                self.router.broadcast(message)
            else:
                self.router.send(message)

    def receive(self, packet):
        message = packet.get_message()
        if "NextBallot" in message:
            self.process_next_ballot(packet)
        elif "LastVote" in message:
            self.process_last_vote(packet)
        elif "BeginBallot" in message:
            self.process_begin_ballot(packet)
        elif "Voted" in message:
            self.process_voted(packet)
        elif "Success" in message:
            self.process_success(packet)
