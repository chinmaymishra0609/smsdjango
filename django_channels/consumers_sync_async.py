from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import Group, Chat
import json

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print(f"The Websocket has been connected successfully.")
        self.group_name = self.scope["url_route"]["kwargs"]["name_of_group"]
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({"type": "websocket.accept"})

    def websocket_receive(self, event):
        print(f"The message has been received successfully.")
        data = json.loads(event["text"])

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
        self.send({
            "type":"websocket.send",
            "text":event["text"]
        })

    def websocket_disconnect(self, event):
        print(f"The Websocket has been disconnected successfully.")
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        raise StopConsumer()

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print(f"The Websocket has been connected successfully.")
        self.group_name = self.scope["url_route"]["kwargs"]["name_of_group"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        print(f"The message has been received successfully.")
        data = json.loads(event["text"])

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
        await self.send({
            "type":"websocket.send",
            "text":event["text"]
        })

    async def websocket_disconnect(self, event):
        print(f"The Websocket has been disconnected successfully.")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()