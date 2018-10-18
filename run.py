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
from respond import speak
import os
import time
import traceback
from cache import CACHE

_BOT_NAME_ = "friendbot"


def ping(sc, channel, *args):
    return 'pong'


def help_me(sc, channel, *args):
    output = 'Current channels\n  #'
    output += '\n  #'.join([CACHE['channels'][ch]['name'] for ch in CACHE.keys() if ch in CACHE['channels']])
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
        'help': help_me
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

            if message.split()[0] == _BOT_NAME_ and message.split()[1] in commands:
                logging.info("Command found: " + message)
                try:
                    text = commands[message.split()[1]](sc, channel, *message.split()[2:])
                except TypeError:
                    text = 'incorrect number of arguments for command ' + message.split()[1]
                except Exception as e:
                    text = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
                if text is not None:
                    logging.info("Sending: " + text)
                    sc.rtm_send_message(channel, text.upper())

        # Sleep for a second
        time.sleep(1)


if __name__ == '__main__':
    main()
