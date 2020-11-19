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


class RENDERFARMCLIENT_PT_Main(Panel):
    bl_label = "Local Render Farm - Client"
    bl_idname = "RENDERFARMCLIENT_PT_Main"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        from .operators import status, conn
        layout = self.layout
        settings = context.scene.local_render_farm_client

        if status == "NOT_CONNECTED":
            layout.prop(settings, "serverIp")
            layout.operator("local_render_farm_client.connect")
        elif status == "CONNECTED":
            layout.label(text="Waiting for server to begin rendering.")
            layout.label(text=f"Your hash is {conn.hash}")


classes = (
    RENDERFARMCLIENT_PT_Main,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)