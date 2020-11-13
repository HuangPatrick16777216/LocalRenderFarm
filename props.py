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
from bpy.types import PropertyGroup
from bpy.props import BoolProperty, IntProperty, FloatProperty, StringProperty, EnumProperty, PointerProperty


class RenderFarmProps(PropertyGroup):
    compType: EnumProperty(
        name="Type",
        description="Render server or render client.",
        items=[
            ("0", "Server", "You give the blend file and commands."),
            ("1", "Client", "You receive commands from the server.")
        ]
    )

    serverIp: StringProperty(
        name="Server IP",
        description="Local IP address of server computer."
    )

    serverRender: BoolProperty(
        name="Render on server?",
        description="Do rendering on server?",
        default=True
    )


def register():
    bpy.utils.register_class(RenderFarmProps)
    bpy.types.Scene.local_render_farm = PointerProperty(type=RenderFarmProps)

def unregister():
    bpy.utils.unregister_class(RenderFarmProps)
    del bpy.types.Scene.local_render_farm