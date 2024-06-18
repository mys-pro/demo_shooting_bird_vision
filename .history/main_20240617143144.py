import pygame
import os
import random
import time
import mediapipe as mp
import cv2

# Khởi tạo pygame
pygame.init() 
pygame.display.set_caption("Shooting Bird")
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class HandTracker:
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
        explosions_speed = 2
        self.counter += 1
        if self.counter >= explosions_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        if self.index >= len(self.images) - 1 and self.counter >= explosions_speed:
            self.kill()

class Game():
    def __init__(self):
        self.volume = 0.02
        pygame.mixer.music.load('assets/music/bgMusic.ogg')
        pygame.mixer.music.play(repeat)
        pygame.mixer.music.set_volume(volume)

        self.game_font = pygame.font.Font('assets/fonts/digital-7.ttf', 40)
        self.background = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.view_finder = viewFinder()
        spawnBird = pygame.USEREVENT
        pygame.time.set_timer(spawnBird, 2000)

        self.birds_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        self.Fire_rate = 100
        self.Cur_Fire_rate = 0
        self.score = 0
        self.hight_score = 0
        self.percent = 100
        self.time = 31
        self.cur_time = time
        self.game_play = False
        self.tap_play = True
        self.game_end = False
    
    def reset(self):
        self.Fire_rate = 100
        self.Cur_Fire_rate = 0
        self.score = 0
        self.hight_score = 0
        self.percent = 100
        self.time = 31
        self.cur_time = time
        self.game_play = False
        self.tap_play = True
        self.birds_group = []



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

    def get_score(self, screen, score):
        score_surface = self.game_font.render('SCORE: ' + str(score), True, (255, 255, 255))
        screen.blit(score_surface, [20, 20])

    # Lấy âm thanh
    def get_sound(file_path, volume):
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    sound.play()

# Xử lý thanh nạp đạn
def fire_bar(screen, game_font, percent):
    width, height = 500, 35
    bar_bg = pygame.Surface((width, height), pygame.SRCALPHA)
    bar_bg.fill((255, 255, 255) + (120,)) 

    bar = pygame.Surface((width * (percent / 100), height))
    bar.fill((188,186,50)) 

    text = game_font.render('FIRE RATE', True, (255, 255, 255))

    x = SCREEN_WIDTH // 2 - width // 2 - 15
    y = SCREEN_HEIGHT - 20 - height

    screen.blit(text, [x - 170, y + 1])
    screen.blit(bar_bg, [x, y])
    screen.blit(bar, [x, y])

# Xủ lý hiển thị thơi gian
def time_display(screen, time, game_font):
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

    time_surface = game_font.render('TIME: ' + M + ":" + S, True, (255, 255, 255))
    screen.blit(time_surface, [855, SCREEN_HEIGHT - 20 - 35])

# Xử lý kết thúc game
def game_over(screen, score, hight_score, game_font):
    score_surface = game_font.render('SCORE: ' + str(score), True, (255, 255, 255))
    hight_score_surface = game_font.render('HIGHT SCORE: ' + str(hight_score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130))
    hight_score_rect = hight_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    screen.blit(score_surface, score_rect)
    screen.blit(hight_score_surface, hight_score_rect)

# Vẽ hình ảnh
def draw(SCREEN, game_play, tap_play, game_end, background, view_finder, birds_group, explosion_group, score, hight_score, game_font, percent, time):
    bg, bg_x, bg_y = background 
    SCREEN.blit(bg, (bg_x, bg_y))

    if tap_play is False:
        for bird in birds_group:
            if game_play is False:
                bird.kill()
            bird.draw(SCREEN)
        birds_group.update()

        explosion_group.draw(SCREEN)
        explosion_group.update() 

        score_display(SCREEN, score, game_font)
        fire_bar(SCREEN, game_font, percent)

        time_display(SCREEN, time, game_font)

    if tap_play:
        font = pygame.font.Font('assets/fonts/digital-7.ttf', 90)
        text = font.render('TAP TO PLAY', True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2))
        SCREEN.blit(text, text_rect)

    if game_end:
        game_over(SCREEN, score, hight_score, game_font)

    # view_finder.follow_mouse()
    view_finder.draw(SCREEN)
    pygame.display.update()

