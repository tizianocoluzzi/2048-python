import pygame
from constant import color
v = [[0, 2, 4, 8],[16, 32, 64, 128], [256, 512, 1024, 8], [0, 2, 2048, 8]]
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SPACING = 15

def draw():
    WIN.fill((200, 200, 200))
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(WIN, color[v[i][j]], [(WIDTH//4 * i + SPACING ,HEIGHT//4 * j + SPACING), (WIDTH//4 - 2*SPACING, HEIGHT//4 - 2*SPACING)])
    pygame.display.update()



def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw()
    pygame.quit()

if __name__ == '__main__':
    main()