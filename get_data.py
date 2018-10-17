
from slackclient import SlackClient
import markovify
import config
import time

# underwriting: C1K9R6F7U
# outage-management: C1KN6GBLH
# help_environment: C59D5D7A9
channel_id = 'C1K9R6F7U'
days_of_messages = 100
today = time.time()

sc = SlackClient(config.slack_token)

data = [sc.api_call('channels.history', channel=channel_id, count=1000, oldest=(today - (x+1)*60*60*24), latest=(today - x*60*60*24)) for x in range(days_of_messages)]

messages = []

for day in data:
    for msg in day['messages']:
        if msg['text']:
            messages.append(msg['text'])

print('There are {} messages in the training data.'.format(str(len(messages))))
model = markovify.Text(". ".join(messages), state_size=2)
print(model.make_sentence())
