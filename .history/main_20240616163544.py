import pygame
import os
import random
import sys

# Khởi tạo pygame
pygame.init() 
pygame.display.set_caption("Shooting Bird")
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Xử lý ống ngắm
class viewFinder:
    def __init__ (self):
        pygame.event.set_grab(True) 
        pygame.mouse.set_visible(False)
        self.image = pygame.image.load('assets/images/viewfinder.png').convert_alpha()
        self.image_copy = self.image.copy()
        self.image_smaller = pygame.transform.scale(self.image_copy, (self.image_copy.get_width() // 2, self.image_copy.get_height() // 2))
        self.rect = self.image_smaller.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def follow_mouse(self):
        self.rect.center = pygame.mouse.get_pos()
    
    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.rect.center).topleft)

# Khởi tạo con chim
class birds:
    def __init__(self, x, y):
        self.images = []
        folder_path = 'assets/images/birds/bird1'
        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_path):
                self.images.append(pygame.image.load(full_path).convert_alpha())
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 5  # Tốc độ mặc định
        self.delay_count = 0
    
    def update(self):
        self.delay_count += 1
        
        # Kiểm tra nếu đã đủ thời gian chờ để cập nhật
        if self.delay_count >= 8:
            # Reset delay_count
            self.delay_count = 0
            
            # Cập nhật chỉ số hình ảnh để tạo hiệu ứng hoạt hình
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            
        # Di chuyển đối tượng sang phải
        self.rect.x += self.velocity
        
        # Kiểm tra nếu đối tượng đi ra khỏi màn hình, đặt lại vị trí
        if self.rect.left > SCREEN_WIDTH:
            self.reset()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Lấy background ngẫu nhiên
def get_background(folder_path, SCREEN_WIDTH, SCREEN_HEIGHT):
    backgrounds = []
    for file_name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file_name)
        if os.path.isfile(full_path):
             backgrounds.append(pygame.image.load(full_path).convert())
    
    bg = random.choice(backgrounds)
    bg_width, bg_height = bg.get_size()
    scale_factor = max(SCREEN_WIDTH / bg_width, SCREEN_HEIGHT / bg_height)

    new_width = int(bg_width * scale_factor)
    new_height = int(bg_height * scale_factor)
    bg = pygame.transform.scale(bg, (new_width, new_height))

    bg_x = (SCREEN_WIDTH - new_width) // 2
    bg_y = (SCREEN_HEIGHT - new_height) // 2
    return bg, bg_x, bg_y

explosion_group = pygame.sprite.Group()

# Vẽ hình ảnh
def draw(SCREEN, background, view_finder, bird):
    bg, bg_x, bg_y = background 
    SCREEN.blit(bg, (bg_x, bg_y))

    bird.update()
    # Vẽ đối tượng lên màn hình
    bird.draw(SCREEN)

    view_finder.follow_mouse()
    view_finder.draw(SCREEN)
    pygame.display.update()

def main(SCREEN):
    background = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT) # Gọi hàm get_background
    view_finder = viewFinder()
    b = bird(0, 100)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
    
        draw(SCREEN, background, view_finder, b)
        pygame.time.Clock().tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main(SCREEN)