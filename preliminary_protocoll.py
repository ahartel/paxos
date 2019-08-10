from router import Router
from message import Packet
import re


class PreliminaryPriest:
    def __init__(self):
        self.__router = None
        self.__initiated_ballot = None
        self.__num_participants = 0
        self.__num_received_last_vote = 0
        self.__last_decree_received = None
        self.__last_ballot_voted = None
        self.__decree = None
        self.__max_ballot_received = None
        self.__received_votes = []
        self.__proposed_decree = None

    def get_decree(self):
        return self.__decree

    def process_next_ballot(self, packet):
        pattern = re.compile("NextBallot\(([0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            self.__router.send(Packet(self, "LastVote({},{})".format(ballot, -1), packet.get_source()))
            self.__max_ballot_received = ballot

    def process_last_vote(self, packet):
        pattern = re.compile("LastVote\(([0-9]+),([\-0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            last_vote = int(match.group(2))
            if ballot == self.__initiated_ballot:
                self.__num_received_last_vote += 1
        if self.__num_received_last_vote == self.__num_participants:
            self.__proposed_decree = 23
            send = Packet(self, "BeginBallot({},{})".format(self.__initiated_ballot, self.__proposed_decree), None)
            self.__router.broadcast(send)

    def process_begin_ballot(self, packet):
        pattern = re.compile("BeginBallot\(([0-9]+),([\-0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            decree = int(match.group(2))
            if ballot == self.__max_ballot_received:
                self.__last_decree_received = decree
                self.__last_ballot_voted = ballot
                self.__router.send(Packet(self, "Voted({})".format(ballot), packet.get_source()))

    def process_voted(self, packet):
        pattern = re.compile("Voted\(([0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            if ballot == self.__initiated_ballot:
                self.__received_votes.append(packet.get_source())
        if len(self.__received_votes) == self.__num_participants:
            self.__router.broadcast(Packet(self, "Success({})".format(self.__proposed_decree), None))

    def process_success(self, packet):
        pattern = re.compile("Success\(([0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            decree = int(match.group(1))
            self.__decree = decree

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

    for priest in priests:
        print(priest.get_decree())


if __name__ == '__main__':
    main()
