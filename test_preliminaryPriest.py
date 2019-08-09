from unittest import TestCase
from preliminary_protocoll import PreliminaryPriest
from message import Packet


class TestPreliminaryPriest(TestCase):
    def setUp(self) -> None:
        self.priest = PreliminaryPriest()

    def test_receive(self):
        message = Packet(0, "Hello world", 1)
        self.priest.receive(message)
