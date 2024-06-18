import pygame
import os
import random
import time

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
        self.image_smaller = pygame.transform.scale(self.image_copy, (self.image_copy.get_width() // 3, self.image_copy.get_height() // 3))
        self.rect = self.image_smaller.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def follow_mouse(self):
        self.rect.center = pygame.mouse.get_pos()
    
    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.rect.center).topleft)

# Khởi tạo con chim
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, folder_name, speed, frame_rate):
        super().__init__()
        self.images = []
        folder_path = os.path.join('assets/images/birds', folder_name)
        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_path):
                self.images.append(pygame.image.load(full_path).convert_alpha())

        self.index = 0
        self.image = self.images[self.index]
        self.image_copy = self.image.copy()
        self.image_smaller = pygame.transform.scale(self.image_copy, (self.image_copy.get_width() // 2, self.image_copy.get_height() // 2))
        self.rect = self.image_smaller.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
        self.frame_rate = frame_rate
        self.frame_rate_count = 0
        self.direction = "right" if x < SCREEN_WIDTH // 2 else "left"
    
    def toRight(self):
        self.frame_rate_count += 1

        if self.frame_rate_count >= self.frame_rate:
            self.index += 1
            self.frame_rate_count = 0

        if self.index >= len(self.images) - 1:
            self.index = 0
        self.image = self.images[self.index]

        self.rect.x += self.speed
        if self.rect.x >= SCREEN_WIDTH + 100:
            self.kill()

    def toLeft(self):
        self.frame_rate_count += 1

        if self.frame_rate_count >= self.frame_rate:
            self.index += 1
            self.frame_rate_count = 0
        if self.index >= len(self.images) - 1:
            self.index = 0
        self.image = pygame.transform.flip(self.images[self.index], True, False)

        self.rect.x -= self.speed
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        if self.direction == "right":
            self.toRight()
        else:
            self.toLeft()

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=self.rect.center).topleft)

# Xử lý hiệu ứng nổ khi bắn trúng chim
class Explosions(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        folder_path = 'assets/images/smoke'
        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_path):
                image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (98, 98))
                self.images.append(image)
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosions_speed = 4
        self.counter += 1
        if self.counter >= explosions_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.counter >= explosions_speed:
            self.kill()

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

# Tạo chim
def create_bird(bird_list_folder, speed, frame_rate):
    folder_name = random.choice(bird_list_folder)
    bird_x = random.choice([-100, SCREEN_WIDTH + 100])
    bird_y = random.randrange(100, SCREEN_HEIGHT // 2, 30)
    return Bird(bird_x, bird_y, folder_name, speed, frame_rate)

# Lấy nhạc
def get_music(file_path, repeat, volume):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(repeat)
    pygame.mixer.music.set_volume(volume)

# Lấy âm thanh
def get_sound(file_path, volume):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    sound.play()

# Xử lý điểm
def score_display(screen, score, hight_score, game_font):
    score_surface = game_font.render('SCORE: ' + str(score), True, (255, 255, 255))
    screen.blit(score_surface, [20, 20])

def fire_bar(screen):
    bar_bg = pygame.Surface((200, 100), pygame.SRCALPHA)  # Surface với kênh alpha
    bar_bg.fill((255, 255, 255) + (120,))  # Tô màu với độ mờ alpha
    bar_bg_rect = bar_bg.get_rect(center(SCREEN_WIDTH // 2))
    screen.blit(rect, (100, 100))  # Vẽ hình chữ nhật lên màn hình

# Vẽ hình ảnh
def draw(SCREEN, background, view_finder, birds_group, explosion_group, score, hight_score, game_font):
    bg, bg_x, bg_y = background 
    SCREEN.blit(bg, (bg_x, bg_y))

    for bird in birds_group:
        bird.draw(SCREEN)
    birds_group.update()

    explosion_group.draw(SCREEN)
    explosion_group.update() 

    score_display(SCREEN, score, hight_score, game_font)

    view_finder.follow_mouse()
    view_finder.draw(SCREEN)
    pygame.display.update()

def main(SCREEN):
    get_music('assets/music/bgMusic.ogg', -1, 0.02)
    background = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT) # Gọi hàm get_background
    view_finder = viewFinder()
    bird_list_folder = ['bird1', 'bird2']
    spawnBird = pygame.USEREVENT
    pygame.time.set_timer(spawnBird, 1200)
    birds_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    Fire_rate = 100
    Cur_Fire_rate = 0
    game_font = pygame.font.Font('assets/fonts/digital-7.ttf', 40)
    score = 0
    hight_score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == spawnBird:
                new_bird = create_bird(bird_list_folder, 5, 8)
                birds_group.add(new_bird)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Cur_Fire_rate <= 0:
                get_sound('assets/sound/sniper.ogg', 0.02)
                for bird in birds_group:
                    if view_finder.rect.colliderect(bird.rect):
                        score += 1
                        bird.kill()
                        explosion = Explosions(bird.rect.x + bird.image_smaller.get_width() // 2, bird.rect.y + bird.image_smaller.get_height() // 2)
                        explosion_group.add(explosion)
                Cur_Fire_rate = Fire_rate

        Cur_Fire_rate -= 1
        if Fire_rate <= 0:
            Cur_Fire_rate = 0

        draw(SCREEN, background, view_finder, birds_group, explosion_group, score, hight_score, game_font)
        pygame.time.Clock().tick(FPS)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main(SCREEN)