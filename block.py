import pygame
import numpy as np
import settings as sts


class Block:

    def __init__(self, x, y, color):
        self.color = color
        self.rect = pygame.Rect(x, y, sts.cell_size, sts.cell_size)

    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        
    def check_sides(self, surface, shift_x): 
        rect = surface.get_rect()
        right_border = self.x + sts.cell_size + shift_x <= rect.right
        left_border = self.x + shift_x >= rect.left
        return left_border * right_border

    def check_bottom(self, surface, shift_y):
        rect = surface.get_rect()
        bottom_border = self.y + shift_y + sts.cell_size <= rect.bottom
        return bottom_border
    
    # def check_collisions(self, shift_x, shift_y, inactive_blocks):
    #     pygame.sprite.collide_rect(self, inactive_blocks)

class Figure:

    def __init__(self, x, y, figure_type):
        self.x = x
        self.y = y
        self.type = sts.shapes[figure_type]
        self.color = sts.colors[figure_type]
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.active = True

        self.blocks = []
        self.create_figure_shape()

    def create_figure_shape(self):
        for shift_y, row in enumerate(self.type):
            for shift_x, cell in enumerate(row):
                if cell:
                    single_block = Block(
                        x=self.x + shift_x * sts.cell_size,
                        y=self.y + shift_y * sts.cell_size,
                        color=self.color
                    )
                    self.blocks.append(single_block)

    def check_sides(self, surface, shift):
        return all([block.check_sides(surface, shift) for block in self.blocks])
    
    def check_bottom(self, surface, shift):
        return all([block.check_bottom(surface, shift) for block in self.blocks])
    
    def move(self, surface):
        if not self.active:
            return
        
        shift_x = 0
        shift_y = sts.step_down
        if self.moving_left:
            shift_x = -sts.step_side
        if self.moving_right:
            shift_x = sts.step_side
        if self.moving_down:    
            shift_y = shift_y * sts.speed_coef
        
        coef_x = self.check_sides(surface, shift_x)
        coef_y = self.check_bottom(surface, shift_y)
        
        # Спускаемся на недостающий участок, чтобы фигура всегда прижималась к низу 
        if coef_y == 0:
            shift_y /= sts.speed_coef
            coef_y = self.check_bottom(surface, shift_y)

        for block in self.blocks:
            block.move(coef_x * shift_x, coef_y * shift_y)
        self.x += coef_x * shift_x
        self.y += coef_y * shift_y
        if coef_y == 0:
            self.active = False

    def rotate(self):
        self.type = np.rot90(self.type)
        self.blocks.clear()
        self.create_figure_shape()

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)
    
