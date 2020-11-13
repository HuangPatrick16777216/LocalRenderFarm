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
from bpy.types import Operator
from bpy.props import BoolProperty
from .connection import Client, Server

status = None
conn = None
active = False


class RENDERFARM_OT_StartServer(Operator):
    bl_label = "Start Server"
    bl_description = "Start server and allow others to connect."
    bl_idname = "local_render_farm.start_server"

    def execute(self, context):
        global status, conn, active
        settings = context.scene.local_render_farm

        active = True
        conn = Server(socket.gethostbyname(socket.gethostname()), 5555)
        conn.Start()

        status = "WAITING"
        return {"FINISHED"}


class RENDERFARM_OT_StartRender(Operator):
    bl_label = "Start Rendering"
    bl_description = "Start rendering on all clients."
    bl_idname = "local_render_farm.start_render"

    popup: BoolProperty(
        name="Show popup warning?",
        description="Show user warning?",
        default=True
    )

    def execute(self, context):
        settings = context.scene.local_render_farm

        if not bpy.data.is_saved:
            self.report({"ERROR"}, "Blend file is not saved.")
            return {"CANCELLED"}
        if bpy.data.is_dirty:
            self.report({"ERROR"}, "Blend file is dirty (unsaved changes).")
            return {"CANCELLED"}

        if self.popup:
            bpy.ops.local_render_farm.start_render_popup("INVOKE_DEFAULT")
            return {"FINISHED"}

        global status, conn
        status = "RENDERING"

        return {"FINISHED"}


class RENDERFARM_OT_StartRenderPopup(Operator):
    bl_label = "Are you sure?"
    bl_description = "Are you sure you want to start rendering?"
    bl_idname = "local_render_farm.start_render_popup"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to start rendering?")

    def execute(self, context):
        bpy.ops.local_render_farm.start_render(popup=False)
        return {"FINISHED"}


class RENDERFARM_OT_Connect(Operator):
    bl_label = "Connect"
    bl_description = "Connect to server computer."
    bl_idname = "local_render_farm.connect"

    def execute(self, context):
        global status, conn, active
        settings = context.scene.local_render_farm

        active = True
        conn = Client(settings.serverIp, 5555)

        status = "WAITING"
        return {"FINISHED"}


classes = (
    RENDERFARM_OT_StartServer,
    RENDERFARM_OT_StartRender,
    RENDERFARM_OT_StartRenderPopup,
    RENDERFARM_OT_Connect,
)

def register():
    global status, conn, active
    status = "UNCONN"
    conn = None
    active = False

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    global active
    active = False
    
    for cls in classes:
        bpy.utils.unregister_class(cls)