class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings 
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 20

        # Alien settings.

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 3       
        self.initial_drop_distance = 400   
        self.initial_drop_done = False

        self.fleet_drop_speed = 6
        self.score_scale = 1.5
        # How quickly the game speeds up
        self.speedup_scale = 1.2
        self.bullet_factor = 10
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        #
        self.alien_speed = 1.0
        self.bullet_speed = 25
        self.ship_speed = 12
        self.fleet_direction = 2
        self.alien_bullet = 400
        # Scoring settings
        self.alien_points = 10

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        if self.alien_bullet > 30:
            self.alien_bullet -= self.bullet_factor