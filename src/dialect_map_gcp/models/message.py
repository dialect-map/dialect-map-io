# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from typing import Dict
from typing import List


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

    container: Dict | List
    field_name: str
    value_prev: object
    value_post: object
    source_file: str
    created_at: datetime

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

    def _augment_record(self, record: dict) -> dict:
        """
        Augments the provided data record with message level fields
        :param record: vanilla data record
        :return: the augmented data record
        """

        if self.is_creation:
            record["created_at"] = self.created_at

        return record

    @cached_property
    def record(self) -> dict:
        """
        Returns the data record within a diff operation message.
        Some fields are inherited from the diff operation message
        :return: the data record
        """

        record = None

        if self.is_creation:
            record = self.value_post
        elif self.is_deletion:
            record = self.value_prev
        elif self.is_edition:
            record = self.container

        assert isinstance(record, dict)
        return self._augment_record(record)

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
