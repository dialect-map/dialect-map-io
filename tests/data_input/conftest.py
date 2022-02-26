# -*- coding: utf-8 -*-

import os
import logging
import subprocess

import pytest

from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1 import SubscriberClient


PUBSUB_ADDRESS = "localhost:8085"
PUBSUB_PROJECT = "test-project"
PUBSUB_TOPIC = "test-topic"
PUBSUB_SUBS = "test-subscription"


@pytest.fixture(scope="class")
def pubsub_emulator():
    """
    Wraps the initialization of a local Pub/Sub emulator to use during the tests
    It is equivalent to the usage of unit-test 'setUpClass' and 'tearDownClass' methods.
    For more information about how to interact with the Pub/Sub emulator:
    https://cloud.google.com/pubsub/docs/emulator
    """

    logging.info("Starting Pub/Sub emulator")

    # Start the Pub/Sub emulator
    process = subprocess.Popen(
        args=["gcloud", "beta", "emulators", "pubsub", "start", f"--project={PUBSUB_PROJECT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Set up environment variables
    os.environ["PUBSUB_EMULATOR_HOST"] = PUBSUB_ADDRESS
    os.environ["PUBSUB_PROJECT_ID"] = PUBSUB_PROJECT

    # Create testing Pub/Sub topic
    publisher = PublisherClient()
    topic_path = publisher.topic_path(PUBSUB_PROJECT, PUBSUB_TOPIC)
    __________ = publisher.create_topic(name=topic_path)

    # Create testing Pub/Sub subscription
    subscriber = SubscriberClient()
    subs_path = subscriber.subscription_path(PUBSUB_PROJECT, PUBSUB_SUBS)
    _________ = subscriber.create_subscription(name=subs_path, topic=topic_path)

    try:
        yield
    except Exception as error:
        logging.error(f"Error occurred while testing Pub/Sub")
        logging.error(f"Error: {error}")
    finally:
        logging.info("Stopping Pub/Sub emulator")
        subscriber.delete_subscription(subscription=subs_path)
        publisher.delete_topic(topic=topic_path)
        process.terminate()
