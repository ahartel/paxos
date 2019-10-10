import os
import re
import random
from router import Router
from message import Packet
from collections import deque
from log_printer import LogPrinter
from generic_priest import GenericPriest


class SlipOfPaper:
    def __init__(self):
        self.num_received_last_vote = 0
        self.num_participants = 0
        self.quorum = 0
        self.proposed_decree = None
        self.received_votes = []


class BasicPriest(GenericPriest):
    def __init__(self):
        super(BasicPriest, self).__init__()

        # 3 variables that are needed according to the paper
        self.last_tried = -1
        self.prev_vote = -1
        self.next_bal = -1
        # a slip of paper that should only be needed by the initiating priest
        self.slip = SlipOfPaper()

    def initiate_ballot(self):
        self.last_tried = self.last_tried + 1
        message = Packet(self, "NextBallot({})".format(self.last_tried), None)
        self.slip.num_participants = self.router.get_num_endpoints()
        self.slip.quorum = int(self.slip.num_participants/2)+1
        self.queue.append(message)
        self.slip.num_received_last_vote = 0

    def process_next_ballot(self, packet):
        pattern = re.compile("NextBallot\(([0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            if ballot > self.next_bal:
                self.queue.append(Packet(self, "LastVote({},{})".format(ballot, self.prev_vote), packet.get_source()))
                self.next_bal = ballot

    def process_last_vote(self, packet):
        pattern = re.compile("LastVote\(([0-9]+),([\-0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            last_vote = int(match.group(2))
            if ballot == self.last_tried:
                self.slip.num_received_last_vote += 1
        if self.slip.num_received_last_vote == self.slip.num_participants:
            self.slip.proposed_decree = 23
            send = Packet(self, "BeginBallot({},{})".format(self.last_tried, self.slip.proposed_decree), None)
            self.queue.append(send)

    def process_begin_ballot(self, packet):
        pattern = re.compile("BeginBallot\(([0-9]+),([\-0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            decree = int(match.group(2))
            if ballot == self.next_bal:
                self.prev_vote = ballot
                self.queue.append(Packet(self, "Voted({})".format(ballot), packet.get_source()))

    def process_voted(self, packet):
        pattern = re.compile("Voted\(([0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            ballot = int(match.group(1))
            if ballot == self.last_tried:
                self.slip.received_votes.append(packet.get_source())
        if len(self.slip.received_votes) == self.slip.quorum:
            self.decree = self.slip.proposed_decree
            self.queue.append(Packet(self, "Success({})".format(self.slip.proposed_decree), None))

    def process_success(self, packet):
        pattern = re.compile("Success\(([0-9]+)\)")
        match = pattern.match(packet.get_message())
        if match:
            decree = int(match.group(1))
            self.decree = decree


def create_priests(num):
    priests = []
    for n in range(num):
        priests.append(BasicPriest())
    return priests


def main():
    seed = ord(os.urandom(1))
    #seed = 217
    print("Running with seed {}".format(seed))
    random.seed(seed)
    priests = create_priests(5)
    router = Router()
    for priest in priests:
        priest.connect_to(router)

    any_decree_committed = False
    iteration = 0
    while not any_decree_committed:
        print("Iteration {}".format(iteration))
        priests[0].initiate_ballot()
        for t in range(30):
            router.distribute()
            for priest in priests:
                priest.distribute()

        for priest in priests:
            if priest.get_decree() is not None:
                any_decree_committed = True
                break

        iteration += 1

    printer = LogPrinter(router.get_log(), len(priests))
    printer.print()
    router.reset_log()
    print("Selected decree is {}".format(priest.get_decree()))


if __name__ == '__main__':
    main()