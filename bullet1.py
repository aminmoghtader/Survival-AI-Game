import pygame
from pygame.sprite import Sprite


class A_bullet(Sprite):

    def __init__(self, ai_game, alien):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 50, 50)  
        self.rect = pygame.Rect(0, 0, 5, 18)
        self.rect.midtop = alien.rect.midbottom
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.bullet_speed  
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)