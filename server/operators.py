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

import bpy
from bpy.types import Operator
from .connection import Server

server = None
status = None


class RENDERFARMSERVER_OT_StartServer(Operator):
    bl_label = "Start Server"
    bl_description = "Start server and allow clients to connect"
    bl_idname = "local_render_farm_server.start_server"

    def execute(self, context):
        global server, status
        server = Server()
        server.Start()
        status = "STARTED"

        return {"FINISHED"}


classes = (
    RENDERFARMSERVER_OT_StartServer,
)

def register():
    global server, status
    server = None
    status = "NOT_STARTED"

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)