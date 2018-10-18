from slackclient import SlackClient
import logging
import os

max_messages = 5000


def get_messages(channel_id, user_id=None):
    results = []
    latest = ''
    while len(results) < max_messages:
        data = get_messages.sc.api_call('channels.history', channel=channel_id, count=1000, latest=latest)
        if not data['ok']:
            logging.info('no results')
            return results

        messages = [m for m in data['messages'] if 'subtype' not in m or m['subtype'] not in ['channel_join', 'channel_leave']]
        latest = data['messages'][-1]['ts']
        logging.info('[get_messages] new messages count in channel {}: {}'.format(channel_id, len(messages)))
        if user_id:
            messages = [m for m in messages if 'user' in m and m['user'] == user_id]
            logging.info('[get_messages] new messages for user {}: {}'.format(user_id, len(messages)))
        for msg in messages:
            if msg['text']:
                cleaned = clean_message(msg['text'])
                results.append(cleaned)
        if not data['has_more']:
            break
    return results


get_messages.sc = SlackClient(os.environ.get('slack_oauth'))


def clean_message(message):
    # Cleanup string and add a period to the end of every message
    msg = remove_urls(message)
    msg = msg.strip().lower()  # make everything lower
    if msg and not msg[-1] in ('!', '.', '?'):
        msg += '.'
    return msg


def remove_urls(msg):
    # This will remove links, and some of the @here and @person comments
    if msg.find("<@") >= 0 and msg.find(">") >= 0:
        # Recursively call this until there are no pairs of <@> left
        return remove_urls(msg[:msg.find("<@")] + 'someone' + msg[msg.find(">")+1:])
    elif msg.find("<") >= 0 and msg.find(">") >= 0:
        # Recursively call this until there are no pairs of <> left
        return remove_urls(msg[:msg.find("<")] + msg[msg.find(">")+1:])
    return msg
