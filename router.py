from collections import deque
from message import Packet
import random


class Router:
    def __init__(self):
        self.__endpoints = []
        self.__log = []
        self.__queue = deque()

    def log(self, entry):
        self.__log.append(entry)

    def add_endpoint(self, endpoint):
        self.log("Adding endpoint {}".format(self.get_num_endpoints()))
        self.__endpoints.append(endpoint)

    def get_endpoints(self):
        return self.__endpoints

    def get_source_index(self, packet):
        sender_index = self.__endpoints.index(packet.get_source())
        return sender_index

    def broadcast(self, packet):
        source_index = self.get_source_index(packet)
        assert source_index >= 0
        for endpoint_index, endpoint in enumerate(self.get_endpoints()):
            self.__queue.append(Packet(source_index, packet.get_message(), endpoint_index))
        self.log("Broadcasting: {} to {} endpoints.".format(packet, self.get_num_endpoints()))

    def get_num_endpoints(self):
        return len(self.get_endpoints())

    def send(self, packet):
        assert not packet.is_broadcast()
        assert packet.get_target() in range(self.get_num_endpoints())
        packet.set_source(self.get_source_index(packet))
        assert packet.get_source() in range(self.get_num_endpoints())
        self.log("Appending: {}".format(packet))
        self.__queue.append(packet)

    def decide_to_drop(self, message):
        if random.randint(0, 100) > 90:
            self.log("Dropping message {}".format(message))
            return True
        else:
            return False

    def distribute(self):
        if len(self.__queue) > 0:
            message = self.__queue.popleft()
            if self.decide_to_drop(message):
                return
            else:
                self.do_send(message)

    def do_send(self, message):
        self.log("Distributing {}".format(message))
        if message.is_broadcast():
            raise NotImplementedError
        else:
            self.__endpoints[message.get_target()].receive(message)

    def get_log(self):
        return self.__log
