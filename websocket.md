# websocket

## 聊天室解决方案

<img src="/Users/shizhuzexuan/Library/Application Support/typora-user-images/image-20220911174852285.png" alt="image-20220911174852285" style="zoom:67%;" />

## websocket

- http协议 无状态&短连接
  - 客户端主动连接服务器
  - 客户端向服务器发送消息，服务端接收到返回数据
  - 客户端收到数据
  - 断开链接
  - 轮询和长轮询基于http实现
- https对数据进行加密
- Websocket 创建持久的连接不断开，基于这个连接进行收发数据【服务端给客户端主动推送消息】
  - web聊天室
  - 实时图表

### websocket原理

- http协议

  - 连接
  - 数据传输
  - 断开连接

- websocket 基于http建立

  - 连接 客户端发起

  - 握手 客户端发送一段消息，后端接收到消息再做一些特殊处理并返回，验证服务端支持websocket

    - 客户端向服务端发送

      <img src="/Users/shizhuzexuan/Library/Application Support/typora-user-images/image-20220911180713527.png" alt="image-20220911180713527" style="zoom:67%;" />

    - 服务端接收

      <img src="/Users/shizhuzexuan/Library/Application Support/typora-user-images/image-20220911181722853.png" alt="image-20220911181722853" style="zoom:67%;" />

  - 收发数据（加密）

    <img src="/Users/shizhuzexuan/Library/Application Support/typora-user-images/image-20220911182558393.png" alt="image-20220911182558393" style="zoom:67%;" />

    <img src="/Users/shizhuzexuan/Library/Application Support/typora-user-images/image-20220911182659890.png" alt="image-20220911182659890" style="zoom:67%;" />

    

  - 断开连接

### django使用websocket

- 新建项目

- 安装组件channels

  ```bash
  pip install channels
  ```

  

- app配置

  ```python
  INSTALLED_APPS = [
      "django.contrib.admin",
      "django.contrib.auth",
      "django.contrib.contenttypes",
      "django.contrib.sessions",
      "django.contrib.messages",
      "django.contrib.staticfiles",
      "channels",
  ]
  ```

- 添加配置

  ```python
  ASGI_APPLICATION = "django.channels.demo.routing.application"
  ASGI_APPLICATION = "djangoProject.asgi.application"
  ```

  引用的是asgi.py中的application方法

- 修改asgi文件

  ```python
  import os
  from django.core.asgi import get_asgi_application
  from channels.routing import ProtocolTypeRouter, URLRouter
  
  from . import routing
  
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject.settings")
  
  # application = get_asgi_application()
  
  application = ProtocolTypeRouter({
      "http": get_asgi_application(),
      "websocket": URLRouter(routing.websocket_urlpatterns),
  })
  ```

- 在settings的同级目录创建routing.py

  ```python
  from django.urls import re_path
  
  from app01 import consumers
  
  websocket_urlpatterns = [
      re_path(r'ws/(?P<group>\w+)/$', consumers.Chatconsumer.as_asgi()),
  ]
  ```

- 在app01目录下创建consumers.py，编写处理websocket的业务逻辑

  ```python
  from channels.generic.websocket import WebsocketConsumer
  from channels.exceptions import StopConsumer
  
  class ChatConsumer(WebsocketConsumer):
      def websocket_connect(self, message):
          #接受客户端连接 允许创建
          self.accept()
  
      def websocket_receive(self, message):
          # 浏览器基于websocket向后端发送数据，自动触发接收消息
          print(message)
          self.send("不要回复")
  
      def websocket_disconnect(self, message):
          # 客户端与服务端断开时，自动触发
          raise StopConsumer()
  ```

- django中的wsgi和asgi

  - wsgi 只支持同步

  - asgi wsgi+异步+websocket

  - http

    ```
    urls.py
    views.py
    ```

  - websocket

    ```
    routings.py
    consumers.py
    ```

    

### 聊天室

- 使用http访问聊天室页面

- 让客户端主动发起ws连接，服务端接收到连接后通过（握手）

  - 客户端 websocket

    ```javascript
    socket = new WebSocket("ws://127.0.0.1:8000/room/123/")
    ```

  - 服务端连接并握手

    ```python
    from channels.generic.websocket import WebsocketConsumer
    from channels.exceptions import StopConsumer
    
    class ChatConsumer(WebsocketConsumer):
        def websocket_connect(self, message):
            #接受客户端连接 允许创建
            print("创建连接")
            self.accept()
    ```

