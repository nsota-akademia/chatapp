import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Messages
import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_pk = int(self.scope["url_route"]["kwargs"]["my_pk"])
        pk = int(self.scope["url_route"]["kwargs"]["pk"])
        if my_pk > pk:
            my_pk=str(my_pk).ljust(8,'0')
            my_pk=int(my_pk)
            pk=str(pk).ljust(8,'0')
            pk=int(pk)
            self.room_name = str(my_pk * 100000000 + pk)
            self.room_group_name = "chat_%s" % self.room_name
        else:
            my_pk=str(my_pk).ljust(8,'0')
            my_pk=int(my_pk)
            pk=str(pk).ljust(8,'0')
            pk=int(pk)
            self.room_name = str(pk * 100000000 + my_pk)
            self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        myID = text_data_json["myID"]
        friendID = text_data_json["friendID"]
        myID = int(myID)
        friendID = int(friendID)
        await self.channel_layer.group_send(self.room_group_name, {"type" : "chat_message", "message" : message, "myID" : myID, "friendID" : friendID})

    @database_sync_to_async
    def save(self,message,myID,friendID):
        Messages.objects.create(
            message_from=myID,
            message_to=friendID,
            message=message,
        )

    async def chat_message(self, event):
        message = event["message"]
        myID = event["myID"]
        friendID = event["friendID"]
        await self.save(message,myID,friendID)
        await self.send(text_data=json.dumps({"message": message, "myID" : myID, "friendID" : friendID}))