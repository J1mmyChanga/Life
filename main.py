import pygame
from copy import deepcopy


pygame.init()
size = width, height = 1500, 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption('0_0')

running = True
fps = 6
clock = pygame.time.Clock()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * (width) for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 18

    def render(self, surface):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(surface, (255, 255, 255),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos[0], mouse_pos[1]
        if self.left <= x <= self.left + self.width * self.cell_size\
            and self.top <= y <= self.top + self.height * self.cell_size:
            res_x = (x - self.left) // self.cell_size
            res_y = (y - self.top) // self.cell_size
            return(res_x, res_y)
        else:
            return None


class Life(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.next_field = [[0 for i in range(width)] for j in range(height)]
        self.current_field = [[0 for i in range(width)] for j in range(height)]

    def next_move(self, current_field, x, y):
        count = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if current_field[j % self.height][i % self.width]:
                    count += 1
        if current_field[y][x]:
            count -= 1
            if count == 2 or count == 3:
                return 1
            return 0
        else:
            if count == 3:
                return 1
            return 0

    def create_cells(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.current_field[y][x]:
                    pygame.draw.rect(screen, pygame.Color('green'),
                                     (self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size,
                                      self.cell_size))
                self.next_field[y][x] = self.next_move(self.current_field, x, y)
        if go:
            self.current_field = deepcopy(self.next_field)
        self.render(screen)

board = Life(100, 100)
go = False
is_pressed = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not(go):
                    is_pressed = True
            elif event.button == 3:
                go = not(go)
            elif event.button == 4:
                fps += 1
            elif event.button == 5:
                fps -= 1
                if fps <= 0:
                    fps = 1
        if event.type == pygame.MOUSEBUTTONUP:
            is_pressed = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                go = not(go)
        while is_pressed:
            x, y = board.get_cell(event.pos)
            if not board.current_field[y][x]:
                board.current_field[y][x] = 1
            if not board.current_field[y][x - 1]:
                board.current_field[y][x - 1] = 1
            if not board.current_field[y][x + 1]:
                board.current_field[y][x + 1] = 1

            if not board.current_field[y + 1][x]:
                board.current_field[y + 1][x] = 1
            # if not board.current_field[y + 1][x - 1]:
            #     board.current_field[y + 1][x - 1] = 1
            # if not board.current_field[y + 1][x + 1]:
            #     board.current_field[y + 1][x + 1] = 1

            if not board.current_field[y - 1][x]:
                board.current_field[y - 1][x] = 1
            # if not board.current_field[y - 1][x - 1]:
            #     board.current_field[y - 1][x - 1] = 1
            # if not board.current_field[y - 1][x + 1]:
            #     board.current_field[y - 1][x + 1] = 1
            else:
                break
    screen.fill((0, 0, 0))
    board.create_cells(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()