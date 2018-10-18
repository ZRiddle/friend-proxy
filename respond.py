#
import logging
from cache import CACHE


def speak(sc, channel, *args):
    model = CACHE[channel]
    return model.make_short_sentence(140)
