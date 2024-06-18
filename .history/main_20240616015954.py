import pygame
import os
import random
import sys

WIDTH, HEIGHT = 1200, 700
FPS = 60

def load_background(folder_path, screen_width, screen_height):
    backgrounds = [] # Tạo danh sách rỗng để chứa tên các file hình ảnh
    for file_name in os.listdir(folder_path): # Duyệt qua tất cả các mục trong thư mục
        full_path = os.path.join(folder_path, file_name) # Tạo đường dẫn đầy đủ tới file
        if os.path.isfile(full_path): # Kiểm tra xem đây có phải là file không
             backgrounds.append(pygame.image.load(full_path)) # Nếu là file, thêm vào danh sách background
    
    bg = random.choice(backgrounds)# Chọn ngẫu nhiên một hình nền
    bg_width, bg_height = bg.get_size() # Lấy kích thước hình nền
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
    icon = pygame.image.load(r'assets/images/icon.png') # Lấy ảnh icon
    pygame.display.set_icon(icon) # Đặt ảnh icon cho cửa sổ
    cursor_img = pygame.image.load(r'assets/images/viewfinder.png').convert_alpha() # Tải hình ảnh con trỏ chuột
    cursor_img = pygame.transform.scale(cursor_img, (64, 64))
    pygame.mouse.set_visible(False) # Ẩn con trỏ

    bg, bg_x, bg_y = load_background(r'assets/images/backgrounds/', WIDTH, HEIGHT) # Gọi hàm load_random_background
    clock = pygame.time.Clock() # Đối tượng Clock để điều chỉnh tốc độ khung hình

    # Vòng lặp chính
    running = True
    while running:
        # Xử lý các sự kiện từ bàn phím, chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        SCREEN.blit(bg, (bg_x, bg_y)) # Vẽ hình nền lên màn hình

        # pos_mouse = pygame.mouse.get_pos() # Lấy vị trí hiện tại của con trỏ
        # SCREEN.blit(cursor_img, pos_mouse) # Vẽ ảnh ảnh lên vị trí con trỏ

        # Cập nhật tọa độ con trỏ
        cursor_x, cursor_y = pygame.mouse.get_pos()

        # Giới hạn vị trí của con trỏ trong khung hình
        cursor_x = max(0, min(cursor_x, WIDTH))
        cursor_y = max(0, min(cursor_y, HEIGHT))
        pygame.draw.circle(screen, (0, 0, 255), (cursor_x, cursor_y), 10)  # Vẽ con trỏ

        pygame.display.update() # Cập nhật màn hình
        # clock.tick(FPS)

    pygame.quit() # Dừng chương trình, giải phóng tài nguyên

if __name__ == "__main__":
    main()