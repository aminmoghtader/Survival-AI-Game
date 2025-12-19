import pygame

class Explosion(pygame.sprite.Sprite):
    """انفجار کوتاه‌مدت هنگام برخورد گلوله با بیگانه‌ها."""

    def __init__(self, position):
        super().__init__()
        self.frames = []
        self.frame_index = 0
        self.duration = 5  # هر فریم چند بار نمایش داده شود
        self.frame_counter = 0

        # ایجاد چند فریم ساده از انفجار (دایره‌های رنگی)
        for size in range(5, 35, 5):
            surface = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 200 - size*5, 0), (35, 35), size)
            pygame.draw.circle(surface, (255, 255, 100), (35, 35), size // 2)
            self.frames.append(surface)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)

    def update(self):
        """نمایش فریم‌های انفجار به‌ترتیب."""
        self.frame_counter += 1
        if self.frame_counter >= self.duration:
            self.frame_counter = 0
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.kill()  # حذف پس از اتمام انیمیشن
            else:
                self.image = self.frames[self.frame_index]
