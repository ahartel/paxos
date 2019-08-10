from unittest import TestCase
from router import Router
from message import Packet
from unittest.mock import Mock


class TestRouter(TestCase):
    def setUp(self) -> None:
        self.router = Router()

    def test_add_endpoint(self):
        endpoint = Mock()
        self.router.add_endpoint(endpoint)
        endpoints_in_router = self.router.get_endpoints()
        self.assertEqual(len(endpoints_in_router), 1)
        self.assertEqual(endpoints_in_router[0], endpoint)

    def test_broadcast(self):
        receiver1 = Mock()
        receiver2 = Mock()
        sender = Mock()
        self.router.add_endpoint(receiver1)
        self.router.add_endpoint(receiver2)
        self.router.add_endpoint(sender)
        message_sent = Packet(sender, "Hello world", None)
        self.router.broadcast(message_sent)
        self.router.distribute()
        receiver1.receive.assert_called_once()
        receiver2.receive.assert_called_once()

    def test_send(self):
        sender = Mock()
        receiver = Mock()
        message = Packet(sender, "Hello world", 1)
        self.router.add_endpoint(sender)
        self.router.add_endpoint(receiver)
        self.router.send(message)
        self.router.distribute()
        receiver.receive.assert_called_once()

    def test_send_not_broadcast(self):
        message = Packet(0, "Hello world", None)
        self.assertRaises(AssertionError, self.router.send, message)

    def tearDown(self) -> None:
        print(self.router.get_log())
