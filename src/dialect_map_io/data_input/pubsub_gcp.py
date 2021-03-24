# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from typing import List
from google.cloud.pubsub_v1 import SubscriberClient
from google.pubsub_v1.types import ReceivedMessage

from ..auth import BaseAuthenticator

logger = logging.getLogger()


class PubSubReader:
    """
    Class to read Pub/Sub messages synchronously
    Ref: https://cloud.google.com/pubsub/docs/pull#synchronous_pull
    """

    def __init__(self, project_id: str, subscription: str, auth_ctl: BaseAuthenticator):
        """
        Initializes the Pub/Sub reader
        :param project_id: GCP project ID where the subscription is located
        :param subscription: name of the Pub/Sub subscription to read from
        :param auth_ctl: authenticator controller
        """

        self.subscription = subscription
        self.pubsub_client = SubscriberClient(credentials=auth_ctl.credentials)
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
        :return: message publish time
        """

        return message.message.publish_time

    def close(self):
        """ Closes the Pubsub connection """

        logger.info("Disconnecting from PubSub")
        self.pubsub_client.close()

    def pull_messages(self, num_messages: int) -> List[ReceivedMessage]:
        """
        Pulls messages from the Pub/Sub subscription (without ACK)
        :param num_messages: maximum number of messages to pull
        :return: list of messages
        """

        response = self.pubsub_client.pull(
            subscription=self.messages_path,
            max_messages=num_messages,
        )

        messages = response.received_messages
        logger.info(f"Received {len(messages)} new messages")

        return messages

    def ack_messages(self, messages: List[ReceivedMessage]) -> int:
        """
        Acknowledges the received messages so they will not be sent again
        :param messages: list of received messages
        :return: number of messages acknowledged
        """

        ack_ids = []

        for message in messages:
            logger.info(f"Acknowledging ID: {message.ack_id}")
            ack_ids.append(message.ack_id)

        self.pubsub_client.acknowledge(
            subscription=self.messages_path,
            ack_ids=ack_ids,
        )

        return len(ack_ids)
