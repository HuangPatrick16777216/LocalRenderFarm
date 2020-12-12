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
import pickle
import time
import bpy
from bpy.types import Operator

server = None


def render(settings):
    global server
    frame = settings.frame_start

    while frame <= settings.frame_end:
        for client in server.clients:
            if not client.rendering:
                client.render(settings.out_path, frame)
                frame += 1
                break

        time.sleep(0.01)


class Server:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

        self.clients = []

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            self.clients.append(Client(conn, addr))


class Client:
    msg_len = 16777216

    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.rendering = False

    def render(self, path, frame):
        self.rendering = True
        self.send({"type": "render", "frame": frame})

        while True:
            msg = self.recv()
            if msg is not None and msg["type"] == "image":
                with open(os.path.join(path, f"{frame}.jpg"), "wb") as file:
                    file.write(msg["image"])
                break

        self.rendering = False

    def send(self, obj):
        self.conn.send(pickle.dumps(obj))

    def recv(self):
        try:
            return pickle.loads(self.conn.recv(self.msg_len))
        except:
            return None


class RENDERSERVER_OT_Start(Operator):
    """Starts server"""
    bl_label = "Start Server"
    bl_description = "Starts server"
    bl_idname = "render_server.start"

    def execute(self, context):
        global server
        settings = context.scene.render_server

        server = Server(settings.ip, 5555)
        threading.Thread(target=server.start).start()

        settings.status = "STARTED"
        return {"FINISHED"}


class RENDERSERVER_OT_Render(Operator):
    """Starts rendering."""
    bl_label = "Render"
    bl_description = "Starts rendering."
    bl_idname = "render_server.render"

    def execute(self, context):
        settings = context.scene.render_server
        threading.Thread(target=render, args=(settings,)).start()
        return {"FINISHED"}


classes = (
    RENDERSERVER_OT_Start,
    RENDERSERVER_OT_Render
)

def register():
    global server
    server = None

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)