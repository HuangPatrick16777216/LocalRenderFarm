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


class RENDERFARM_PT_Main(Panel):
    bl_label = "Local Render Farm"
    bl_idname = "RENDERFARM_PT_Main"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        from .operators import status, conn
        settings = context.scene.local_render_farm
        layout = self.layout

        if status == "UNCONN":
            layout.prop(settings, "compType", expand=True)

        if settings.compType == "0":
            if status == "UNCONN":
                layout.label(text=f"Your local IP is {socket.gethostbyname(socket.gethostname())}")
                layout.operator("local_render_farm.start_server")

            elif status == "WAITING":
                layout.label(text="Waiting for clients.")
                layout.label(text=f"Your local IP is {socket.gethostbyname(socket.gethostname())}")
                #layout.prop(settings, "serverRender")
                layout.prop(settings, "outputDir")
                layout.operator("local_render_farm.start_render")
                layout.separator()

                if len(conn.clients) > 0:
                    layout.label(text="Connected clients:")
                    for c in conn.clients:
                        layout.label(text=f"  * {c.addr[0]}  {c.addr[1]}")

            elif status == "RENDERING":
                layout.label(text="Rendering has started.")
                
                layout.separator()
                layout.label(text="Client statuses:")

        else:
            if status == "UNCONN":
                layout.prop(settings, "serverIp")
                layout.operator("local_render_farm.connect")
            elif status == "WAITING":
                layout.label(text=f"Your local IP is {socket.gethostbyname(socket.gethostname())}")
                layout.label(text="Waiting for server to start...")
            elif status == "RENDERING":
                layout.label(text="Rendering")


classes = (
    RENDERFARM_PT_Main,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)