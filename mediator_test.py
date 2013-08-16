from mediator import Mediator
from unittest import TestCase
import mock


class MediatorTest(TestCase):

    def setUp(self):
        self.mediator = Mediator()

    def test_event__load(self):
        '''
        Check that the load event gets called
        '''
        Mediator._load = mock.MagicMock()

        Mediator.load()

        Mediator._load.assert_called_once_with()

    def test_event__unload(self):
        Mediator._load = mock.MagicMock()

        Mediator.load()

        Mediator._load.assert_called_once_with()





if __name__ == '__main__':
    MediatorTest()
