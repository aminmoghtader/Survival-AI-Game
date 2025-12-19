import pygame.font
from pygame.sprite import Group
import cv2
from ship import Ship

dir = "/home/am/Documents/AI/anaconda3/envs/ML/AI_Game/Survival/images/ship1.bmp"
img = cv2.imread(dir)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
resized = cv2.resize(img, (50, 50)).swapaxes(0, 1)


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10    

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            mini_image = pygame.transform.scale(ship.image, (ship.rect.width // 3, 
                                                             ship.rect.height // 3))
            ship.image = mini_image
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 710
            self.ships.add(ship)

    def health_bar(self):
        #
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 770

        health_percentage = max(0, self.ai_game.ship.health / 100)
        current_width = int(bar_width * health_percentage)

        pygame.draw.rect(self.screen, (80, 80, 80), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        pygame.draw.rect(self.screen, (0, 255, 0), 
                        (bar_x, bar_y, current_width, bar_height))
        
        if self.ai_game.ship.health <= 30:
            pygame.draw.rect(self.screen, (255, 0, 0), 
                             (bar_x, bar_y, current_width, bar_height))

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        self.health_bar()