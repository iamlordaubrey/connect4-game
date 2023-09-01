from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


def add_to_room_event_producer(group_name, channel_name):
    channel_layer.group_add(group_name, channel_name)


def broadcast_event_producer(group_name, event_type, message='Broadcast message'):
    # channel_layer.group_send(group_name, {
    #     'type': event_type,
    #     'text': message,
    # })
    async_to_sync(channel_layer.group_send)(group_name, {
        'type': event_type,
        'text': message,
    })
