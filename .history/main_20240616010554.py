import pygame
import os
import random

# Khởi tạo pygame
pygame.init()
# Thiết lập kích thước cửa sổ
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Title cửa sổ
pygame.display.set_caption("Shooting Bird")

background_folder = r'assets/images/backgrounds/'
bg, bg_x, bg_y = load_background(background_folder, WIDTH, HEIGHT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Vẽ hình nền lên màn hình
    SCREEN.blit(bg, (bg_x, bg_y))
    pygame.display.update()
pygame.quit()