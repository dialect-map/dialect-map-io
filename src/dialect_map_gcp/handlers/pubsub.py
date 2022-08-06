# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from datetime import timezone
from typing import List

from google.cloud.pubsub_v1 import SubscriberClient
from google.pubsub_v1.types import ReceivedMessage as Message

from dialect_map_io.auth import BaseAuthenticator
from dialect_map_io.auth import DummyAuthenticator
from dialect_map_io.encoding import BasePlainDecoder
from dialect_map_io.encoding import JSONPlainDecoder

from .base import BaseQueueHandler


logger = logging.getLogger()


class PubSubQueueHandler(BaseQueueHandler):
    """
    Class to handle Pub/Sub messages synchronously
    Ref: https://cloud.google.com/pubsub/docs/pull#synchronous_pull
    """

    def __init__(
        self,
        project_id: str,
        subscription: str,
        timeout_secs: float = 10.0,
        auth_ctl: BaseAuthenticator = None,
        decoder: BasePlainDecoder = None,
    ):
        """
        Initializes the Pub/Sub handler
        :param project_id: GCP project ID where the subscription is located
        :param subscription: name of the Pub/Sub subscription to read from
        :param timeout_secs: timeout seconds for the pull operation (optional)
        :param auth_ctl: authenticator controller (optional)
        :param decoder: messages content decoder (optional)
        """

        if auth_ctl is None:
            auth_ctl = DummyAuthenticator()

        if decoder is None:
            decoder = JSONPlainDecoder()

        self.messages_dec = decoder
        self.subscription = subscription
        self.timeout_secs = timeout_secs

        self.pubsub_client = SubscriberClient(**{"credentials": auth_ctl.credentials})
        self.messages_path = self.pubsub_client.subscription_path(project_id, subscription)

    @staticmethod
    def get_message_metadata(message: Message) -> dict:
        """
        Parses the provided Pub/Sub message getting its metadata
        :param message: Pub/Sub message
        :return: message metadata
        """

        return message.message.attributes

    @staticmethod
    def get_message_publish_time(message: Message) -> datetime:
        """
        Parses the provided Pub/Sub message getting its published time
        :param message: Pub/Sub message
        :return: message published time (UTC)
        """

        str_date = message.message.publish_time.rfc3339()
        off_date = datetime.fromisoformat(str_date.replace("Z", "+00:00"))
        utc_date = datetime.fromtimestamp(off_date.timestamp(), timezone.utc)

        return utc_date

    def _get_message_ack_id(self, message: Message) -> str:
        """
        Gets the provided Pub/Sub message ack ID
        :param message: Pub/Sub message
        :return: message ack ID
        """

        return message.ack_id

    def _get_message_main_id(self, message: Message) -> str:
        """
        Gets the provided Pub/Sub message main ID
        :param message: Pub/Sub message
        :return: message main ID
        """

        return message.message.message_id

    def _get_message_data(self, message: Message) -> bytes:
        """
        Gets the provided Pub/Sub message data
        :param message: Pub/Sub message
        :return: message data
        """

        return message.message.data

    def _ack_messages(self, messages: List[Message]) -> None:
        """
        Acknowledges the list of received messages
        :param messages: list of received messages
        """

        ids = []

        for message in messages:
            ack_id = self._get_message_ack_id(message)
            msg_id = self._get_message_main_id(message)

            logger.info(f"Acknowledging message {msg_id}")
            ids.append(ack_id)

        self.pubsub_client.acknowledge(subscription=self.messages_path, ack_ids=ids)

    def _dec_messages(self, messages: List[Message]) -> List[object]:
        """
        Decoded the received messages raw content
        :param messages: list of received messages
        :return: list of decoded messages content
        """

        messages = map(lambda m: self._get_message_data(m), messages)
        messages = map(lambda m: self.messages_dec.decode(m), messages)

        return list(messages)

    def _pull_messages(self, num_messages: int) -> List[Message]:
        """
        Pulls messages from the Pub/Sub subscription (without ACK)
        :param num_messages: maximum number of messages to pull
        :return: list of messages
        """

        response = self.pubsub_client.pull(
            subscription=self.messages_path,
            max_messages=num_messages,
            timeout=self.timeout_secs,
        )

        messages = response.received_messages
        logger.info(f"Received {len(messages)} messages")

        return messages

    def close(self):
        """Closes the Pubsub connection"""

        logger.info("Disconnecting from PubSub")
        self.pubsub_client.close()

    def get_messages(self, num_messages: int) -> List[object]:
        """
        Gets and decodes messages from the Pub/Sub subscription
        :param num_messages: max number of messages to get
        :return: list of messages
        """

        msg_objects = self._pull_messages(num_messages)
        msg_records = self._dec_messages(msg_objects)

        self._ack_messages(msg_objects)
        return msg_records
