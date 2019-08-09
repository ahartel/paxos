from router import Router
from message import Packet
import re


class PreliminaryPriest:
    def __init__(self):
        self.__router = None
        self.__initiated_ballot = None
        self.__num_participants = 0
        self.__num_received_lastvote = 0

    def process_next_ballot(self, packet):
        pattern = re.compile("NextBallot\(([0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = match.group(1)
            self.__router.send(Packet(self, "LastVote({},{})".format(ballot, -1), packet.get_source()))

    def process_last_vote(self, packet):
        pattern = re.compile("LastVote\(([0-9]+),([\-0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            last_vote = int(match.group(2))
            if ballot == self.__initiated_ballot:
                self.__num_received_lastvote += 1
        if self.__num_received_lastvote == self.__num_participants:
            self.__router.broadcast(Packet(self, "BeginBallot({}, {})".format(self.__initiated_ballot, 23), None))

    def receive(self, packet):
        message = packet.get_message()
        if "NextBallot" in message:
            self.process_next_ballot(packet)
        elif "LastVote" in message:
            self.process_last_vote(packet)

    def connect_to(self, router):
        self.__router = router
        router.add(self)

    def initiate_ballot(self):
        self.__initiated_ballot = 0
        message = Packet(self, "NextBallot({})".format(self.__initiated_ballot), None)
        self.__num_participants = self.__router.get_num_endpoints()
        self.__router.broadcast(message)


def create_priests(num):
    priests = []
    for n in range(num):
        priests.append(PreliminaryPriest())
    return priests


def print_log(router):
    log = router.get_log()
    for entry in log:
        print(entry)


def main():
    priests = create_priests(5)
    router = Router()
    for priest in priests:
        priest.connect_to(router)

    priests[0].initiate_ballot()
    router.distribute()

    print_log(router)


if __name__ == '__main__':
    main()
