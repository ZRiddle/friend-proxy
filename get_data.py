
from slackclient import SlackClient
import markovify
import config

sc = SlackClient(config.slack_token)

# underwriting: C1K9R6F7U
# outage-management: C1KN6GBLH
# help_environment: C59D5D7A9
data = sc.api_call('channels.history', channel='C1K9R6F7U', count=1000)

messages = []
for msg in data['messages']:
    if msg['text']:
        messages.append(msg['text'])

model = markovify.Text(". ".join(messages), state_size=2)

print(model.make_sentence())
