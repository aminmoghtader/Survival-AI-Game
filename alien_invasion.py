import sys
import pygame
import random
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from bullet1 import  A_bullet
from scoreboard import Scoreboard
from explosion import Explosion
import numpy as np

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self, ai_control=False):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                                self.settings.screen_height))
        pygame.display.set_caption("Sicktir")
        self.screen.fill(self.settings.bg_color)
        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        self.stats = GameStats(self)
        self._create_fleet()
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        self.play_button = Button(self, "Play")
        self.sb = Scoreboard(self)
        self.explosions = pygame.sprite.Group()
        self.alien_spawn_timer = 0
        self.alien_spawn_delay = 100 
        self.alien_row_y = -100
        self.ai_control = ai_control

    def run_game(self):

        while True:
            self._check_events() 

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._alien_drop()

            self._update_screen()
            self.clock.tick(60)


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.K_SPACE:
                self.game_active = True
            elif event.type == pygame.K_s:
                self.game_active = False
            elif event.type == pygame.K_a:  
                self._check_keydown_events(event)
            elif event.type == pygame.K_d:
                self._check_keydown_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.health_bar()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_z:
            self._fire_bullet()
        elif event.key == pygame.K_SPACE:
            self.game_active = True
        elif event.key == pygame.K_s:
            self.game_active = False
        elif event.key == pygame.K_a:
            self.ship.rotate("left")
        elif event.key == pygame.K_d:
            self.ship.rotate("right")

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            bullet_1 = Bullet(self, self.ship.angle)
            bullet_1.rect.midtop = (self.ship.rect.centerx - 50, self.ship.rect.top)
            bullet_2 = Bullet(self, self.ship.angle)
            bullet_2.rect.midtop = (self.ship.rect.centerx + 50, self.ship.rect.top)
            self.bullets.add(bullet_1,bullet_2)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        self.alien_bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0 or bullet.rect.top > \
                self.screen.get_rect().height:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            
            for bullets in collisions.values():
                for alien in bullets:
                    explosion = Explosion(alien.rect.center)
                    self.explosions.add(explosion)
                    self.stats.score += self.settings.alien_points

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.alien_bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.ship.health = 100

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()
            self.sb.prep_ships()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        """Check if the fleet is at an edge, then update positions."""
        self._spawn_aliens()
        for alien in self.aliens.sprites():
            if random.randint(0, self.settings.alien_bullet) == 0:
                bullet = A_bullet(self, alien)
                self.alien_bullets.add(bullet)

        #drop
        if not self.settings.initial_drop_done:
            self._alien_drop()
            return
                        
        self._check_fleet_edges()
        self.aliens.update()        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens,):
            self._ship_hit()
        hits = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True) 
        if hits:
            self.ship.health -= 20
            if self.ship.health <= 0:
                self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        #self._check_aliens_bottom()

    def _alien_drop(self):
        #
        all_dropped = True
        shake_intensity = 6
        
        for alien in self.aliens.sprites():
            if alien.rect.y < self.settings.initial_drop_distance:
                progress = alien.rect.y / self.settings.initial_drop_distance
                drop_speed = max(1, int(5 * (1 - progress)))
                alien.rect.y += drop_speed
                offset_x = random.randint(-shake_intensity, shake_intensity)
                alien.rect.x += offset_x
                all_dropped = False
        if all_dropped:
            self.settings.initial_drop_done = True
              

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        start_y = -alien_height * 9
        current_x, current_y = alien_width, start_y 
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 8 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1   

    def _spawn_aliens(self):

        self.alien_spawn_timer += 1

        if self.alien_spawn_timer >= self.alien_spawn_delay:
            self.alien_spawn_timer = 0

            alien = Alien(self)
            alien_width, alien_height = alien.rect.size

            # چک کنیم که پایین‌تر از محدوده‌ی صفحه نیست
            if self.alien_row_y < self.settings.screen_height / 3:
                # در هر ردیف، چند تا بیگانه بسازیم
                for x in range(alien_width, self.settings.screen_width - alien_width, 2 * alien_width):
                    self._create_alien(x, self.alien_row_y)
            
                # ردیف بعدی بالاتر (یعنی نزدیک‌تر به وسط)
                self.alien_row_y += 6 * alien_height

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        self._spawn_aliens()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()

        # Draw the play button if the game is inactive.

        #font = pygame.font.SysFont(None, 36)
        #health_text = font.render(f"Health: {self.ship.health}", True, (255, 0, 0))
        #self.screen.blit(health_text, (20, 20))
        self.explosions.update()
        self.explosions.draw(self.screen)
        
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _get_observation(self):
        """Extract current game state as numeric array."""
        ship_x = self.ship.rect.centerx / self.settings.screen_width
        
        aliens = list(self.aliens.sprites())[:10]
        alien_positions = []
        for a in aliens:
            alien_positions.extend([
                a.rect.x / self.settings.screen_width,
                a.rect.y / self.settings.screen_height
            ])
        
        # پر کردن کمبود بیگانه‌ها با صفر
        while len(alien_positions) < 20:
            alien_positions.append(0)
        
        bullets = list(self.bullets.sprites())[:5]
        bullet_positions = []
        for b in bullets:
            bullet_positions.extend([
                b.rect.x / self.settings.screen_width,
                b.rect.y / self.settings.screen_height
            ])
        while len(bullet_positions) < 10:
            bullet_positions.append(0)
        
        obs = np.array([ship_x] + alien_positions + bullet_positions, dtype=np.float32)
        return obs
    
    def reset(self):
        """Reset the game to start a new episode (for RL)."""
        # پاک کردن همه‌ی اشیاء بازی
        self.bullets.empty()
        self.aliens.empty()
        self.alien_bullets.empty()
        self.explosions.empty()

        # ریست کردن وضعیت سفینه و نمره
        self.ship.center_ship()
        self.ship.health = 100
        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()

        # ایجاد بیگانگان جدید
        self._create_fleet()
        self.settings.initial_drop_done = False

        # بازگرداندن observation اولیه برای RL
        obs = self._get_observation()
        return obs
    

if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
