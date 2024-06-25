from django.urls import re_path
from . import consumers

# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sender_username>[\w.@+-]+)/(?P<recipient_username>[\w.@+-]+)/$', consumers.WebRTCConsumer.as_asgi()),
]

