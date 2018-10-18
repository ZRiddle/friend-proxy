from slackclient import SlackClient
import logging
import os

max_messages = 5000


def get_user_messages(user_id):
    return


def get_messages(channel_id, user_id=None):
    sc = SlackClient(os.environ.get('slack_oauth'))
    results = []
    latest = ''
    while len(results) < max_messages:
        data = sc.api_call('channels.history', channel=channel_id, count=1000, latest=latest)
        if not data['ok']:
            logging.info('no results')
            return results

        messages = data['messages']
        logging.info('[get_messages] new messages count: {}'.format(len(messages)))
        if user_id:
            messages = [m for m in messages if m['user'] == user_id]
        for msg in messages:
            if msg['text']:
                cleaned = clean_message(msg['text'])
                results.append(cleaned)
            latest = msg['ts']
        if not data['has_more']:
            break
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
