import pygame

pygame.init()
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Bird")
bg = pygame.image.load(r'assets/images/backgrounds/Cartoon_Forest_BG_01.png')
# Lấy kích thước hình nền
bg_width, bg_height = bg.get_size()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    SCREEN.blit(bg, (0, 0))
    pygame.display.update()
pygame.quit()