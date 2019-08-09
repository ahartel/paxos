from unittest import TestCase
from router import Router
from message import Packet
from unittest.mock import Mock


class TestRouter(TestCase):
    def setUp(self) -> None:
        self.router = Router()

    def test_add_endpoint(self):
        endpoint = Mock()
        self.router.add(endpoint)
        endpoints_in_router = self.router.get_endpoints()
        self.assertEqual(len(endpoints_in_router), 1)
        self.assertEqual(endpoints_in_router[0], endpoint)

    def test_broadcast(self):
        receiver1 = Mock()
        receiver2 = Mock()
        self.router.add(receiver1)
        self.router.add(receiver2)
        message = Packet(2, "Hello world", None)
        self.router.broadcast(message)
        self.router.distribute()
        receiver1.receive.assert_called_with(message)
        receiver2.receive.assert_called_with(message)

    def test_send(self):
        sender = Mock()
        receiver = Mock()
        message = Packet(0, "Hello world", 1)
        self.router.add(sender)
        self.router.add(receiver)
        self.router.send(message)
        self.router.distribute()
        receiver.receive.assert_called_with(message)

    def test_send_not_broadcast(self):
        message = Packet(0, "Hello world", None)
        self.assertRaises(AssertionError, self.router.send, message)

    def tearDown(self) -> None:
        print(self.router.get_log())