- 收发消息 - 客户端主动向服务端发消息

  - 客户端主动向服务端发消息

    ```html
    <div>
        <input type="text" placeholder="请输入" id="txt">
        <input type="button" value="发送" onclick="sendMessage()">
    </div>
    
    <script>
        socket = new WebSocket("ws://127.0.0.1:8000/room/123/");
    
        function sendMessage(){
            let tag = document.getElementById("txt");
            socket.send(tag.value);
        }
    </script>
    ```

  - 服务端

    ```python
    class ChatConsumer(WebsocketConsumer):
        def websocket_connect(self, message):
            #接受客户端连接 允许创建
            print("创建连接")
            self.accept()
    
        def websocket_receive(self, message):
            # 浏览器基于websocket向后端发送数据，自动触发接收消息
            text = message['text']
            print("接收到消息", text)
    ```

- 收发消息 - 服务端主动向客户端发消息

  - 客户端

    ```javascript
     function sendMessage(){
            let tag = document.getElementById("txt");
            socket.send(tag.value);
        }
    ```

  - 服务端

    ```python
    class ChatConsumer(WebsocketConsumer):
        def websocket_connect(self, message):
            #接受客户端连接 允许创建
            print("创建连接")
            self.accept()
    
        def websocket_receive(self, message):
            # 浏览器基于websocket向后端发送数据，自动触发接收消息
            text = message['text']
            print("接收到消息", text)
            # 给客户端发送消息
            self.send("来了")
    ```



### 群聊

- 前端

  ```html
  <div class="message" id="message"></div>
  <div>
      <input type="text" placeholder="请输入" id="txt">
      <input type="button" value="发送" onclick="sendMessage()">
      <input type="button" value="关闭连接" onclick="closeConn()">
  </div>
  
  <script>
      socket = new WebSocket("ws://127.0.0.1:8000/room/123/");
      {#当ws收到服务端的消息时，自动触发#}
      {#刚创建好连接后触发#}
      socket.onopen = function (event) {
          let tag = document.createElement("div");
          tag.innerText = "连接成功";
          document.getElementById("message").appendChild(tag);
      }
  
      socket.onmessage = function (event) {
          let tag = document.createElement("div");
          tag.innerText = event.data;
          document.getElementById("message").appendChild(tag);
      }
  
      function sendMessage(){
          let tag = document.getElementById("txt");
          socket.send(tag.value);
      }
  
      function closeConn(){
          socket.close();
      }
      {#服务端主动断开时触发#}
      socket.onclose = function (event) {
          let tag = document.createElement("div");
          tag.innerText = "服务端断开";
          document.getElementById("message").appendChild(tag);
      }
  
  </script>
  </body>
  ```

- 后端

  ```python
  from channels.generic.websocket import WebsocketConsumer
  from channels.exceptions import StopConsumer
  
  CONN_LIST = []
  
  class ChatConsumer(WebsocketConsumer):
      def websocket_connect(self, message):
          #接受客户端连接 允许创建
          print("创建连接")
          self.accept()
  
          CONN_LIST.append(self)
  
      def websocket_receive(self, message):
          # 浏览器基于websocket向后端发送数据，自动触发接收消息
          text = message['text']
          print("接收到消息", text)
          # 给客户端发送消息
          # if text == "close":
          #     # 服务端主动断开，给客户端发送消息
          #     self.close()
          #     # raise StopConsumer() #它执行后，ws的切断不再执行
          #     return
  
          res = "{}...".format(text)
          for conn in CONN_LIST:
              conn.send(res)
          # self.send(res)
  
      def websocket_disconnect(self, message):
          # 客户端与服务端断开时，自动触发
          CONN_LIST.remove(self)
          # print("客户端断开连接")
          raise StopConsumer()
  
  ```

  

### 群聊 chanel layers

- 在settings中配置

  ```python
  CHANNEL_LAYERS = {
    "default": {
      "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
  }
  ```

  

- consumers中的特殊代码

  - 前端

    ```html
    <script>
        socket = new WebSocket("ws://127.0.0.1:8000/room/{{ qq_group_num }}/");
        {#当ws收到服务端的消息时，自动触发#}
        {#刚创建好连接后触发#}
        socket.onopen = function (event) {
            let tag = document.createElement("div");
            tag.innerText = "连接成功";
            document.getElementById("message").appendChild(tag);
        }
    
        socket.onmessage = function (event) {
            let tag = document.createElement("div");
            tag.innerText = event.data;
            document.getElementById("message").appendChild(tag);
        }
    
        function sendMessage(){
            let tag = document.getElementById("txt");
            socket.send(tag.value);
        }
    
        function closeConn(){
            socket.close();
        }
        {#服务端主动断开时触发#}
        socket.onclose = function (event) {
            let tag = document.createElement("div");
            tag.innerText = "服务端断开";
            document.getElementById("message").appendChild(tag);
        }
    
    </script>
    </body>
    </html>
    ```

  - 后端

    ```python
    from channels.generic.websocket import WebsocketConsumer
    from channels.exceptions import StopConsumer
    from asgiref.sync import async_to_sync
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
    ```

    



