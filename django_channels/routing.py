# Import the path function to define URL routes in the application.
from django.urls import path
# Import the consumer module from the django_channels app to connect consumer with URL patterns.
from . import consumers_sync_async, consumers_web_socket_sync_async, consumers_json_web_socket_sync_async

# Define the list of URL patterns for user-related operations.
urlpatterns = [
    path("ws/sc/<str:name_of_group>/", consumers_sync_async.MySyncConsumer.as_asgi(), name="sync-consumer"),
    path("ws/ac/<str:name_of_group>/", consumers_sync_async.MyAsyncConsumer.as_asgi(), name="async-consumer"),

    path("ws/wssc/<str:name_of_group>/", consumers_web_socket_sync_async.MyWebSocketConsumer.as_asgi(), name="web-socket-sync-consumer"),
    path("ws/wsac/<str:name_of_group>/", consumers_web_socket_sync_async.MyAsyncWebSocketConsumer.as_asgi(), name="web-socket-async-consumer"),

    path("ws/jwssc/<str:name_of_group>/", consumers_json_web_socket_sync_async.MyJsonWebSocketConsumer.as_asgi(), name="json-web-socket-sync-consumer"),
    path("ws/jwsac/<str:name_of_group>/", consumers_json_web_socket_sync_async.MyJsonAsyncWebSocketConsumer.as_asgi(), name="json-web-socket-async-consumer"),
]