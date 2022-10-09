# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from datetime import timezone
from typing import List

from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1 import SubscriberClient
from google.pubsub_v1.types import ReceivedMessage as Message

from dialect_map_io.auth import BaseAuthenticator
from dialect_map_io.auth import DummyAuthenticator
from dialect_map_io.encoding import BaseBinaryDecoder
from dialect_map_io.encoding import BaseBinaryEncoder
from dialect_map_io.encoding import JSONBinaryDecoder
from dialect_map_io.encoding import JSONBinaryEncoder
from dialect_map_io.handlers import BaseQueueHandler


logger = logging.getLogger()


class PubSubQueueHandler(BaseQueueHandler):
    """
    Class to handle Pub/Sub messages synchronously
    Ref 1: https://cloud.google.com/pubsub/docs/pull
    Ref 2: https://cloud.google.com/pubsub/docs/publisher
    """

    def __init__(
        self,
        project_id: str,
        timeout_secs: float = 10.0,
        auth_ctl: BaseAuthenticator = None,
        decoder: BaseBinaryDecoder = None,
        encoder: BaseBinaryEncoder = None,
    ):
        """
        Initializes the Pub/Sub handler
        :param project_id: GCP project ID where the topic / subscription are located
        :param timeout_secs: timeout seconds for the pull operation (optional)
        :param auth_ctl: authenticator controller (optional)
        :param decoder: messages content decoder (optional)
        :param encoder: messages content encoder (optional)
        """

        if auth_ctl is None:
            auth_ctl = DummyAuthenticator()
        if decoder is None:
            decoder = JSONBinaryDecoder()
        if encoder is None:
            encoder = JSONBinaryEncoder()

        self.project_id = project_id
        self.messages_dec = decoder
        self.messages_enc = encoder
        self.timeout_secs = timeout_secs

        self._publisher_client = PublisherClient(**{"credentials": auth_ctl.credentials})
        self._subscriber_client = SubscriberClient(**{"credentials": auth_ctl.credentials})

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

    def _ack_messages(self, subscription_path: str, messages: List[Message]) -> None:
        """
        Acknowledges the list of received messages
        :param subscription_path: path to the Pub/Sub subscription
        :param messages: list of received messages
        """

        ids = []

        for message in messages:
            ack_id = self._get_message_ack_id(message)
            msg_id = self._get_message_main_id(message)

            logger.info(f"Acknowledging message {msg_id}")
            ids.append(ack_id)

        self._subscriber_client.acknowledge(
            subscription=subscription_path,
            ack_ids=ids,
        )

    def _pull_messages(self, subscription_path: str, num_messages: int) -> List[Message]:
        """
        Pulls messages from the Pub/Sub subscription (without ACK)
        :param subscription_path: path to the Pub/Sub subscription
        :param num_messages: maximum number of messages to pull
        :return: list of messages
        """

        response = self._subscriber_client.pull(
            subscription=subscription_path,
            max_messages=num_messages,
            timeout=self.timeout_secs,
        )

        messages = response.received_messages
        logger.info(f"Received {len(messages)} messages")

        return messages

    def _push_messages(self, topic_path: str, messages: List[bytes]) -> int:
        """
        Publishes objects as messages to a Pub/Sub topic
        :param topic_path: path to the Pub/Sub topic
        :param messages: list of message objects to publish
        :return: number of messages published
        """

        for msg_data in messages:
            self._publisher_client.publish(
                topic=topic_path,
                data=msg_data,
                timeout=self.timeout_secs,
            )

        logger.info(f"Published {len(messages)} messages")
        return len(messages)

    def close(self):
        """Closes the Pubsub connection"""

        logger.info("Disconnecting from PubSub")
        self._subscriber_client.close()
        self._publisher_client.close()

    def pull_messages(self, subscription: str, num_messages: int) -> List[object]:
        """
        Pulls and decodes messages from a Pub/Sub subscription
        :param subscription: name of the Pub/Sub subscription to pull from
        :param num_messages: max number of messages to pull
        :return: list of messages
        """

        subscription_path = self._subscriber_client.subscription_path(self.project_id, subscription)
        received_messages = self._pull_messages(subscription_path, num_messages)

        messages_data = [self._get_message_data(msg) for msg in received_messages]
        messages_data = [self.messages_dec.decode(data) for data in messages_data]

        self._ack_messages(subscription_path, received_messages)
        return messages_data

    def push_messages(self, topic: str, messages: List[object]) -> int:
        """
        Encodes and publishes messages to a Pub/Sub topic
        :param topic: name of the Pub/Sub topic to publish to
        :param messages: list of message objects to publish
        :return: number of messages published
        """

        messages_data = [self.messages_enc.encode(msg) for msg in messages]

        topic_path = self._publisher_client.topic_path(self.project_id, topic)
        pushed_num = self._push_messages(topic_path, messages_data)

        return pushed_num
