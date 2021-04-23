import random
import pygame
import os
from constant import color
pygame.font.init()

WIDTH, HEIGHT = 600, 600
FPS = 60
SPACING = 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WIN.fill(color['BG'])
font = pygame.font.SysFont('comicsans', 50)

class table:
    score = 0

    def __init__(self, n=4):
        # initialization of the matrix
        self.n = n
        self.v = [[] for _ in range(n)]
        for i in range(n):
            self.v[i] = [0 for _ in range(n)]

    def check_zeros(self):
        for i in range(len(self.v)):
            g = 0 in self.v[i]
            if g:
                return True
        return False

    def generation(self, q=1):
        a = random.randint(0, self.n - 1)
        b = random.randint(0, self.n - 1)
        if self.check_zeros():
            for _ in range(q):
                if self.v[a][b] == 0:
                    self.v[a][b] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
                else:
                    self.generation()

    def print_board(self):
        for i in range(self.n):
            for j in range(self.n):
                x = WIDTH // 4 * i + SPACING
                y = HEIGHT // 4 * j + SPACING
                w = WIDTH // 4 - 2 * SPACING
                h = HEIGHT // 4 - 2 * SPACING
                pygame.draw.rect(WIN, color[self.v[j][i]], [(x, y), (w, h)], border_radius=20)
                if not self.v[j][i] == 1:
                    text = font.render(f'{self.v[j][i]}', True, color['txt'])
                    placement = text.get_rect(center=(x + w / 2, y + h / 2))
                    WIN.blit(text, placement)
                pygame.display.update()

    def sum(self, vals):
        summed = []
        for i in range(len(vals)):
            summed.append([])
            j = 0
            while j < len(vals[i]):
                if j < len(vals[i]) - 1:
                    if vals[i][j] == vals[i][j + 1]:
                        summed[i].append(vals[i][j] * 2)
                        self.score += vals[i][j] * 2
                        j += 2  # incrementing j because the loop must jump the next number
                    else:
                        summed[i].append(vals[i][j])
                        j += 1
                elif len(vals[i]) - 1 == j:
                    summed[i].append(vals[i][j])
                    j += 1
        return summed

    def merge(self):
        # find values different from zero and store them in a vector
        vals = []
        for i in range(self.n):
            vals.append([])
            for j in range(self.n):
                if self.v[i][j] != 0:
                    vals[i].append(self.v[i][j])
        vals = self.sum(vals)
        n_vals = [[] for _ in range(self.n)]
        # initialize the new matrix with zeros
        for i in range(self.n):
            n_vals[i] = [0 for _ in range(self.n)]
        # adding summed value in new list
        for i in range(self.n):
            for j in range(len(vals[i])):
                n_vals[i][j] = vals[i][j]
        return n_vals

    @staticmethod
    def reverse(list):
        # reverse the rows of the matrix
        n_list = []
        for i in range(len(list)):
            n_list.append([])
            for j in range(len(list[i])):
                n_list[i].append(list[i][len(list[i]) - 1 - j])
        return n_list

    @staticmethod
    def column_rows(list):
        # change the rows with the columns
        n_list = [[] for _ in range(len(list))]
        for i in range(len(list)):
            n_list[i] = [0 for _ in range(len(list))]

        for i in range(len(list)):
            for j in range(len(list)):
                n_list[i][j] = list[j][i]
        return n_list

    def moveL(self):
        self.v = self.merge()

    def moveR(self):
        self.v = self.reverse(self.v)
        self.v = self.merge()
        self.v = self.reverse(self.v)

    def moveT(self):
        self.v = self.column_rows(self.v)
        self.v = self.merge()
        self.v = self.column_rows(self.v)

    def moveD(self):
        self.v = self.column_rows(self.v)
        self.v = self.reverse(self.v)
        self.v = self.merge()
        self.v = self.reverse(self.v)
        self.v = self.column_rows(self.v)

    def get_move(self, a):
        if a == 'w':
            self.moveT()
        if a == 's':
            self.moveD()
        if a == 'd':
            self.moveR()
        if a == 'a':
            self.moveL()
        if a == 'q':
            pygame.quit()

    @staticmethod
    def key_pressed():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'q'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    return 'w'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    return 's'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    return 'a'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    return 'd'
                else:
                    return None

    def lose(self):
        # scanning rows and column to see if there are possible moves
        for i in range(1, len(self.v)):
            for j in range(1, len(self.v[i])):
                if self.v[i][j] == self.v[i][j - 1] or self.v[i - 1][j] == self.v[i][j]:
                    return True
        return False


def main():
    t = table()
    t.generation(q=2)
    check = True
    clock = pygame.time.Clock()
    while check:
        clock.tick(FPS)
        t.print_board()
        pygame.display.flip()
        a = t.key_pressed()
        t.get_move(a)
        if not t.check_zeros():
            check = t.lose()
        else:
            check = True
        if a:
            t.generation()
    pygame.quit()


if __name__ == '__main__':
    main()
