# -*- coding: utf-8 -*-

import pytest
import time

from google.cloud.pubsub_v1 import PublisherClient
from src.dialect_map_gcp import PubSubReader

from .conftest import PUBSUB_PROJECT
from .conftest import PUBSUB_TOPIC
from .conftest import PUBSUB_SUBS


@pytest.mark.gcp
@pytest.mark.usefixtures("pubsub_emulator")
class TestPubSubReader:
    """
    Class to group all the Pub/Sub reader tests

    Class attributes:
        SECS_BETWEEN_PULLS: number of seconds to wait between consecutive pulls.
            The number should be big enough to allow non-acknowledged messages
            to be available again on the next reader.pull_messages()
    """

    SECS_BETWEEN_PULLS = 10

    @pytest.fixture(scope="class")
    def reader(self):
        """
        Creates a Pub/Sub reader using testing values
        :return: initiated reader
        """

        return PubSubReader(
            project_id=PUBSUB_PROJECT,
            subscription=PUBSUB_SUBS,
            timeout_secs=2,
        )

    def test_pull_messages(self, reader: PubSubReader):
        """
        Tests the correct pulling of serialized messages from Pub/Sub
        Messages may include custom attributes, in the form of a dictionary
        :param reader: Pub/Sub reader
        """

        msg_data = b'{"field_1": "value_A", "field_2": "value_B"}'
        msg_meta = {"metadata_1": "value_A", "metadata_2": "value_B"}

        publisher = PublisherClient()
        topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)
        publisher.publish(topic=topic_path, data=msg_data, **msg_meta)

        messages = reader.pull_messages(10)
        ________ = reader.ack_messages(messages)

        assert len(messages) == 1
        assert reader.get_message_data(messages[0]) == msg_data
        assert reader.get_message_metadata(messages[0]) == msg_meta

    def test_pull_no_messages(self, reader: PubSubReader):
        """
        Tests the correct handling of the no-more-messages scenario
        :param reader: Pub/Sub reader
        """

        messages = reader.pull_messages(10)
        ________ = reader.ack_messages(messages)

        assert len(messages) == 0

    def test_ack_messages(self, reader: PubSubReader):
        """
        Tests the correct acknowledgement of pulled messages
        :param reader: Pub/Sub reader
        """

        publisher = PublisherClient()
        topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)
        publisher.publish(topic=topic_path, data=b"{}")

        messages = reader.pull_messages(10)
        ________ = reader.ack_messages(messages)

        # Enough time so that potential non-acknowledged messages
        # become available again upon subscriber.pull()
        time.sleep(self.SECS_BETWEEN_PULLS)
        messages = reader.pull_messages(10)

        assert len(messages) == 0

    def test_no_ack_messages(self, reader: PubSubReader):
        """
        Tests the not-acknowledging default behaviour of the Pub/Sub reader
        :param reader: Pub/Sub reader
        """

        publisher = PublisherClient()
        topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)
        publisher.publish(topic=topic_path, data=b"{}")

        messages_1 = reader.pull_messages(10)

        # Enough time so that non-acknowledged messages
        # become available again upon subscriber.pull()
        time.sleep(self.SECS_BETWEEN_PULLS)
        messages_2 = reader.pull_messages(10)

        assert len(messages_1) == 1
        assert len(messages_2) == 1
