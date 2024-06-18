import pygame
import os
import random

WIDTH, HEIGHT = 1200, 700

def load_background(folder_path, screen_width, screen_height):
    # Tạo danh sách rỗng để chứa tên các file hình ảnh
    backgrounds = []
    # Duyệt qua tất cả các mục trong thư mục
    for file_name in os.listdir(folder_path):
        # Tạo đường dẫn đầy đủ tới file
        full_path = os.path.join(folder_path, file_name)
        # Kiểm tra xem đây có phải là file không
        if os.path.isfile(full_path):
            # Nếu là file, thêm vào danh sách background
             backgrounds.append(pygame.image.load(full_path))
    # Chọn ngẫu nhiên một hình nền
    bg = random.choice(backgrounds)
    # Lấy kích thước hình nền
    bg_width, bg_height = bg.get_size()
    scale_factor = max(screen_width / bg_width, screen_height / bg_height) # Tính toán hệ số tỉ lệ để bao phủ toàn bộ cửa sổ
    # Tính toán kích thước mới để bao phủ toàn bộ cửa sổ
    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)
    bg = pygame.transform.scale(bg, (new_width, new_height)) # Thay đổi kích thước hình nền
    # Tính toán vị trí để căn giữa hình nền
    bg_x = (screen_width - new_width) // 2
    bg_y = (screen_height - new_height) // 2
    return bg, bg_x, bg_y

def main():
    pygame.init() # Khởi tạo pygame
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # Tạo cửa sổ với kích thước WIDTH x HEIGHT
    pygame.display.set_caption("Shooting Bird") # Đặt tiêu đề cửa sổ
    bg, bg_x, bg_y = load_background(r'assets/images/backgrounds/', WIDTH, HEIGHT) # Gọi hàm load_random_background
    # Vòng lặp chính
    running = True
    while running:
        # Xử lý các sự kiện từ bàn phím, chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        SCREEN.blit(bg, (bg_x, bg_y)) # Vẽ hình nền lên màn hình
        pygame.display.update() # Cập nhật màn hình

    pygame.quit() # Dừng chương trình, giải phóng tài nguyên

if __name__ == "__main__":
    main()