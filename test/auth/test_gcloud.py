# -*- coding: utf-8 -*-

import pytest
from datetime import date
from datetime import datetime
from datetime import timedelta
from unittest.mock import patch

from src.auth.gcloud import OpenIDAuthenticator


def patched_init(self, key_path: str, target_url: str):
    """
    Substitutes the real OpenIDAuthenticator initialization
    :param self: fake self instance to store attributes
    :param key_path: fake path to the Service Account key
    :param target_url: fake URL authenticating against
    """

    time_mid_night = datetime.min.time()
    date_yesterday = date.today() - timedelta(days=1)
    date_yesterday = datetime.combine(date_yesterday, time_mid_night)

    self.credentials = type("PatchedCredentials", (object,), {"expiry": date_yesterday})


@pytest.fixture(scope="module")
def openid_auth() -> OpenIDAuthenticator:
    """
    Creates a dummy version of the OpenID Authenticator, without using any requests.
    :return: patched object
    """

    with patch.object(OpenIDAuthenticator, "__init__", new=patched_init):
        return OpenIDAuthenticator("", "")


def test_check_expiration(openid_auth: OpenIDAuthenticator):
    """
    Checks the correct validation of the credentials expiration date
    :param openid_auth: patched OpenID authenticator
    """

    assert openid_auth.check_expiration() is True
