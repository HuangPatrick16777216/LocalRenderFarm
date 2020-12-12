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

import os
import bpy
import threading

currFrame = None


def Render(server, frameStart, frameEnd, outPath):
    global currFrame
    currFrame = frameStart

    for cli in server.clients:
        threading.Thread(target=Client, args=(cli, frameEnd, outPath)).start()


def Client(client, endFrame, outPath):
    global currFrame

    while True:
        if currFrame > endFrame:
            return

        print("Render frame: {}".format(currFrame))
        client.Send({"type": "render", "frame": currFrame})
        currFrame += 1

        msg = client.Receive()
        with open(os.path.join(outPath, "{}.jpg".format(msg["frame"])), "wb") as imgFile:
            imgFile.write(msg["image"])