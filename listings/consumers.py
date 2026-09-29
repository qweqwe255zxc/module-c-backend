from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ListingsConsumer(JsonWebsocketConsumer):
    groups = ['listings']

    def connect(self) -> None:
        self.accept()
        self.send_json({'type': 'hello'})

    def listing_new(self, event):
        self.send_json({
            'type': 'listing:new',
            'listing': event['listing'],
        })
