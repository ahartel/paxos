class Packet:
    def __init__(self, source, message, target):
        self.__source = source
        self.__message = message
        self.__target = target
        if target is None:
            self.__broadcast = True
        else:
            self.__broadcast = False

    def is_broadcast(self):
        return self.__broadcast

    def get_target(self):
        return self.__target

    def get_source(self):
        return self.__source

    def get_message(self):
        return self.__message

    def set_source(self, source):
        self.__source = source

    def __str__(self):
        if self.is_broadcast():
            return "{} )) '{}'".format(self.get_source(), self.get_message())
        else:
            return "{} -> {}: '{}'".format(self.get_source(), self.get_target(), self.get_message())
