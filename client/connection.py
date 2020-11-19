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
import string
import random
import pickle


class Client:
    msgLen = 16777216

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.hash = ""
    
    def Start(self):
        while True:
            msg = self.Receive()
            if msg["type"] == "init":
                self.hash = msg["hash"]
                print(self.hash)

    def Send(self, obj):
        data = pickle.dumps(obj)
        self.conn.send(data)

    def Receive(self):
        data = self.conn.recv(self.msgLen)
        return pickle.loads(data)