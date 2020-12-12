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

bl_info = {
    "name": "Local Render Farm - Client",
    "description": "Client side of local render farm",
    "author": "Patrick Huang",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "Properties >> Render >> Local Render Farm - Client",
    "warning": "",
    "doc_url": "https://github.com/HuangPatrick16777216/LocalRenderFarm",
    "tracker_url": "https://github.com/HuangPatrick16777216/LocalRenderFarm/issues",
    "category": "Render"
}

from . import props, operators, ui

modules = (
    props,
    operators,
    ui
)

def register():
    for mod in modules:
        mod.register()

def unregister():
    for mod in modules:
        mod.unregister()