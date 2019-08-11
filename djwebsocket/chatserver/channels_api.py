from channels.layers import get_channel_layer
from .consumers import *
from django.http import JsonResponse
from asgiref.sync import async_to_sync

def send_user_push_alarm(request):
    if 'username' in request.GET:
        username = request.GET['username']
        channel_name = single_channels[username]
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.send)(
            channel_name,
            {
                'type': 'user_push_alarm_handler'
            }
        )

    return JsonResponse({"success": 'true'})

def send_admin_push_alarm(request):
    if 'content' in request.GET:
        content = request.GET['content']
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            'admin-alarm',
            {
                'type': 'admin_alarm_handler',
                'message': content
            }
        )

    return JsonResponse({"success": 'true'})