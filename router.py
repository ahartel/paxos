from collections import deque
from message import Packet


class Router:
    def __init__(self):
        self.__endpoints = []
        self.__log = []
        self.__queue = deque()

    def log(self, entry):
        self.__log.append(entry)

    def add(self, endpoint):
        self.log("Adding endpoint {}".format(self.get_num_endpoints()))
        self.__endpoints.append(endpoint)

    def get_endpoints(self):
        return self.__endpoints

    def set_source_index(self, packet):
        sender_index = self.__endpoints.index(packet.get_source())
        return Packet(sender_index, packet.get_message(), packet.get_target())

    def broadcast(self, packet):
        packet = self.set_source_index(packet)
        self.log("Broadcasting: {} to {} endpoints.".format(packet, self.get_num_endpoints()))
        self.__queue.append(packet)

    def get_num_endpoints(self):
        return len(self.get_endpoints())

    def send(self, packet):
        assert not packet.is_broadcast()
        assert packet.get_target() in range(self.get_num_endpoints())
        packet = self.set_source_index(packet)
        assert packet.get_source() in range(self.get_num_endpoints())
        self.log("Appending: {}".format(packet))
        self.__queue.append(packet)

    def distribute(self):
        while len(self.__queue) > 0:
            message = self.__queue.popleft()
            self.log("Distributing {}".format(message))
            if message.is_broadcast():
                for endpoint in self.__endpoints:
                    endpoint.receive(message)
            else:
                self.__endpoints[message.get_target()].receive(message)

    def get_log(self):
        return self.__log
