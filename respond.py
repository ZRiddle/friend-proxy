#
import logging
from model import learn
from cache import CACHE


def speak(sc, channel, target=''):
    if target[:2] == '<#':
        modelkey = target.split('|')[0][2:]
    elif target[:2] == '<@':
        modelkey = target
    else:
        modelkey = channel
    if modelkey not in CACHE:
        o = learn(sc, channel, target)
        model = CACHE[modelkey]
        return o + '; ' + model.make_short_sentence(140)
    else:
        model = CACHE[modelkey]
        return model.make_short_sentence(140)
