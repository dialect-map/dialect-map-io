# -*- coding: utf-8 -*-

from dataclasses import dataclass
from dataclasses import fields
from datetime import datetime
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
    value_prev: object
    value_post: object
    source_file: str
    created_at: datetime

    @classmethod
    def fields(cls) -> set:
        """
        Returns a set with the dataclass field names
        :return: set with the dataclass field names
        """

        return {f.name for f in fields(cls)}

    @classmethod
    def from_pubsub(cls, message: dict):
        """
        Builds a diff message object from a Pub/Sub parsed message
        :param message: Pub/Sub parsed message
        :return: diff message object
        """

        return cls(
            message["container"],
            message["fieldName"],
            message["valuePrev"],
            message["valuePost"],
            message["sourceFile"],
            message["createdAt"],
        )

    def __post_init__(self):
        """Checks the provided previous and posterior values consistency"""

        if (
            True
            and self.is_creation is False
            and self.is_deletion is False
            and self.is_edition is False
        ):
            raise ValueError("Invalid diff message")

    @property
    def is_creation(self) -> bool:
        """
        Checks if the diff message correspond to a creation
        :return: whether it is a creation
        """

        return (
            isinstance(self.container, list)
            and self.value_prev is None
            and self.value_post is not None
        )

    @property
    def is_deletion(self) -> bool:
        """
        Checks if the diff message correspond to a deletion
        :return: whether it is a deletion
        """

        return (
            isinstance(self.container, list)
            and self.value_prev is not None
            and self.value_post is None
        )

    @property
    def is_edition(self) -> bool:
        """
        Checks if the diff message correspond to an edition
        :return: whether it is a edition
        """

        return (
            isinstance(self.container, dict)
            and self.value_prev is not None
            and self.value_post is not None
        )
