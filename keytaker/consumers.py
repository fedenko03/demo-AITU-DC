from time import sleep

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from random import randint


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("Connected")

        for i in range(100):
            self.send(json.dumps({'message': randint(1, 1000)}))
            sleep(1)


class WSNewOrder(AsyncWebsocketConsumer):
    consumers = []

    async def connect(self):
        await self.accept()
        self.consumers.append(self)
        print("WebSocket connected")

    async def disconnect(self, close_code):
        self.consumers.remove(self)
        print("WebSocket disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            order_id = text_data_json['order_id']
            room_name = text_data_json['room_name']
            note = text_data_json['note']
            time = text_data_json['time']
            user_full_name = text_data_json['user_full_name']
            await self.send(text_data=json.dumps({
                'order_id': order_id,
                'room_name': room_name,
                'note': note,
                'time': time,
                'user_full_name': user_full_name
            }))


class WSCanceledOrder(AsyncWebsocketConsumer):
    consumers = []

    async def connect(self):
        await self.accept()
        self.consumers.append(self)
        print("WebSocket connected")

    async def disconnect(self, close_code):
        self.consumers.remove(self)
        print("WebSocket disconnected")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            msg_id = text_data_json['msg_id']
            msg = text_data_json['msg']
            await self.send(text_data=json.dumps({
                'msg_id': msg_id,
                'msg': msg
            }))
