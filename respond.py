#
import logging
from model import learn
from cache import CACHE

max_sentence_length = 200


def speak(channel, target='', target2=None):
    if target[:2] == '<#':
        modelkey = target.split('|')[0][2:]
    elif target[:2] == '<@':
        if target2:
            modelkey = (target, target2.split('|')[0][2:])
        else:
            modelkey = (target, channel)
    else:
        modelkey = channel
    if modelkey not in CACHE:
        o = learn(channel, target, target2)
        model = CACHE[modelkey]
        s = model.make_short_sentence(max_sentence_length, tries=100)
        if s is not None:
            return o + '\n\n' + s
        else:
            return o + '\n\n:robot_face: Beep Boop'
    else:
        model = CACHE[modelkey]
        s = model.make_short_sentence(max_sentence_length, tries=100)
        if s:
            return s
        return ':robot_face: Beep Boop'


def yell(channel, target='', target2=None):
    # AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
    return speak(channel, target, target2).upper()
