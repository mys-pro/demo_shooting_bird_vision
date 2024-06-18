import pygame
import os
import random
import sys

pygame.init() # Khởi tạo pygame
pygame.display.set_caption("Shooting Bird") # Đặt tiêu đề cửa sổ
icon = pygame.image.load('assets/images/icon.png') # Lấy ảnh icon
pygame.display.set_icon(icon) # Đặt ảnh icon cho cửa sổ

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Tạo cửa sổ với kích thước WIDTH x HEIGHT

def get_background(folder_path, SCREEN_WIDTH, SCREEN_HEIGHT):
    backgrounds = [] # Tạo danh sách rỗng để chứa tên các file hình ảnh
    for file_name in os.listdir(folder_path): # Duyệt qua tất cả các mục trong thư mục
        full_path = os.path.join(folder_path, file_name) # Tạo đường dẫn đầy đủ tới file
        if os.path.isfile(full_path): # Kiểm tra xem đây có phải là file không
             backgrounds.append(pygame.image.load(full_path)) # Nếu là file, thêm vào danh sách background
    
    bg = random.choice(backgrounds)# Chọn ngẫu nhiên một hình nền
    bg_width, bg_height = bg.get_size() # Lấy kích thước hình nền
    scale_factor = max(SCREEN_WIDTH / bg_width, SCREEN_HEIGHT / bg_height) # Tính toán hệ số tỉ lệ để bao phủ toàn bộ cửa sổ

    # Tính toán kích thước mới để bao phủ toàn bộ cửa sổ
    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)
    bg = pygame.transform.scale(bg, (new_width, new_height)) # Thay đổi kích thước hình nền

    # Tính toán vị trí để căn giữa hình nền
    bg_x = (SCREEN_WIDTH - new_width) // 2
    bg_y = (SCREEN_HEIGHT - new_height) // 2
    return bg, bg_x, bg_y

def main(SCREEN):
    cursor_img = pygame.image.load('assets/images/viewfinder.png') # Tải hình ảnh kính ngắm
    cursor_img_width, cursor_img_height = cursor_img.get_size()
    pygame.event.set_grab(True) # Giữ con trỏ trong cửa sổ
    pygame.mouse.set_visible(False) # Ẩn con trỏ

    bg, bg_x, bg_y = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT) # Gọi hàm get_background
    # Vòng lặp chính
    running = True
    while running:
        # Xử lý các sự kiện từ bàn phím, chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False


        mouse_x, mouse_y = pygame.mouse.get_pos() # Lấy vị trí hiện tại của con trỏ
        SCREEN.blit(bg, (bg_x, bg_y)) # Vẽ hình nền lên màn hình
        SCREEN.blit(cursor_img, (mouse_x - (cursor_img_width // 2), mouse_y - (cursor_img_height // 2))) # Vẽ ảnh ảnh lên vị trí con trỏ
        pygame.display.update() # Cập nhật màn hình
        pygame.time.Clock().tick(FPS) # Điều chỉnh tốc độ khung hình

    pygame.quit() # Dừng chương trình, giải phóng tài nguyên

if __name__ == "__main__":
    main(SCREEN)