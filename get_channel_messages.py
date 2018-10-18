from slackclient import SlackClient

def get_messages(channel_id):
	token = 'xoxp-4108165166-7989336820-456462137732-0030f362b7c66e7d9b44c2d7b2c85dbc'
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