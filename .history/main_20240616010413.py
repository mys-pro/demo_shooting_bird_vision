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
def load_random_background(folder_path, screen_width, screen_height):
    # Lấy danh sách tất cả các file hình ảnh trong thư mục
    background_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Tạo mảng chứa tất cả hình nền
    backgrounds = [pygame.image.load(os.path.join(folder_path, f)) for f in background_files]

    # Chọn ngẫu nhiên một hình nền
    bg = random.choice(backgrounds)

    # Lấy kích thước hình nền
    bg_width, bg_height = bg.get_size()

    # Tính toán hệ số tỉ lệ để bao phủ toàn bộ cửa sổ
    scale_factor = max(screen_width / bg_width, screen_height / bg_height)

    # Tính toán kích thước mới để bao phủ toàn bộ cửa sổ
    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)

    # Thay đổi kích thước hình nền
    bg = pygame.transform.scale(bg, (new_width, new_height))

    # Tính toán vị trí để căn giữa hình nền
    bg_x = (screen_width - new_width) // 2
    bg_y = (screen_height - new_height) // 2

    return bg, bg_x, bg_y

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Vẽ hình nền lên màn hình
    SCREEN.blit(bg, (bg_x, bg_y))
    pygame.display.update()
pygame.quit()