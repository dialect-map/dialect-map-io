# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timezone

import pytest

from src.dialect_map_gcp.models import DiffMessage


def test_diff_message_default_init_error():
    """Checks the default creation of a Diff Message object"""

    init_args = {
        "container": [],
        "field_name": "example",
        "value_prev": None,
        "value_post": None,
        "source_file": "file.json",
        "created_at": datetime.now(timezone.utc),
    }

    assert pytest.raises(ValueError, DiffMessage, **init_args)


def test_diff_message_pubsub_init_success():
    """Checks the creation of a Diff Message object from a Pub/Sub message"""

    created = datetime.now(timezone.utc)
    message = {
        "container": {},
        "fieldName": "example",
        "valuePrev": 5,
        "valuePost": 10,
        "sourceFile": "file.json",
        "createdAt": created,
    }

    diff_msg = DiffMessage.from_pubsub(message)

    assert diff_msg.container == {}
    assert diff_msg.field_name == "example"
    assert diff_msg.value_prev == 5
    assert diff_msg.value_post == 10
    assert diff_msg.source_file == "file.json"
    assert diff_msg.created_at == created


def test_diff_message_pubsub_init_error():
    """Checks the creation of a Diff Message object from a Pub/Sub message"""

    message = {}
    assert pytest.raises(KeyError, DiffMessage.from_pubsub, message)
