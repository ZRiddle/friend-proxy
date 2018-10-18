from slackclient import SlackClient


def get_messages(channel_id):
    token = '###'
    sc = SlackClient(token)
    data = sc.api_call('channels.history', channel=channel_id, count=1000)
    results = []
    if data['ok'] == 'False':
        print('no results')
        return results
    for msg in data['messages']:
        if msg['text']:
            results.append(msg['text'])
    return results
