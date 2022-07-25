# -*- coding: utf-8 -*-

import time

import pytest

from google.cloud.pubsub_v1 import PublisherClient
from src.dialect_map_gcp import PubSubQueueHandler

from .conftest import PUBSUB_PROJECT
from .conftest import PUBSUB_TOPIC
from .conftest import PUBSUB_SUBS


@pytest.mark.gcp
@pytest.mark.usefixtures("pubsub_emulator")
class TestPubSubHandler:
    """
    Class to group all the Pub/Sub handler tests

    Class attributes:
        SECS_BETWEEN_PULLS: number of seconds to wait between consecutive pulls.
            The number should be big enough to allow non-acknowledged messages
            to be available again on the next handler.pull_messages()
    """

    SECS_BETWEEN_PULLS = 10

    @pytest.fixture(scope="class")
    def handler(self):
        """
        Creates a Pub/Sub handler using testing values
        :return: initiated handler
        """

        return PubSubQueueHandler(
            project_id=PUBSUB_PROJECT,
            subscription=PUBSUB_SUBS,
            timeout_secs=2,
        )

    def test_read_messages(self, handler: PubSubQueueHandler):
        """
        Tests the correct reading of serialized messages from Pub/Sub
        Messages may include custom attributes, in the form of a dictionary
        :param handler: Pub/Sub handler
        """

        msg_data = b'{"field_1": "value_A", "field_2": "value_B"}'
        msg_meta = {"metadata_1": "value_A", "metadata_2": "value_B"}

        publisher = PublisherClient()
        topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)
        publisher.publish(topic=topic_path, data=msg_data, **msg_meta)

        messages = handler.get_messages(10)

        assert len(messages) == 1
        assert messages[0] == msg_data

    def test_read_valid_messages(self, handler: PubSubQueueHandler):
        """
        Tests the correct acknowledgement of valid messages
        :param handler: Pub/Sub handler
        """

        publisher = PublisherClient()
        topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)
        publisher.publish(topic=topic_path, data=b"{}")

        messages = handler.get_messages(10)
        assert len(messages) == 1

        # Enough time so that potential non-acknowledged messages
        # become available again upon subscriber.pull()
        time.sleep(self.SECS_BETWEEN_PULLS)

        messages = handler.get_messages(10)
        assert len(messages) == 0

    def test_read_invalid_messages(self, handler: PubSubQueueHandler):
        """
        Tests the non acknowledging of invalid messages
        :param handler: Pub/Sub handler
        """

        publisher = PublisherClient()
        topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)
        publisher.publish(topic=topic_path, data=b"()")

        pytest.raises(ValueError, handler.get_messages, 10)

        # Enough time so that non-acknowledged messages
        # become available again upon subscriber.pull()
        time.sleep(self.SECS_BETWEEN_PULLS)

        pytest.raises(ValueError, handler.get_messages, 10)