def main(SCREEN):
    volume = 0.02
    get_music('assets/music/bgMusic.ogg', -1, volume)
    background = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT) # Gọi hàm get_background
    view_finder = viewFinder()
    bird_list_folder = ['bird1', 'bird2']
    spawnBird = pygame.USEREVENT
    pygame.time.set_timer(spawnBird, 2000)
    birds_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    Fire_rate = 100
    Cur_Fire_rate = 0
    game_font = pygame.font.Font('assets/fonts/digital-7.ttf', 40)
    score = 0
    hight_score = 0
    percent = 100
    time = 31
    cur_time = time
    game_play = False
    tap_play = True
    game_end = False

    # cap = cv2.VideoCapture(0)
    # hand_tracker = HandTracker()

    running = True
    while running:
        # _, frame = cap.read()

        # image = hand_tracker.scan_hands(frame)
        # cv2.imshow("Frame", image)
        # cv2.waitKey(1)
        # view_finder_x, view_finder_y = hand_tracker.get_position_hand()
        # view_finder.follow_mediapipe_hand(view_finder_x, view_finder_y)
        # if tap_play and hand_tracker.get_hand_close() and hand_tracker.get_hand_count() == 1:
        #     tap_play = False
        #     game_play = True
        #     game_end = False
        #     cur_time = time
        #     score = 0
        #     background = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT)

        # if game_play and hand_tracker.get_hand_close() and hand_tracker.get_hand_count() == 1 and Cur_Fire_rate <= 0:
        #     get_sound('assets/sound/sniper.ogg', volume)
        #     percent = 0
        #     for bird in birds_group:
        #         if view_finder.rect.colliderect(bird.rect):
        #             score += 1
        #             bird.kill()
        #             explosion = Explosions(bird.rect.x + bird.image_smaller.get_width() // 2, bird.rect.y + bird.image_smaller.get_height() // 2)
        #             explosion_group.add(explosion)
        #     Cur_Fire_rate = Fire_rate


        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if game_play and event.type == spawnBird:
                new_bird = create_bird(bird_list_folder, 5, 8)
                birds_group.add(new_bird)
            elif game_play is False:
                for bird in birds_group:
                    bird.kill()

            if tap_play and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tap_play = False
                game_play = True
                game_end = False
                cur_time = time
                score = 0
                background = get_background('assets/images/backgrounds/', SCREEN_WIDTH, SCREEN_HEIGHT)

            if game_play and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Cur_Fire_rate <= 0:
                get_sound('assets/sound/sniper.ogg', volume)
                percent = 0
                for bird in birds_group:
                    if view_finder.rect.colliderect(bird.rect):
                        score += 1
                        bird.kill()
                        explosion = Explosions(bird.rect.x + bird.image_smaller.get_width() // 2, bird.rect.y + bird.image_smaller.get_height() // 2)
                        explosion_group.add(explosion)
                Cur_Fire_rate = Fire_rate

        Cur_Fire_rate -= 5
        if Fire_rate <= 0:
            Cur_Fire_rate = 0

        if percent < 100:
            percent += 5
        
        if int(cur_time) > 0 and game_play:
            cur_time -= 0.05
        elif int(cur_time) <= 0:
            if score > hight_score:
                hight_score = score
            game_play = False
            game_end = True
            tap_play = True

        draw(SCREEN, game_play, tap_play, game_end, background, view_finder, birds_group, explosion_group, score, hight_score, game_font, percent, int(cur_time))
        pygame.time.Clock().tick(FPS)

    # hand_tracker.release()
    # cap.release()
    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main(SCREEN)