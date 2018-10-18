#
import logging
from cache import CACHE


def speak(sc, channel, target=''):
    if target[:2] == '<#':
        model = CACHE[target.split('|')[0][2:]]
    elif target[:2] == '<@':
        model = CACHE[target]
    else:
        model = CACHE[channel]
    return model.make_short_sentence(140)
