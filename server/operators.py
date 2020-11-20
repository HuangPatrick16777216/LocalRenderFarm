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

import threading
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty
from .connection import Server
from .render import Render

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


class RENDERFARMSERVER_OT_StartRender(Operator):
    bl_label = "Start Render"
    bl_description = "Start rendering on all computers"
    bl_idname = "local_render_farm_server.start_render"

    showWarning: BoolProperty(default=True)

    def execute(self, context):
        global server, status
        settings = context.scene.local_render_farm_server

        if self.showWarning:
            bpy.ops.local_render_farm_server.start_render_warning("INVOKE_DEFAULT")
            return {"FINISHED"}

        status = "RENDERING"
        threading.Thread(target=Render, args=(server, context.scene.frame_start, context.scene.frame_end, settings.outPath)).start()
        
        return {"FINISHED"}


class RENDERFARMSERVER_OT_StartRenderWarning(Operator):
    bl_label = "Are you sure?"
    bl_description = "Are you sure you want to start the render?"
    bl_idname = "local_render_farm_server.start_render_warning"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to start the render?")

    def execute(self, context):
        bpy.ops.local_render_farm_server.start_render(showWarning=False)
        return {"FINISHED"}


classes = (
    RENDERFARMSERVER_OT_StartServer,
    RENDERFARMSERVER_OT_StartRender,
    RENDERFARMSERVER_OT_StartRenderWarning
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