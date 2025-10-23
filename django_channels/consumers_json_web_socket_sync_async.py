from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import json
from .models import Group, Chat

class MyJsonWebSocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        print(f"The Websocket has been connected successfully.")
        self.group_name = self.scope["url_route"]["kwargs"]["name_of_group"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def receive_json(self, content, **kwargs):
        print(f"The message has been received successfully.")

        if self.scope["user"].is_authenticated:
            group = Group.objects.get(name = self.group_name)
            chat = Chat(content=content["message"], group=group)
            chat.save()
            content["user"] = self.scope["user"].username

            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":content
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":{"message":"Login Required...", "user":"guest"}
                }
            )

    def chat_message(self, event):
        self.send_json(event["text"])

    def disconnect(self, close_code):
        print(f"The Websocket has been disconnected successfully.")
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

class MyJsonAsyncWebSocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print(f"The Websocket has been connected successfully.")
        self.group_name = self.scope["url_route"]["kwargs"]["name_of_group"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        print(f"The message has been received successfully.")

        if self.scope["user"].is_authenticated:
            group = await database_sync_to_async(Group.objects.get)(name = self.group_name)
            chat = Chat(content=content["message"], group=group)
            await database_sync_to_async(chat.save)()
            content["user"] = self.scope["user"].username

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":content
                }
            )
        else:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type":"chat.message",
                    "text":{"message":"Login Required...", "user":"guest"}
                }
            )

    async def chat_message(self, event):
        await self.send_json(event["text"])

    async def disconnect(self, code):
        print(f"The Websocket has been disconnected successfully.")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)