import numpy as np
import gymnasium as gym
from gymnasium import spaces
from alien_invasion import AlienInvasion  # بازی خودت

class AlienEnv(gym.Env):
    """Gymnasium environment wrapping Alien Invasion."""
    
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode

        # بازی واقعی
        self.game = AlienInvasion(ai_control=True)

        # Action space: 0=left, 1=right, 2=fire
        self.action_space = spaces.Discrete(3)

        # Observation: [ship_x, 10*alien_positions(x,y), 5*bullet_positions(x,y)]
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(31,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        """Reset environment and return initial observation."""
        if seed is not None:
            np.random.seed(seed)

        self.game.reset()
        obs = self._get_observation()
        info = {}
        return obs, info  # Gymnasium API expects tuple (obs, info)

    def step(self, action):
        """Apply action, update game, return obs, reward, terminated, truncated, info"""
        # اعمال اکشن
        if action == 0:
            self.game.ship.rect.x -= 5
        elif action == 1:
            self.game.ship.rect.x += 5
        elif action == 2:
            self.game._fire_bullet()

        # بروزرسانی وضعیت بازی
        self.game._update_bullets()
        self.game._update_aliens()

        obs = self._get_observation()
        reward = self._calculate_reward()
        terminated = self.game.ship.health <= 0 or not self.game.aliens
        truncated = False
        info = {}

        return obs, reward, terminated, truncated, info

    def _get_observation(self):
        """Return numeric observation of current game state."""
        ship_x = self.game.ship.rect.centerx / self.game.settings.screen_width

        aliens = list(self.game.aliens.sprites())[:10]
        alien_positions = []
        for a in aliens:
            alien_positions.extend([
                a.rect.x / self.game.settings.screen_width,
                a.rect.y / self.game.settings.screen_height
            ])
        while len(alien_positions) < 20:
            alien_positions.append(0.0)

        bullets = list(self.game.bullets.sprites())[:5]
        bullet_positions = []
        for b in bullets:
            bullet_positions.extend([
                b.rect.x / self.game.settings.screen_width,
                b.rect.y / self.game.settings.screen_height
            ])
        while len(bullet_positions) < 10:
            bullet_positions.append(0.0)

        obs = np.array([ship_x] + alien_positions + bullet_positions, dtype=np.float32)
        return obs

    def _calculate_reward(self):
        """Reward function."""
        reward = 0.0
        # پاداش برای از بین بردن بیگانگان
        reward += (10 - len(self.game.aliens)) * 0.5
        # پاداش برای زنده ماندن
        reward += 0.1 if self.game.ship.health > 0 else 0.0
        return reward
    


    def render(self):
        """Render the game to the screen."""
        if self.render_mode == "human":
            self.game.render_frame()
            # خیلی مهم: بدون این خط صفحه سیاه می‌ماند
            import pygame
            pygame.display.update()

    def close(self):
        """Close the game window."""
        self.game.quit_game()
