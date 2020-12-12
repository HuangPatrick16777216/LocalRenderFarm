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
import atexit
import bpy
from bpy.types import Operator


class Server:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

        clients = []

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()


class RENDERSERVER_OT_Start(Operator):
    """Starts server"""
    bl_label = "Start Server"
    bl_description = "Starts server"
    bl_idname = "render_server.start"

    def execute(self, context):
        settings = context.scene.render_server
        return {"FINISHED"}


classes = (
    RENDERSERVER_OT_Start,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)