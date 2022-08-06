# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import List


class BaseQueueHandler(ABC):
    """Interface for the message queue classes"""

    @abstractmethod
    def close(self) -> None:
        """Closes the message queue connection"""

        raise NotImplementedError()

    @abstractmethod
    def get_messages(self, num_messages: int) -> List[object]:
        """
        Gets and decodes messages from the message queue
        :param num_messages: max number of messages to get
        :return: list of messages
        """

        raise NotImplementedError()
