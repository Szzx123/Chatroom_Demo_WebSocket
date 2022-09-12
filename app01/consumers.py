from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
CONN_LIST = []

# class ChatConsumer(WebsocketConsumer):
#     def websocket_connect(self, message):
#         #接受客户端连接 允许创建
#         print("创建连接")
#         self.accept()
#
#         CONN_LIST.append(self)
#
#     def websocket_receive(self, message):
#         # 浏览器基于websocket向后端发送数据，自动触发接收消息
#         text = message['text']
#         print("接收到消息", text)
#         # 给客户端发送消息
#         # if text == "close":
#         #     # 服务端主动断开，给客户端发送消息
#         #     self.close()
#         #     # raise StopConsumer() #它执行后，ws的切断不再执行
#         #     return
#
#         res = "{}...".format(text)
#         for conn in CONN_LIST:
#             conn.send(res)
#         # self.send(res)
#
#     def websocket_disconnect(self, message):
#         # 客户端与服务端断开时，自动触发
#         CONN_LIST.remove(self)
#         # print("客户端断开连接")
#         raise StopConsumer()


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        #接受客户端连接 允许创建
        self.accept()
        # 获取群号，获取路由匹配的group
        group = self.scope['url_route']['kwargs'].get("group")

        # 将客户端的连接对象加入（内存 or redis）
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        # 浏览器基于websocket向后端发送数据，自动触发接收消息
        group = self.scope['url_route']['kwargs'].get("group")
        text = message['text']
        print("接收到消息", text)
        # 给客户端发送消息
        # if text == "close":
        #     # 服务端主动断开，给客户端发送消息
        #     self.close()
        #     # raise StopConsumer() #它执行后，ws的切断不再执行
        #     return

        res = "{}...".format(text)
        # 通知组内所有的客户端，执行xxoo方法，在此方法中可以定义任意功能
        async_to_sync(self.channel_layer.group_send)(group, {"type": "xx.oo", 'message':message})

    def xx_oo(self, event):
            text = event['message']['text']
            self.send(text)

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("group")
        # 客户端与服务端断开时，自动触发
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        # print("客户端断开连接")
        raise StopConsumer()