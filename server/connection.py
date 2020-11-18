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
import threading


class Server:
    ip = socket.gethostbyname(socket.gethostname())
    port = 5555
    msgLen = 16777216

    def __init__(self):
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))

    def Start(self):
        threading.Thread(target=self.Accept).start()
        threading.Thread(target=self.Cleanup).start()

    def Accept(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()

    def Cleanup(self):
        while True:
            for i, client in enumerate(self.clients):
                if not client.active:
                    del self.clients[i]