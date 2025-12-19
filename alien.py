import pygame
import cv2
from pygame.sprite import Sprite

dir = "/home/am/Documents/AI/anaconda3/envs/ML/AI_Game/Survival/images/alien.bmp"
img = cv2.imread(dir)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
resized = cv2.resize(img, (80, 80)).swapaxes(1, 0)
rotated = cv2.flip(resized, -1)

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.surfarray.make_surface(rotated).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen_rect = ai_game.screen.get_rect()   

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        """Move the alien right or left."""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
