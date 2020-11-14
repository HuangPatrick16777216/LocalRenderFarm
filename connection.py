#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import os
import time
import socket
import threading
import pickle
import bpy

PARENT = os.path.dirname(__file__)

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

    def Start(self):
        threading.Thread(target=self.Accept, args=()).start()
        threading.Thread(target=self.Cleanup, args=()).start()

    def Accept(self):
        self.server.listen()
        while True:
            from .operators import active
            if not active:
                self.server.close()
                return

            conn, addr = self.server.accept()
            client = AcceptedClient(conn, addr)
            self.clients.append(client)

    def Cleanup(self):
        while True:
            from .operators import active
            if not active:
                return

            time.sleep(0.1)
            for i, c in enumerate(self.clients):
                if not c.active:
                    del self.clients[i]


class AcceptedClient:
    msgLen = 16777216

    def __init__(self, conn, addr):
        self.active = True
        self.conn = conn
        self.addr = addr

    def RenderFrame(self, frame):
        self.Send({"type": "render", "frame": frame})
        result = self.Receive()
        if result["type"] == "result":
            return result["img"]

    def Receive(self):
        data = self.conn.recv(self.msgLen)
        return pickle.loads(data)

    def Send(self, obj):
        data = pickle.dumps(obj)
        self.conn.send(data)


class Client:
    msgLen = 16777216

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

    def Start(self):
        while True:
            msg = self.Receive()
            
            from .operators import active
            if msg["type"] == "quit" or not active:
                self.conn.close()
                return

            elif msg["type"] == "render":
                bpy.context.scene.frame_current = msg["frame"]
                bpy.ops.render.render(use_viewport=True)
                bpy.data.images["Render Result"].save_render(filepath=os.path.join(PARENT, "tmp.jpg"))

                with open(os.path.join(PARENT, "tmp.jpg"), "rb") as img:
                    data = img.read()
                self.Send({"type": "result", "img": data})

    def Receive(self):
        data = self.conn.recv(self.msgLen)
        return pickle.loads(data)

    def Send(self, obj):
        data = pickle.dumps(obj)
        self.conn.send(data)