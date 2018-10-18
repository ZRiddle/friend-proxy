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
        s = model.make_short_sentence(140)
        if s is not None:
            return o + '\n' + s
        else:
            return o + '\nBeep Boop'
    else:
        model = CACHE[modelkey]
        s = model.make_short_sentence(140)
        if s:
            return s
        return 'Beep Boop'
