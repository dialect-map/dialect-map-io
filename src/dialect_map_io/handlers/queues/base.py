# -*- coding: utf-8 -*-

from abc import ABC
from abc import abstractmethod
from typing import List


class BaseQueueHandler(ABC):
    """Interface for the queue handler classes"""

    @abstractmethod
    def close(self) -> None:
        """Closes the queue connection"""

        raise NotImplementedError()

    @abstractmethod
    def pull_messages(self, queue_name: str, num_messages: int) -> List[object]:
        """
        Pulls and decodes messages from the target queue
        :param queue_name: name of the queue to pull messages from
        :param num_messages: max number of messages to pull
        :return: list of decoded messages
        """

        raise NotImplementedError()

    @abstractmethod
    def push_messages(self, queue_name: str, messages: List[object]) -> int:
        """
        Encodes and pushes messages to the target queue
        :param queue_name: name of the queue to push messages to
        :param messages: list of messages to push
        :return: number of messages pushed
        """

        raise NotImplementedError()
