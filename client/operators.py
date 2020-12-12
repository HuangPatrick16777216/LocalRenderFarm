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

import socket
import threading
import pickle
import bpy
from bpy.types import Operator

conn = None


class Conn:
    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

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