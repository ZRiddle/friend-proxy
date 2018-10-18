#
from cache import CACHE
import logging
import markovify
from get_channel_messages import get_messages


def build_model(messages, id, state_size=2):
    # Fit simple Markov Model - add period between
    logging.info("[build_model] " + id)
    model = markovify.Text(" ".join(messages), state_size=state_size)

    # Cache model
    CACHE[id] = model

    return model


def learn(sc, channel, *args):
    messages = get_messages(channel)
    _ = build_model(messages, channel)
    return 'Ingested {} new messages'.format(len(messages))
