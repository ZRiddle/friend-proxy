#
"""
Common Channdels
- underwriting: C1K9R6F7U
- outage-management: C1KN6GBLH
- help_environment: C59D5D7A9
"""
import logging
logging.basicConfig(level=logging.INFO)

from slackclient import SlackClient
from model import learn
from respond import speak, yell
import os
import time
import traceback
from cache import CACHE

_BOT_NAME_ = "friendbot"
_SCRABBLE_NAME_ = 'scrabblebot'


def ping(channel, *args):
    return 'pong'


def help_me(channel, *args):
    output = 'I can talk like:\n-  <#'
    # output += '>\n  <#'.join([CACHE['channels'][ch]['name'] for ch in CACHE.keys() if ch in CACHE['channels']])
    output += '>\n-  <#'.join([ch for ch in CACHE.keys() if ch in CACHE['channels']])
    output += '>'
    return output


def cache_channels(sc):
    data = sc.api_call('channels.list')
    channels = {}
    for ch in data['channels']:
        channels[ch['id']] = ch

    CACHE['channels'] = channels
    return


def main():
    """
    Startup logic and the main application loop to monitor Slack events.
    """
    logging.info("[main] Starting up bot!")

    # Create the bot instance
    sc = SlackClient(os.environ.get('slack_bot_oauth'))
    cache_channels(sc)

    # Connect to slack
    if not sc.rtm_connect():
        raise Exception("Couldn't connect to slack.")

    logging.info("[main] Bot is listening")
    commands = {
        'ping': ping,
        'speak': speak,
        'impersonate': None,
        'learn': learn,
        'help': help_me,
        'yell': yell
    }

    # Where the magic happens
    while True:
        # Examine latest events
        for slack_event in sc.rtm_read():

            # Disregard events that are not messages
            if not slack_event.get('type') == "message":
                continue

            message = slack_event.get("text")
            user = slack_event.get("user")
            channel = slack_event.get("channel")

            if not message or not user:
                continue

            if message.split()[0] in {_BOT_NAME_, _SCRABBLE_NAME_} and message.split()[1] in commands:
                logging.info("Command found: " + message)
                try:
                    text = commands[message.split()[1]](channel, *message.split()[2:])
                except TypeError:
                    text = 'incorrect number of arguments for command ' + message.split()[1]
                except Exception as e:
                    text = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                if text is not None:
                    if message.split()[0] == _SCRABBLE_NAME_:
                        text = ''.join([':scrabble-{}:'.format(x) if x in 'abcdefghijklmnopqrstuvwxyz' else x for x in text.lower()])
                    logging.info("Sending: " + text)
                    sc.rtm_send_message(channel, text)

        # Sleep for a second
        time.sleep(1)


if __name__ == '__main__':
    main()
