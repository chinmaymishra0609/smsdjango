from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import json
from .models import Group, Chat

class MyWebSocketConsumer(WebsocketConsumer):
    def connect(self):
        print(f"The Websocket has been connected successfully.")
        self.group_name = self.scope["url_route"]["kwargs"]["name_of_group"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def receive(self, text_data = None, bytes_data = None):
        print(f"The message has been received successfully.")
        data = json.loads(text_data)

        if self.scope["user"].is_authenticated:
            group = Group.objects.get(name = self.group_name)
            chat = Chat(content=data["message"], group=group)
            chat.save()
            data["user"] = self.scope["user"].username

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":json.dumps(data)
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":json.dumps({"message":"Login Required...", "user":"guest"})
                }
            )

    def chat_message(self, event):
        self.send(text_data=event["text"])

    def disconnect(self, code):
        print(f"The Websocket has been disconnected successfully.")
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

class MyAsyncWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"The Websocket has been connected successfully.")
        self.group_name = self.scope["url_route"]["kwargs"]["name_of_group"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data = None, bytes_data = None):
        print(f"The message has been received successfully.")
        data = json.loads(text_data)

        if self.scope["user"].is_authenticated:
            group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
            chat = Chat(content=data["message"], group=group)
            await database_sync_to_async(chat.save)()
            data["user"] = self.scope["user"].username

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":json.dumps(data)
                }
            )
        else:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":json.dumps({"message":"Login Required...", "user":"guest"})
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=event["text"])

    async def disconnect(self, code):
        print(f"The Websocket has been disconnected successfully.")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)