import pytest

from backend.utils import generate_text


@pytest.mark.parametrize("text_length", [0, 1, 10, 100, 1000])
def test_generate_text_ok(text_length):
    text = generate_text(text_length)

    assert len(text) == text_length
