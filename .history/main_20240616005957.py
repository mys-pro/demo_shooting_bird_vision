import pygame

# Khởi tạo pygame
pygame.init()
# Thiết lập kích thước cửa sổ
WIDTH, HEIGHT = 1200, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Title cửa sổ
pygame.display.set_caption("Shooting Bird")
# Tải hình nền
bg = pygame.image.load(r'assets/images/backgrounds/Cartoon_Forest_BG_01.png')
# Lấy kích thước hình nền
bg_width, bg_height = bg.get_size()
# Tính toán hệ số tỉ lệ
scale_factor = min(WIDTH / bg_width, HEIGHT / bg_height)
# Tính toán kích thước mới
new_width = int(bg_width * scale_factor)
new_height = int(bg_height * scale_factor)
# Thay đổi kích thước hình nền
bg = pygame.transform.scale(bg, (new_width, new_height))
# Tính toán vị trí để căn giữa hình nền
bg_x = (WIDTH - new_width) // 2
bg_y = (HEIGHT - new_height) // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    SCREEN.blit(bg, (0, 0))
    pygame.display.update()
pygame.quit()