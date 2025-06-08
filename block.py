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
    
    def check_collisions(self, shift_x, shift_y, inactive_blocks):
        self.move(shift_x, shift_y)
        collision = pygame.sprite.spritecollide(self, inactive_blocks, False)
        self.move(-shift_x, -shift_y)
        return collision

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
    
    def check_collisions(self, shift_x, shift_y, inactive_blocks):
        # Отрицание потому что метод проверяет наличие столкновения при заданном смещении блока фигуры  
        return all([not block.check_collisions(shift_x, shift_y, inactive_blocks) for block in self.blocks])

    def check_sides(self, surface, shift):
        return all([block.check_sides(surface, shift) for block in self.blocks])
    
    def check_bottom(self, surface, shift):
        return all([block.check_bottom(surface, shift) for block in self.blocks])
    
    def move(self, surface, inactive_blocks):
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

        # (Проверка столкновений с другими блоками) and (Проверка границ игрового поля)
        coef_x = self.check_collisions(shift_x, 0, inactive_blocks) and self.check_sides(surface, shift_x)
        coef_y = self.check_collisions(0, shift_y, inactive_blocks) and self.check_bottom(surface, shift_y)
    
        if coef_y == 0:
            while (self.check_collisions(0, sts.bottom_correction, inactive_blocks) 
                   and self.check_bottom(surface, sts.bottom_correction)
            ):
                for block in self.blocks:
                    block.move(0, sts.bottom_correction)
            self.active = False
            return 
        
        for block in self.blocks:
            block.move(coef_x * shift_x, coef_y * shift_y)
        
        self.x += coef_x * shift_x
        self.y += coef_y * shift_y
            

    def rotate(self, surface, inactive_blocks):
        if not self.active:
            return
        
        # Сохраняем текущее состояние
        old_type = self.type.copy()
        old_blocks = [block for block in self.blocks]
        old_x, old_y = self.x, self.y
        
        # Поворачиваем матрицу фигуры
        self.type = np.rot90(self.type)
        self.blocks.clear()
        self.create_figure_shape()
        
        # Пытаемся скорректировать позицию, если поворот невозможен
        adjustments = [0, -1, 1, -2, 2]  # Попробуем разные смещения
        for dx in adjustments:
            for dy in adjustments:

                if (self.check_collisions(dx * sts.cell_size, dy * sts.step_down, inactive_blocks)
                    and self.check_sides(surface, dx * sts.cell_size) 
                    and self.check_bottom(surface, dy * sts.step_down) 
                ):
                    # Если нашли подходящее смещение - применяем его
                    for block in self.blocks:
                        block.move(dx * sts.cell_size, 0)
                    self.x += dx * sts.cell_size
                    return
            
        # Если не удалось найти подходящую позицию - отменяем поворот
        self.type = old_type
        self.blocks = old_blocks
        self.x, self.y = old_x, old_y
        self.create_figure_shape()

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)
    
