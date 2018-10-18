#
from cache import CACHE
import logging
import markovify
from get_channel_messages import get_messages, get_user_messages


def build_model(messages, state_size=2):
    # Fit simple Markov Model - add period between
    logging.info("[build_model]")
    model = markovify.Text(" ".join(messages), state_size=state_size)

    return model


def learn(sc, channel, target='', target2=None):
    if target[:2] == '<#':
        messages = get_messages(target.split('|')[0][2:])
        CACHE[target.split('|')[0][2:]] = build_model(messages)
    elif target[:2] == '<@':
        if target2 is None:
            ch = channel
        else:
            ch = target2.split('|')[0][2:]
        messages = get_messages(ch, target[2:-1])
        CACHE[(target, ch)] = build_model(messages)
    else:
        messages = get_messages(channel)
        CACHE[channel] = build_model(messages)
    return 'Ingested {} new messages'.format(len(messages))
