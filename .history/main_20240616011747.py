import pygame
import os
import random

WIDTH, HEIGHT = 1200, 700
FPS = 60

class Bird:
    def __init__(self, screen_width, screen_height):
        self.size = 30  # Kích thước hình vuông biểu diễn con chim
        self.x = screen_width + self.size  # Vị trí ban đầu ngoài phần màn hình bên phải
        self.y = random.randint(0, screen_height - self.size)  # Vị trí y ngẫu nhiên
        self.speed = random.randint(1, 3)  # Tốc độ di chuyển ngẫu nhiên
        self.is_active = True  # Trạng thái hoạt động của con chim

    def move(self):
        self.x -= self.speed  # Di chuyển con chim sang trái

    def is_offscreen(self, screen_width):
        return self.x + self.size < 0  # Kiểm tra xem con chim đã rời khỏi khung hình chưa

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
    bg, bg_x, bg_y = load_background(r'assets/images/backgrounds/', WIDTH, HEIGHT) # Gọi hàm load_random_background

    # Đối tượng Clock để điều chỉnh tốc độ khung hình
    clock = pygame.time.Clock()

    # Danh sách các con chim
    birds = []

    # Vòng lặp chính
    running = True
    while running:
        # Xử lý các sự kiện từ bàn phím, chuột
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        SCREEN.blit(bg, (bg_x, bg_y)) # Vẽ hình nền lên màn hình
        # Sinh ra con chim mới một cách ngẫu nhiên
        if random.random() < 0.02:  # Tỷ lệ để sinh ra chim mới, có thể điều chỉnh
            bird = Bird(screen_width, screen_height)
            birds.append(bird)

        # Xóa những con chim đã rời khỏi màn hình
        birds = [bird for bird in birds if not bird.is_offscreen(screen_width)]

        # Di chuyển và vẽ các con chim
        screen.fill(WHITE)  # Xóa màn hình với màu trắng
        for bird in birds:
            bird.move()  # Di chuyển con chim
            pygame.draw.rect(screen, (255, 0, 0), (bird.x, bird.y, bird.size, bird.size))  # Vẽ con chim
        pygame.display.update() # Cập nhật màn hình

    pygame.quit() # Dừng chương trình, giải phóng tài nguyên

if __name__ == "__main__":
    main()