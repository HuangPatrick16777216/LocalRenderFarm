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
import pickle


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

    def Start(self):
        threading.Thread(target=self.Accept, args=()).start()

    def Accept(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            client = AcceptedClient(conn, addr)
            threading.Thread(target=client, args=()).start()
            self.clients.append(client)

    def Cleanup(self):
        while True:
            for i, c in enumerate(self.clients):
                if not c.active:
                    del self.clients[i]


class AcceptedClient:
    msgLen = 1024

    def __init__(self, conn, addr):
        self.active = True
        self.conn = conn
        self.addr = addr

    def Start(self):
        while True:
            pass

    def Receive(self):
        data = self.conn.recv(self.msgLen)
        return pickle.loads(data)

    def Send(self, obj):
        data = pickle.dumps(obj)
        self.conn.send(data)


class Client:
    msgLen = 1024

    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))

    def Start(self):
        while True:
            msg = self.Receive()
            
            if msg["type"] == "quit":
                self.conn.close()
                return

            elif msg["type"] == "setmsglen":
                self.msgLen = msg["msglen"]

    def Receive(self):
        data = self.conn.recv(self.msgLen)
        return pickle.loads(data)

    def Send(self, obj):
        data = pickle.dumps(obj)
        self.conn.send(data)