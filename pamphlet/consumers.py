import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        #join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        print(text_data_json)
        if text_data_json['action']:
            action=text_data_json['action']
        else:
            action='send-message'
        
        if(action == 'new-offer') or (action=='new-anwser'):
            receive_dict = text_data_json

            print('receiver_channel_name is ',text_data_json['message']['receiver_channel_name'])
            receiver_channel_name = text_data_json['message']['receiver_channel_name']
            receive_dict['message']['receiver_channel_name'] = self.channel_name

            print('has_new_offer')
            async_to_sync(self.channel_layer.send)(
                receiver_channel_name,
                {
                    'type':receive_dict['type'],
                    'sender':self.scope['user'].username,
                    'message':receive_dict
                }
            )

            return
        if text_data_json['type'] =='send_sdp':
            print('new-peer')
            receive_dict = text_data_json

            receive_dict['message']['receiver_channel_name'] = self.channel_name
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {   
                    'type':receive_dict['type'],
                    'message':receive_dict
                }
            )

            return 
        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':text_data_json['type'],
                'sender':self.scope['user'].username,
                'message':message
            }
        )
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))
    
    # Receive message from room group
    def chat_message(self,event):
        message = event['message']
        sender = event['sender']
        if sender == self.scope['user'].username:
            message_direction= 'outgoing'
        else:
            message_direction= 'incoming'

        #send message to Websocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_direction':message_direction,
            'type':event['type'],
        }))
    # Receive message from room group
    def image_message(self,event):
        message = event['message']
        sender = event['sender']
        if sender == self.scope['user'].username:
            message_direction= 'outgoing'
        else:
            message_direction= 'incoming'

        #send message to Websocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_direction':message_direction,
            'type':event['type'],
        }))


    def send_sdp(self,event):
        receive_dict = event['message']
        receive_dict['type']='send_sdp'
        print('rec_dict',receive_dict)
        self.send(text_data=json.dumps(receive_dict))