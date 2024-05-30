import pygame

class Box:
    def __init__(self, x, y, BLOCK_SIZE):
        self.x = x
        self.y = y
        self.BLOCK_SIZE = BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, self.BLOCK_SIZE, self.BLOCK_SIZE)

    def move(self, dx, dy):
        print(dx)
        self.x += dx
        self.y += dy
        self.rect = pygame.Rect(self.x, self.y, self.BLOCK_SIZE, self.BLOCK_SIZE)

    def get_position(self):
        return [self.x // self.BLOCK_SIZE, self.y // self.BLOCK_SIZE]
