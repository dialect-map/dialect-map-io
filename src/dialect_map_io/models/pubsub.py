# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Union


@dataclass
class DiffMessage:
    """
    Object containing the attributes of a data diff Pub/Sub message

    :attr container: dict / list containing the changed field
    :attr field_name: field name that got changed (or "ARRAY")
    :attr value_prev: value before the change
    :attr value_post: value after the change
    :attr source_file: file name where the change may have been originated
    :attr created_at: datetime when the change was produced
    """

    container: Union[Dict, List]
    field_name: str
    value_prev: Any
    value_post: Any
    source_file: str
    created_at: datetime

    @classmethod
    def from_pubsub(cls, message: dict):
        """
        Builds a diff message object from a Pub/Sub parsed message
        :param message: Pub/Sub parsed message
        :return: diff message object
        """

        return DiffMessage(
            message["container"],
            message["fieldName"],
            message["valuePrev"],
            message["valuePost"],
            message["sourceFile"],
            message["createdAt"],
        )

    def __post_init__(self):
        """ Checks the provided previous and posterior values consistency """

        if self.value_prev is None and self.value_post is None:
            raise ValueError("Invalid value change. Both values are NULL")

        if self.value_prev == self.value_post:
            raise ValueError("Invalid value change. Both values are equal")

    def is_creation(self) -> bool:
        """
        Checks if the diff message correspond to a creation
        :return: whether it is a creation
        """

        return self.value_prev is None and self.value_post is not None

    def is_deletion(self) -> bool:
        """
        Checks if the diff message correspond to a deletion
        :return: whether it is a deletion
        """

        return self.value_prev is not None and self.value_post is None

    def is_edition(self) -> bool:
        """
        Checks if the diff message correspond to an edition
        :return: whether it is a edition
        """

        return self.value_prev is not None and self.value_post is not None
