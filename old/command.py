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
import threading


def Render(clients, startFrame, endFrame, outDir):
    currFrame = startFrame
    while True:
        for c in clients:
            if currFrame > endFrame:
                return

            if not c.rendering:
                threading.Thread(target=RenderImage, args=(c, currFrame, outDir)).start()
                currFrame += 1


def RenderImage(client, frame, outDir):
    image = client.RenderFrame(frame)
    path = os.path.join(outDir, f"{frame}.jpg")
    with open(path, "wb") as file:
        file.write(image)