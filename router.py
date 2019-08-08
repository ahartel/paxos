class Router:
    def __init__(self):
        self.__endpoints = []
        self.__log = []

    def log(self, entry):
        self.__log.append(entry)

    def add(self, endpoint):
        self.log("Adding endpoint {}".format(self.get_num_endpoints()))
        self.__endpoints.append(endpoint)

    def get_endpoints(self):
        return self.__endpoints

    def broadcast(self, message):
        self.log("Broadcasting: {} to {} endpoints.".format(message, self.get_num_endpoints()))
        for endpoint in self.__endpoints:
            endpoint.receive(message)

    def get_num_endpoints(self):
        return len(self.get_endpoints())

    def send(self, message):
        assert not message.is_broadcast()
        assert message.get_target() in range(self.get_num_endpoints())
        assert message.get_source() in range(self.get_num_endpoints())
        self.log("Sending: {}".format(message))
        self.__endpoints[message.get_target()].receive(message)

    def get_log(self):
        return self.__log
