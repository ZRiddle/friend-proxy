#
"""
Common Channdels
- underwriting: C1K9R6F7U
- outage-management: C1KN6GBLH
- help_environment: C59D5D7A9
"""
from slackclient import SlackClient
import markovify
import os
import time
import logging

_BOT_NAME_ = "friendbot"
logging.basicConfig(level=logging.INFO)


def clean_message(message):
    # Cleanup string and add a period to the end of every message
    msg = remove_urls(message)
    msg = msg.strip().lower()  # make everything lower
    if msg and not msg[-1] in ('!', '.', '?'):
        msg += '.'
    return msg


def remove_urls(msg):
    # This will remove links, and some of the @here and @person comments
    if msg.find("<") >= 0 and msg.find(">") >= 0:
        # Recursively call this until there are no pairs of <> left
        return remove_urls(msg[:msg.find("<")] + msg[msg.find(">")+1:])
    return msg


def get_messages_from_channel(channel):
    """TODO - this function feels too messy"""
    logging.info("[get_messages_from_channel] - " + channel)
    sc = SlackClient(os.environ.get('slack_oauth'))

    days_of_messages = 30
    intervals_of_days = 30
    today = time.time()

    data = []
    for x in range(intervals_of_days):
        data.append(sc.api_call('channels.history', channel=channel, count=1000,
                                oldest=(today - (x + 1) * days_of_messages * 60 * 60 * 24),
                                latest=(today - x * days_of_messages * 60 * 60 * 24)))
        time.sleep(.2)

    messages = []
    for day in data:
        for msg in day['messages']:
            if msg['text']:
                messages.append(msg['text'])
    return messages


def build_model_from_channel(channel='C1K9R6F7U'):
    # Grab messages
    logging.info("[build_model_from_channel] - " + channel)
    messages = get_messages_from_channel(channel=channel)

    # Fit simple Markov Model - add period between
    cleaned_messages = [clean_message(msg) for msg in messages]
    model = markovify.Text(" ".join(cleaned_messages), state_size=2)

    return model


def main():
    """
    Startup logic and the main application loop to monitor Slack events.
    """
    print("Starting up bot!")
    logging.info("Starting up bot!")

    # Build model on channel
    model = build_model_from_channel()

    # Create the bot instance
    sc = SlackClient(os.environ.get('slack_bot_oauth'))

    # Connect to slack
    if not sc.rtm_connect():
        raise Exception("Couldn't connect to slack.")

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

            ######
            # Commands we're listening for.
            ######

            if _BOT_NAME_ + " ping" in message.lower():
                logging.info("[bot reply] - sending pong")
                sc.rtm_send_message(channel, "pong")

            if _BOT_NAME_ + " speak" in message.lower():
                logging.info("[bot reply] - generating message")
                sc.rtm_send_message(channel, model.make_short_sentence(140))

            if _BOT_NAME_ + " help" in message.lower():
                logging.info("[bot reply] - helping")
                sc.rtm_send_message(channel, "God helps those who help themselves")

        # Sleep for a second
        time.sleep(1)


if __name__ == '__main__':
    main()
