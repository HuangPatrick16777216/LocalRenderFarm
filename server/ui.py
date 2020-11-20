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
import bpy
from bpy.types import Panel


class RENDERFARMSERVER_PT_Main(Panel):
    bl_label = "Local Render Farm - Server"
    bl_idname = "RENDERFARMSERVER_PT_Main"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        from .operators import status, server
        layout = self.layout
        settings = context.scene.local_render_farm_server

        if status == "NOT_STARTED":
            layout.label(text=f"Your local IP address is {socket.gethostbyname(socket.gethostname())}")
            layout.operator("local_render_farm_server.start_server")
        elif status == "STARTED":
            layout.operator("local_render_farm_server.start_render")
            layout.label(text=f"Your local IP address is {socket.gethostbyname(socket.gethostname())}")
            layout.label(text=f"{len(server.clients)} clients have connected.")
            layout.separator()
            layout.label(text="Connected clients:")
            for cli in server.clients:
                layout.label(text=f"  * {cli.addr[0]}")


classes = (
    RENDERFARMSERVER_PT_Main,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)