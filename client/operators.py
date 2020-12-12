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
import bpy
from bpy.types import Operator

conn = None


class Conn:
    msg_len = 16777216

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        threading.Thread(target=self.start).start()

    def start(self):
        save_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "render.jpg")
        while True:
            msg = self.recv()
            if msg["type"] == "render":
                bpy.context.scene.frame_set(msg["frame"])
                bpy.ops.render.render()
                bpy.data.images.get("Render Result").save_render(save_path)
                with open(save_path, "rb") as file:
                    data = file.read()
                self.send({"type": "image", "image": data})

    def send(self, obj):
        self.conn.send(pickle.dumps(obj))

    def recv(self):
        return pickle.loads(self.conn.recv(self.msg_len))


class RENDERCLIENT_OT_Connect(Operator):
    """Connects to server."""
    bl_label = "Connect"
    bl_description = "Connects to server."
    bl_idname = "render_client.connect"

    def execute(self, context):
        global conn
        settings = context.scene.render_client
        
        conn = Conn(settings.ip, 5555)
        settings.status = "CONNECTED"
        
        return {"FINISHED"}


classes = (
    RENDERCLIENT_OT_Connect,
)

def register():
    global conn
    conn = None

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)