from slackclient import SlackClient
import logging
import os


def get_messages(channel_id):
    sc = SlackClient(os.environ.get('slack_oauth'))
    data = sc.api_call('channels.history', channel=channel_id, count=1000)
    results = []
    if data['ok'] == 'False':
        logging.info('no results')
        return results
    for msg in data['messages']:
        if msg['text']:
            cleaned = clean_message(msg['text'])
            results.append(cleaned)
    return results


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
