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

import pygame
import socket
import threading

pygame.init()
pygame.display.set_caption("Local Render Farm - Server")


class Button:
    def __init__(self, loc, size, text):
        self.loc = loc
        self.size = size
        self.text = text
        self.text_loc = (loc[0] + (size[0]-text.get_width()) // 2, loc[1] + (size[1]-text.get_height()) // 2)

    def draw(self, window, events):
        loc = self.loc
        size = self.size
        bg_col = (GRAY if self.clicked(events) else GRAY_LIGHT) if self.hovered() else WHITE

        pygame.draw.rect(window, bg_col, loc+size)
        pygame.draw.rect(window, BLACK, loc+size, 3)
        window.blit(self.text, self.text_loc)

    def clicked(self, events):
        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                break

        if click:
            mouse_pos = pygame.mouse.get_pos()
            loc = self.loc
            size = self.size
            if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
                return True

        return False
    
    def hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        loc = self.loc
        size = self.size
        if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
            return True
        return False


class TextInput:
    def __init__(self, loc, size, font, label, init_text=""):
        self.loc = loc
        self.size = size
        self.font = font
        self.label = font.render(label, 1, BLACK)
        self.text = init_text

        self.label_pos = (loc[0] + (size[0]-label.get_width()) // 2, loc[1] + (size[1]-label.get_height()) // 2)
        self.typing = False
        self.cursor_pos = 0

    def draw(self, window, events):
        loc = self.loc
        size = self.size

        pygame.draw.rect(window, WHITE, loc+size)
        pygame.draw.rect(window, BLACK, loc+size, 3)
        if not self.typing and self.text == "":
            window.blit(self.label, self.label_pos)
        else:
            text = self.font.render(self.text, 1, BLACK)
            text_pos = (loc[0] + (size[0]-text.get_width()) // 2, loc[1] + (size[1]-text.get_height()) // 2)
            window.blit(text, text_pos)


class Server:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))

        self.clients = []

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()


def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        WINDOW.fill(WHITE)


SCREEN = (1600, 900)
FPS = 60
WINDOW = pygame.display.set_mode(SCREEN)

BLACK = (0, 0, 0)
GRAY_DARK = (64, 64, 64)
GRAY = (128, 128, 128)
GRAY_LIGHT = (192, 192, 192)
WHITE = (255, 255, 255)

main()