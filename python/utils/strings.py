import string
import random


def random_string(n=10):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

