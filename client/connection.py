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
import socket
import threading
import string
import random
import pickle
import bpy


class Client:
    msgLen = 16777216

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.hash = ""
        self.filePath = os.path.join(os.path.realpath(os.path.dirname(__file__)), self.hash+".jpg")
    
    def Start(self):
        while True:
            msg = self.Receive()
            if msg["type"] == "init":
                self.hash = msg["hash"]
                print(self.hash)

            elif msg["type"] == "render":
                bpy.context.scene.frame_set(msg["frame"])
                bpy.ops.render.render(use_viewport=True)
                bpy.data.images.get("Render Result").save_render(self.filePath)
                with open(self.filePath, "rb") as imgFile:
                    data = imgFile.read()
                self.Send({"type": "image", "frame": msg["frame"], "image": data})

    def Send(self, obj):
        data = pickle.dumps(obj)
        self.conn.send(data)

    def Receive(self):
        data = self.conn.recv(self.msgLen)
        return pickle.loads(data)