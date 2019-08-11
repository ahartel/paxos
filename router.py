from collections import deque
from message import Packet
import random


class Router:
    def __init__(self):
        self.__endpoints = []
        self.__log = []
        self.__queue = deque()
        self.__time = 0

    def log(self, entry, index):
        self.__log.append((self.__time, entry, index))

    def add_endpoint(self, endpoint):
        new_index = self.get_num_endpoints()
        self.log("Adding endpoint {}".format(new_index), new_index)
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
        self.log("Broadcasting: '{}' to {} endpoints.".format(packet.get_message(), self.get_num_endpoints()), source_index)

    def get_num_endpoints(self):
        return len(self.get_endpoints())

    def send(self, packet):
        assert not packet.is_broadcast()
        assert packet.get_target() in range(self.get_num_endpoints())
        packet.set_source(self.get_source_index(packet))
        assert packet.get_source() in range(self.get_num_endpoints())
        self.log("Appending: {}".format(packet), packet.get_source())
        self.__queue.append(packet)

    def decide_to_drop(self, message):
        if random.randint(0, 100) > 90:
            self.log("Dropping message {}".format(message), message.get_target())
            return True
        else:
            return False

    def distribute(self):
        self.__time += 1
        if len(self.__queue) > 0:
            packet = self.__queue.popleft()
            if self.decide_to_drop(packet):
                return
            else:
                self.do_send(packet)

    def do_send(self, packet):
        self.log("Distributing {}".format(packet), packet.get_target())
        if packet.is_broadcast():
            raise NotImplementedError
        else:
            self.__endpoints[packet.get_target()].receive(packet)

    def get_log(self):
        return self.__log
