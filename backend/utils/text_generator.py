import random
import string


def generate_text(length: int):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
