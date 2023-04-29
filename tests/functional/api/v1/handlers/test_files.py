import http
from unittest import mock

from tests.helpers import dummy_side_effect


def test_send_file_ok(client):
    with mock.patch("flask.send_file", side_effect=dummy_side_effect) as send_file_mock:
        resource = client.get("/api/v1/file/testFile")

        send_file_mock.assert_called()
