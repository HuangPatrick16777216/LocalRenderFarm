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
from bpy.types import Panel


class RENDERSERVER_PT_Main(Panel):
    bl_label = "Local Render Farm - Server"
    bl_idname = "RENDERSERVER_PT_Main"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        from .operators import server
        layout = self.layout
        settings = context.scene.render_server

        if settings.status == "NOT_STARTED":
            layout.prop(settings, "ip")
            layout.operator("render_server.start")

        elif settings.status == "STARTED":
            row = layout.row(align=True)
            row.prop(settings, "frame_start")
            row.prop(settings, "frame_end")
            layout.prop(settings, "out_path")
            layout.operator("render_server.render")
            
            layout.label(text="Waiting for clients...")

            box = layout.box()
            num_clients = len(server.clients)
            num_text = f"{num_clients} client connected." if num_clients == 1 else f"{num_clients} clients connected."
            box.label(text=num_text)

            if num_clients > 0:
                col = box.column(align=True)
                for client in server.clients:
                    col.label(text=client.addr[0])

        elif settings.status == "RENDERING":
            layout.label(text="Rendering")
            layout.prop(settings, "hover", text="Hover to refresh.")
            box = layout.box()
            box.label(text="Client statuses:")

            col = box.column(align=True)
            for client in server.clients:
                col.label(text=f"{client.addr[0]}: {client.curr_frame}")


classes = (
    RENDERSERVER_PT_Main,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)