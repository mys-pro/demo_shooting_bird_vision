import pygame
import os
import random

WIDTH, HEIGHT = 1200, 700

def load_background(folder_path, screen_width, screen_height):
    # Tạo danh sách rỗng để chứa tên các file hình ảnh
    background_files = []
    # Duyệt qua tất cả các mục trong thư mục
    for file_name in os.listdir(folder_path):
        # Tạo đường dẫn đầy đủ tới file
        full_path = os.path.join(folder_path, file_name)
        # Kiểm tra xem đây có phải là file không
        if os.path.isfile(full_path):
            # Nếu là file, thêm vào danh sách background_files
            background_files.append(file_name)
    # Tạo mảng chứa tất cả hình nền
    backgrounds = []
    for file_name in background_files:
        # Tạo đường dẫn đầy đủ tới file hình ảnh
        full_path = os.path.join(folder_path, file_name)
        # Tải hình ảnh và thêm vào mảng backgrounds
        backgrounds.append(pygame.image.load(full_path))
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

def main():
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Shooting Bird")

    # Gọi hàm load_random_background
    background_folder = r'assets/images/backgrounds/'
    bg, bg_x, bg_y = load_background(r'assets/images/backgrounds/', WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Vẽ hình nền lên màn hình
        SCREEN.blit(bg, (bg_x, bg_y))

        # Cập nhật màn hình
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()