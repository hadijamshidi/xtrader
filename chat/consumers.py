from channels import Group
from channels.sessions import channel_session
from .models import Room
import json
@channel_session
def ws_connect(message):
    # prefix, label = message['path'].strip('/').split('chat/')
    label = 'test'
    print(message)
    # room = Room.objects.get(label=label)
    # print(room.label)
    Group('chat-' + label).add(message.reply_channel)
    message.channel_session['room'] = label
    ws_send(message)
    print('connected')

@channel_session
def ws_receive(message):
    label = message.channel_session['room']
    room = Room.objects.get(label=label)
    data = json.loads(message['text'])
    m = room.messages.create(handle=data['handle'], message='yes')
    Group('chat-'+label).send({'text': json.dumps(m.as_dict())})
    # print('recieved')

@channel_session
def ws_disconnect(message):
    label = message.channel_session['room']
    print(label)
    Group('chat-'+label).discard(message.reply_channel)
    print('disconnected')


def ws_send(message):
    Group('chat-test').send({'text':{'m':15}})

def hadi():

    label = 'test6'
    room = Room.objects.get(label=label)
    # data = json.loads(message['text'])
    # m = room.messages.create(handle='handle', message='yes')
    m = {'handle': 'handle', 'message': 'self.message', 'timestamp': 'self.formatted_timestamp'}
    Group('chat-'+label).send({'text':json.dumps(m) })
                                   # json.dumps(m.as_dict())})
# from chat.consumers import hadi as h