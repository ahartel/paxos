from unittest import TestCase
from unittest import skip
from basic_protocol import BasicPriest
from unittest.mock import Mock


class TestBasicPriest(TestCase):
    def setUp(self) -> None:
        self.ZeroRng = Mock()
        self.ZeroRng.sample_boolean.return_value = False
        self.OneRng = Mock()
        self.OneRng.sample_boolean.return_value = True

    @staticmethod
    def setupPriestAndRouterWithDelay(delay, rng):
        router = Mock()
        priest = BasicPriest(delay, router, rng)
        return priest, router

    def test_can_receive_and_send(self):
        priest, router = self.setupPriestAndRouterWithDelay(0, self.OneRng)
        priest.receive("message")
        priest.distribute()
        router.send.assert_called_once()

    def test_can_delay(self):
        priest, router = self.setupPriestAndRouterWithDelay(1, self.OneRng)
        priest.receive("message")
        priest.distribute()
        router.send.assert_not_called()
        priest.distribute()
        router.send.assert_called_once()

    def test_does_not_want_to_act(self):
        priest = BasicPriest(0, None, self.ZeroRng)
        self.assertEqual(False, priest.want_to_act())

    def test_does_want_to_act(self):
        priest = BasicPriest(0, None, self.OneRng)
        self.assertEqual(True, priest.want_to_act())

    def test_can_act_conditionally(self):
        priest, router = self.setupPriestAndRouterWithDelay(0, self.ZeroRng)
        priest.receive("message")
        priest.distribute()
        router.send.assert_not_called()

