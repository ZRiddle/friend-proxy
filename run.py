#
"""
Common Channdels
- underwriting: C1K9R6F7U
- outage-management: C1KN6GBLH
- help_environment: C59D5D7A9
"""
from slackclient import SlackClient
from model import learn
from respond import speak
import os
import time
import logging
from get_channel_messages import get_messages

_BOT_NAME_ = "friendbot"
logging.basicConfig(level=logging.INFO)

CACHE = {}  # Initialize model cache


def ping(sc, channel, *args):
    return 'pong'


def help_me(sc, channel, *args):
    return 'God helps those who help themselves.'


def main():
    """
    Startup logic and the main application loop to monitor Slack events.
    """
    logging.info("[main] Starting up bot!")

    # Create the bot instance
    sc = SlackClient(os.environ.get('slack_bot_oauth'))

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
                text = commands[message.split()[1]](sc, channel, *message.split()[2:])
                if text is not None:
                    sc.send_message(text)

        # Sleep for a second
        time.sleep(1)


if __name__ == '__main__':
    main()
