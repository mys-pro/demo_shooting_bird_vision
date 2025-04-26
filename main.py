import pygame
import os
import random
import mediapipe as mp
import sys
import cv2
import time

# Khởi tạo pygame
pygame.init() 
pygame.display.set_caption("Shooting Bird")
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class HandTracker():
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
        self.hand_position = None, None
        self.results = None
        self.hand_close = False
        self.hand_close_count = 0

    def scan_hands(self, image):       
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        self.results = self.hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.hand_close = False

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS)
                x, y = hand.landmark[9].x, hand.landmark[9].y
                self.hand_position = int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)
                x1, y1 = hand.landmark[12].x, hand.landmark[12].y

                if y1 > y:
                    self.hand_close = True
                    self.hand_close_count += 1
                else:
                    self.hand_close_count = 0
                    
        return image

    def get_position_hand(self):
        return self.hand_position

    def get_hand_close(self):
        return self.hand_close

    def get_hand_count(self):
        return self.hand_close_count

    def release(self):
        self.hands.close()

# Xử lý ống ngắm
class viewFinder():
    def __init__ (self):
        self.image = pygame.image.load('assets/images/viewfinder.png').convert_alpha()
        self.image_copy = self.image.copy()
        self.image_smaller = pygame.transform.scale(self.image_copy, (self.image_copy.get_width() // 2, self.image_copy.get_height() // 2))
        self.rect = self.image_smaller.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    def follow_mouse(self):
        self.rect.center = pygame.mouse.get_pos()

    def follow_mediapipe_hand(self, x, y):
        if x is not None and y is not None and x > 0 and x < SCREEN_WIDTH and y > 0 and y < SCREEN_HEIGHT:
            self.rect.center = (x, y)
    
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
    
    def toRight(self, pause):
        if pause == False:
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

    def toLeft(self, pause = False):
        if pause == False:
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

    def update(self, pause = False):
        if self.direction == "right":
            self.toRight(pause)
        else:
            self.toLeft(pause)

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
        explosions_speed = 2
        self.counter += 1
        if self.counter >= explosions_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.counter >= explosions_speed:
            self.kill()

# Xử lý game
class Game():
    def __init__(self, screen):
        self.screen = screen
        self.ui = UI(self.screen)
        self.background = self.ui.get_background('assets/images/backgrounds', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.volume = 1
        if self.ui.music:
            self.ui.play_music(-1, self.volume)

        self.cap = cv2.VideoCapture(0)
        self.bird_list_folder = ['bird1', 'bird2']
        self.birds_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        
        self.shoot = False
        self.spawn_time = 2
        self.spawn_time_start = time.time()
        self.fire_time = 1.7
        self.fire_cur_time = 0
        self.fire_bar_percent = 100
        self.time = 31
        self.time_start = time.time()
        self.time_cur = time.time()

        self.file_path = 'hight_score.txt'
        with open(self.file_path, 'r') as file:
            line = file.readline().strip()
            self.hight_score = int(line.split(': ')[1])

        self.score = 0
        self.game_page = "home"
        self.pause = False
        self.sound_game_over = False

    def load_camera(self):
        _, self.frame = self.cap.read()

    def reset(self):
        self.background = self.ui.get_background('assets/images/backgrounds', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view_finder = viewFinder()
        self.hand_tracking = HandTracker()
        self.birds_group.empty()
        self.explosion_group.empty()
        self.score = 0
        self.fire_bar_percent = 100
        self.time_start = time.time()

    def spawn_bird(self, speed, frame_rate):
        if not self.pause and time.time() - self.spawn_time_start >= self.spawn_time:
            bird_list_folder = ['bird1', 'bird2']
            folder_name = random.choice(bird_list_folder)
            bird_x = random.choice([-100, SCREEN_WIDTH + 100])
            bird_y = random.randrange(100, SCREEN_HEIGHT // 2, 30)
            new_bird = Bird(bird_x, bird_y, folder_name, speed, frame_rate)
            self.birds_group.add(new_bird)
            self.spawn_time_start = time.time()

    def getTime(self, time_set):
        if not self.pause and time_set > 0:
            self.time_cur = time_set - (time.time() - self.time_start)
        elif self.pause:
            self.time_start = time.time() - (time_set - self.time_cur)
        return int(self.time_cur)

    def event(self):
        self.shoot = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if self.game_page == "game_play" and self.hand_tracking.get_hand_close() and self.hand_tracking.get_hand_count() == 1:
            self.shoot = True

        if not self.pause:
            self.shooting()

    def shooting(self):
        if self.shoot and (self.fire_cur_time == 0 or (time.time() - self.fire_cur_time >= self.fire_time)):
            self.ui.play_sound(self.volume)
            self.fire_bar_percent = 0
            for bird in self.birds_group:
                if self.view_finder.rect.colliderect(bird.rect):
                    self.score += 1
                    bird.kill()
                    explosion = Explosions(bird.rect.x + bird.image_smaller.get_width() // 2, bird.rect.y + bird.image_smaller.get_height() // 2)
                    self.explosion_group.add(explosion)
            self.fire_cur_time = time.time()

    def set_view_finder_position(self):
        self.frame = self.hand_tracking.scan_hands(self.frame)
        if self.game_page == "game_play" and not self.pause:
            x, y = self.hand_tracking.get_position_hand()
            self.view_finder.follow_mediapipe_hand(x, y)
            self.view_finder.draw(self.screen)

    def home(self):
        if self.game_page == "home" and self.ui.get_play_button():
            self.game_page = "game_play"
            self.reset()

    def game_play(self):
        for bird in self.birds_group:
            bird.draw(self.screen)

        self.birds_group.update(self.pause)
        self.explosion_group.draw(self.screen)
        self.explosion_group.update()

        self.ui.score_display(self.score)
        if self.fire_bar_percent < 100:
            self.fire_bar_percent += 4
        self.ui.fire_bar(self.fire_bar_percent)

        time_set = self.getTime(self.time)
        self.ui.time_display(time_set)

        if(time_set <= 0):
            self.game_page = "game_over"
            self.sound_game_over = True

        if self.ui.get_pause_button():
            self.pause = True

        if self.pause and self.ui.get_start_button():
            self.pause = False

    def game_over(self):
        if self.sound_game_over:
            self.ui.game_over_sound(0.08)
            self.sound_game_over = False
        if self.score > self.hight_score:
            self.hight_score = self.score
            with open(self.file_path, 'w') as file:
                file.write(f'hight_score: {self.hight_score}\n')
        self.ui.game_over_display(self.hight_score, self.score)

        if self.ui.reset:
            self.reset()
            self.game_page = "game_play"

    def draw(self):
        bg, bg_x, bg_y = self.background 
        self.screen.blit(bg, (bg_x, bg_y))

        if self.game_page == "home":
            self.home()
        elif self.game_page == "game_play":
            self.game_play()
        elif self.game_page == "game_over":
            self.game_over()

        self.ui.get_music_button()
        self.ui.get_sound_button()
        self.set_view_finder_position()
    
    def update(self):
        self.load_camera()
        self.spawn_bird(8, 8)
        self.draw()
        self.event()
        cv2.imshow("Frame", self.frame)
        cv2.waitKey(1)

class UI():
    def __init__(self, screen):
        self.screen = screen
        
        self.sounds = {}
        self.sounds["music"] = pygame.mixer.music
        self.sounds["music"].load('assets/music/bgMusic.ogg')
        self.sounds["shoot"] = pygame.mixer.Sound('assets/sound/sniper.ogg')
        self.sounds["click"] = pygame.mixer.Sound('assets/sound/tap-notification-180637.mp3')
        self.sounds["game_over"] = pygame.mixer.Sound('assets/sound/lose.ogg')
        self.mouse_left_click = False

        play_image = pygame.image.load("assets/images/buttons/play_button.png").convert_alpha()
        start_image = pygame.image.load("assets/images/buttons/start_button.png").convert_alpha()
        pause_image = pygame.image.load("assets/images/buttons/pause_button.png").convert_alpha()
        reset_image = pygame.image.load("assets/images/buttons/reset_button.png").convert_alpha()
        self.music_image = pygame.image.load("assets/images/buttons/music_button_on.png").convert_alpha()
        self.sound_image = pygame.image.load("assets/images/buttons/sound_on.png").convert_alpha()

        self.play_button = Button(self.screen, play_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0.5)
        self.start_button = Button(self.screen, start_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0.3)
        self.pause_button = Button(self.screen, pause_image, SCREEN_WIDTH - 40, 40, 0.3)
        self.reset_button = Button(self.screen, reset_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, 0.4)
        self.music_button = Button(self.screen, self.music_image, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, 0.3)
        self.sound_button = Button(self.screen, self.sound_image, SCREEN_WIDTH - 110, SCREEN_HEIGHT - 40, 0.3)


        self.reset = False
        self.music = True
        self.sound = True
        self.file_path = 'setting.txt'
        self.volume = 1
        with open(self.file_path, 'r') as file:
            for line in file:
                if 'music:' in line:
                    self.music = line.split(': ')[1].strip().lower() == 'true'
                elif 'sound:' in line:
                    self.sound = line.split(': ')[1].strip().lower() == 'true'
        self.repeat = 0
    
    def get_image(self, image, scale):
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        return image

    def play_music(self, repeat, volume):
        self.repeat = repeat
        self.sounds["music"].set_volume(volume)
        self.sounds["music"].play(repeat)

    def play_sound(self, volume):
        self.sounds["shoot"].set_volume(volume)
        if self.sound:
            self.sounds["shoot"].play()

    def click_sound(self, volume):
        self.sounds["click"].set_volume(volume)
        if self.sound:
            self.sounds["click"].play()

    def game_over_sound(self, volume):
        self.sounds["game_over"].set_volume(volume)
        if self.sound:
            self.sounds["game_over"].play()

    # Lấy background ngẫu nhiên
    def get_background(self, folder_path, SCREEN_WIDTH, SCREEN_HEIGHT):
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

    # Xử lý điểm
    def score_display(self, score):
        font = pygame.font.Font('assets/fonts/digital-7.ttf', 30)
        bird_icon = self.get_image(pygame.image.load('assets/images/birds/bird1/b-1.png'), 0.6)
        bird_icon = pygame.transform.flip(bird_icon, True, False)
        score_surface = font.render("X" + str(score), True, (255, 255, 255))
        self.screen.blit(bird_icon, [20, 10])
        self.screen.blit(score_surface, [75, 22])
    
    def get_pause_button(self):
        if self.pause_button.draw():
            self.click_sound(self.volume)
            return True
        return False
    
    def get_start_button(self):
        if self.start_button.draw():
            self.click_sound(self.volume)
            return True
        return False
    
    def get_play_button(self):
        if self.play_button.draw():
            self.click_sound(self.volume)
            return True
        return False

    def get_music_button(self):
        if self.music_button.draw():
            self.music = not self.music
            with open(self.file_path, 'w') as file:
                file.write(f'music: {"True" if self.music else "False"}\n')
                file.write(f'sound: {"True" if self.sound else "False"}\n')
        
        if self.music:
            if not self.sounds["music"].get_busy():
                self.sounds["music"].play(self.repeat)
            self.music_image = self.get_image(pygame.image.load("assets/images/buttons/music_button_on.png").convert_alpha(), 0.3)
            self.music_button.image = self.music_image
        else:
            self.sounds["music"].stop()
            self.music_image = self.get_image(pygame.image.load("assets/images/buttons/music_button_off.png").convert_alpha(), 0.3)
            self.music_button.image = self.music_image

    def get_sound_button(self):
        if self.sound_button.draw():
            self.sound = not self.sound
            with open(self.file_path, 'w') as file:
                file.write(f'music: {"True" if self.music else "False"}\n')
                file.write(f'sound: {"True" if self.sound else "False"}\n')
        
        if self.sound:
            self.sound_image = self.get_image(pygame.image.load("assets/images/buttons/sound_on.png").convert_alpha(), 0.3)
            self.sound_button.image = self.sound_image
        else:
            self.sound_image = self.get_image(pygame.image.load("assets/images/buttons/sound_off.png").convert_alpha(), 0.3)
            self.sound_button.image = self.sound_image
    
    # Xử lý thanh nạp đạn
    def fire_bar(self, percent):
        font = pygame.font.Font('assets/fonts/digital-7.ttf', 30)
        width, height = 400, 30
        x = SCREEN_WIDTH // 2 - width // 2 + 10
        y = SCREEN_HEIGHT - 20 - height

        pygame.draw.rect(self.screen, (255, 255, 255), ((x, y), (width, height)), 2)

        bar = pygame.Surface((width * (percent / 100) - 10, height - 10))
        bar.fill((255,255,255)) 

        text = font.render('FIRE RATE', True, (255, 255, 255))

        self.screen.blit(text, [x - 120, y + 3])
        self.screen.blit(bar, [x + 5, y + 5])

    # Xủ lý hiển thị thơi gian
    def time_display(self, time):
        M = '00'
        S = '00'

        if time >= 60:
            m_f = str(time // 60)
            if m_f < 10:
                M = '0' + m_f
            else:
                M = m_f
        else:
            if time < 10:
                S = '0' + str(time)
            else:
                S = str(time)
        
        font = pygame.font.Font('assets/fonts/digital-7.ttf', 30)
        time_surface = font.render(M + ":" + S, True, (255, 255, 255))
        self.screen.blit(time_surface, [820, SCREEN_HEIGHT - 48])

    def game_over_display(self, hight_score, score):
        game_over_img = pygame.image.load('assets/images/game_over.png').convert_alpha()
        game_over_rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        font = pygame.font.Font('assets/fonts/Baloo-Regular.ttf', 30)
        score_surface = font.render('SCORE: ' + str(score), True, (97,62,92))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        hight_score_surface = font.render('HIGHT SCORE: ' + str(hight_score), True, (97,62,92))
        hight_score_rect = hight_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.screen.blit(game_over_img, game_over_rect)
        self.screen.blit(score_surface, score_rect)
        self.screen.blit(hight_score_surface, hight_score_rect)
        self.reset = False
        if self.reset_button.draw():
            self.click_sound(self.volume)
            self.reset = True

class Button():
    def __init__(self, screen, image, x, y, scale):
        self.screen = screen
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        x_center = x - width // 2
        y_center = y - height // 2
        self.rect.topleft = (x_center, y_center)
        self.clicked = False

    def draw(self):
        action = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.clicked and pygame.mouse.get_pressed()[0] == 1:
                action = True
        
        self.clicked = pygame.mouse.get_pressed()[0]
        self.screen.blit(self.image, self.rect)
        return action


def main(SCREEN):
    game = Game(SCREEN)
    game.reset()
    while True:
        game.update()
        pygame.display.update()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main(SCREEN)