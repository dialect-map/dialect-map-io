# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from datetime import timezone
from typing import List

from google.api_core.exceptions import DeadlineExceeded
from google.cloud.pubsub_v1 import SubscriberClient
from google.pubsub_v1.types import ReceivedMessage

from dialect_map_io.auth import BaseAuthenticator
from dialect_map_io.auth import DummyAuthenticator

logger = logging.getLogger()


class PubSubReader:
    """
    Class to read Pub/Sub messages synchronously
    Ref: https://cloud.google.com/pubsub/docs/pull#synchronous_pull
    """

    def __init__(
        self,
        project_id: str,
        subscription: str,
        timeout_secs: float = 10.0,
        auth_ctl: BaseAuthenticator = None,
    ):
        """
        Initializes the Pub/Sub reader
        :param project_id: GCP project ID where the subscription is located
        :param subscription: name of the Pub/Sub subscription to read from
        :param timeout_secs: timeout seconds for the pull operation
        :param auth_ctl: authenticator controller (optional)
        """

        if auth_ctl is None:
            auth_ctl = DummyAuthenticator()

        self.timeout_secs = timeout_secs
        self.subscription = subscription
        self.pubsub_client = SubscriberClient(**{"credentials": auth_ctl.credentials})
        self.messages_path = self.pubsub_client.subscription_path(project_id, subscription)

    @staticmethod
    def get_message_id(message: ReceivedMessage) -> str:
        """
        Parses a Pub/Sub high level message, getting its message ID
        :param message: high level Pub/Sub message
        :return: message ID
        """

        return message.message.message_id

    @staticmethod
    def get_message_data(message: ReceivedMessage) -> bytes:
        """
        Parses a Pub/Sub high level message, getting its data
        :param message: high level Pub/Sub message
        :return: message data
        """

        return message.message.data

    @staticmethod
    def get_message_metadata(message: ReceivedMessage) -> dict:
        """
        Parses a Pub/Sub high level message, getting its metadata
        :param message: high level Pub/Sub message
        :return: message metadata attributes
        """

        return message.message.attributes

    @staticmethod
    def get_message_publish_time(message: ReceivedMessage) -> datetime:
        """
        Parses a Pub/Sub high level message, getting its publish time
        :param message: high level Pub/Sub message
        :return: message publish time (UTC)
        """

        str_date = message.message.publish_time.rfc3339()
        off_date = datetime.fromisoformat(str_date.replace("Z", "+00:00"))
        utc_date = datetime.fromtimestamp(off_date.timestamp(), timezone.utc)

        return utc_date

    def _ack_messages(self, ack_ids: List[str]) -> None:
        """
        Acknowledges the received message ACK IDs
        :param ack_ids: list of received ACK IDs
        """

        for ack_id in ack_ids:
            logger.info(f"Acknowledging ID: {ack_id}")

        self.pubsub_client.acknowledge(
            subscription=self.messages_path,
            ack_ids=ack_ids,
        )

    def close(self):
        """Closes the Pubsub connection"""

        logger.info("Disconnecting from PubSub")
        self.pubsub_client.close()

    def pull_messages(self, num_messages: int) -> List[ReceivedMessage]:
        """
        Pulls messages from the Pub/Sub subscription (without ACK)
        :param num_messages: maximum number of messages to pull
        :return: list of messages
        """

        ### NOTE:
        ### To allow a <20 seconds timeout, the pull operation needs to be wrapped
        ### around a try-except block (until DeadlineExceeded exception is better handled)
        ###
        ### Ref: https://github.com/googleapis/google-cloud-python/issues/9390
        ### Ref: https://github.com/googleapis/python-pubsub/issues/343
        try:
            response = self.pubsub_client.pull(
                subscription=self.messages_path,
                max_messages=num_messages,
                timeout=self.timeout_secs,
            )
        except DeadlineExceeded:
            messages = []  # type: ignore
            logger.info(f"Received {len(messages)} new messages")
        else:
            messages = response.received_messages
            logger.info(f"Received {len(messages)} new messages")

        return messages

    def ack_messages(self, messages: List[ReceivedMessage]) -> int:
        """
        Acknowledges the received messages so they will not be sent again
        :param messages: list of received messages
        :return: number of messages acknowledged
        """

        ack_ids = [message.ack_id for message in messages]
        num_ids = len(ack_ids)

        if num_ids > 0:
            self._ack_messages(ack_ids)

        return num_ids
