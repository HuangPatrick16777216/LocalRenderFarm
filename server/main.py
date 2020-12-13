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
        self.frame = 0

    def draw(self, window, events):
        self.frame += 1
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

        if self.typing:
            cursor_x = self.font.render(self.text[:self.cursor_pos], 1, BLACK).get_width()
            pygame.draw.line(window, BLACK, (cursor_x, loc[1]+10), (cursor_x, loc[1]+size[1]-10))

        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if loc[0] <= mouse_pos[0] <= loc[0]+size[0] and loc[1] <= mouse_pos[1] <= loc[1]+size[1]:
                    self.typing = True
                else:
                    self.typing = False
            elif event.type == pygame.KEYDOWN and self.typing:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_TAB):
                    self.typing = False
                elif event.key == pygame.K_LEFT:
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    self.cursor_pos = max(len(self.text), self.cursor_pos + 1)
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                        self.cursor_pos -= 1
                elif event.key == pygame.K_DELETE:
                    if self.cursor_pos < len(self.text):
                        self.text = self.text[:self.cursor_pos+1] + self.text[self.cursor_pos+2:]
                else:
                    self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]


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