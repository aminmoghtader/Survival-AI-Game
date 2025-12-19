import pygame
from pygame.sprite import Sprite
import math
import cv2
import random

dir = "/home/am/Documents/AI/anaconda3/envs/ML/AI_Game/Survival/images/ship1.bmp"
img = cv2.imread(dir)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
resized = cv2.resize(img, (180, 180)).swapaxes(0, 1)

class Ship(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.original_image = pygame.surfarray.make_surface(resized).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        #self.rect.centerx = self.screen_rect.centerx
        #self.rect.bottom = self.screen_rect.bottom 

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Movement flags; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.health = 100

        self.angle = 0
        self.rotation_speed = 180

    def rotate(self, direction:str):
        """چرخش کشتی"""
        if direction == "left":
            self.angle += self.rotation_speed
        elif direction == "right":
            self.angle -= self.rotation_speed


        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Update the ship's position based on movement flags."""
        # حرکت افقی
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # حرکت عمودی
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed          

        # به‌روزرسانی موقعیت واقعی rect
        self.rect.x = self.x
        self.rect.y = self.y
        
    
    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)
        

        if self.moving_up or self.moving_down:
            radians = math.radians(self.angle)
            flame_base_length = 80  # طول شعله
            flame_base_width = 15    # عرض شعله
            colors = [(255, 255, 100), (255, 150, 0), (255, 50, 0)]

            # مرکز پشت کشتی
            center_x = self.rect.centerx - math.sin(radians) * (self.image.get_height() / 1.8)
            center_y = self.rect.centery + math.cos(radians) * (self.image.get_height() / 1.8)

            # افست شعله‌ها برای دو موتور (چپ و راست)
            offsets = [-self.rect.width // 8.6, self.rect.width // 8.6]  # فاصله از مرکز کشتی

            for offset in offsets:
                # کمی تصادفی کردن طول شعله برای حالت طبیعی
                flame_length = flame_base_length + random.randint(-5, 5)
                flame_width = flame_base_width + random.randint(-4, 4)

                # مرکز مستطیل شعله
                rect_center_x = center_x + math.cos(radians) * offset
                rect_center_y = center_y + math.sin(radians) * offset

                    # رسم چند مستطیل رنگی برای افکت گرادیان شعله
                for i, color in enumerate(colors):
                    # هر لایه کمی کوتاه‌تر و باریک‌تر
                    layer_length = flame_length * (1 - 0.25 * i)
                    layer_width = flame_width * (1 - 0.2 * i)

                     # حرکت دینامیک شعله به عقب و جلو
                    move_offset = random.randint(-5, 5)
                    layer_center_x = rect_center_x - math.sin(radians) * move_offset
                    layer_center_y = rect_center_y + math.cos(radians) * move_offset

                    # ایجاد سطح شعله
                    flame_surf = pygame.Surface((layer_width, layer_length), pygame.SRCALPHA)
                    flame_surf.fill(color)

                    # چرخش شعله مطابق زاویه کشتی
                    rotated_flame = pygame.transform.rotate(flame_surf, self.angle)
                    new_rect = rotated_flame.get_rect(center=(layer_center_x, layer_center_y))

                    self.screen.blit(rotated_flame, new_rect)