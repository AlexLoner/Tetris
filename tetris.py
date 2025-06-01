import pygame
import numpy as np
import settings as sts
from block import Figure

class Tetris:
    """Класс для управления рерсами и поведением игры"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((sts.screen_width, sts.screen_height))
        self.pz_screen = self.screen.subsurface((*sts.pz_pos, sts.pz_width, sts.pz_height))
        pygame.display.set_caption("Тетрис Демо")
        self.active_figure = None
        self.blocks = []
        self.run_game = True
        self.clock = pygame.time.Clock()
    
    def key_down_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self.run_game = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.active_figure.moving_left = True
        elif event.key == pygame.K_RIGHT or event.key ==  pygame.K_d:
            self.active_figure.moving_right = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.active_figure.moving_down = True
        elif event.key == pygame.K_SPACE:
            self.active_figure.rotate()
            while not self.active_figure.check_sides(self.pz_screen, 0):
                for block in self.active_figure.blocks:
                    block.x -= sts.step_side

    def key_up_events(self, event):
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.active_figure.moving_left = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.active_figure.moving_right = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.active_figure.moving_down = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_game = False
            elif event.type == pygame.KEYDOWN:
                self.key_down_events(event)
            elif event.type == pygame.KEYUP:
                self.key_up_events(event)
                
    def create_figure(self):
        figure_type = np.random.randint(low=0, high=len(sts.shapes))
        self.active_figure = Figure(x=sts.pz_pos[0], y=sts.pz_pos[1], figure_type=figure_type)

    def update_screen(self):
        self.screen.fill(sts.bg_color)
        self.pz_screen.fill(sts.pz_bg_color)
        self.active_figure.draw(self.screen)
        self.draw_inactive_block()
        pygame.display.flip()
    
    def add_inactive_blocks(self, blocks):
        for block in blocks:
            block.color = sts.inactive_color
            self.blocks.append(block)

    def draw_inactive_block(self):
        for block in self.blocks:
            block.draw(self.pz_screen)
        
    def start_game(self):
        while self.run_game:
            if self.active_figure is None:
                self.create_figure()
            elif not self.active_figure.active:
                self.add_inactive_blocks(self.active_figure.blocks)
                self.create_figure()
            self.handle_events()
            self.active_figure.move(surface=self.pz_screen)
            self.update_screen()
            self.clock.tick(sts.framerate)
            

if __name__ == "__main__":

    tetris = Tetris()
    tetris.start_game()    
        