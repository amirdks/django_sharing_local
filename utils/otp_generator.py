import random


def otp_generator():
    return random.randint(0, 90000) + 10000
