import pygame 
import settings as sts


class ScoreBoard:

    def __init__(self, surface):
        self.surface = surface
        self.surface_rect = surface.get_rect()
        self.level = 1
        self.score = 0
        self.total_lines = 0
        self.score_images = [] 
        self.score_rects = []
        self.font = pygame.font.Font(None, sts.text_size)
        self.offset_top = 50
    
    def reset_score(self):
        self.level = 1
        self.score = 0
        self.total_lines = 0
        self.score_images = [] 
        self.score_rects = []

    def render_stats(self):
        text_lines = [f"Score: {self.score}", f"Level: {self.level}"]
        self.score_images = [self.font.render(string, True, sts.text_color, sts.bg_color) for string in text_lines]
        self._set_score_positions()
        
    def _set_score_positions(self):
        for num, score_image in enumerate(self.score_images):
            score_rect = score_image.get_rect()
            score_rect.right = self.surface_rect.right - 20
            score_rect.top = self.surface_rect.left + num * self.offset_top
            self.score_rects.append(score_rect)

    def update_stats(self, num_lines):
        self.score += num_lines**2
        self.total_lines += num_lines
        if self.total_lines and self.total_lines % sts.lines_to_increse_level == 0:
            sts.step_down += 1
            self.level += 1

    def draw(self):
        self.render_stats()
        for image, rect in zip(self.score_images, self.score_rects):
            self.surface.blit(image, rect)
        