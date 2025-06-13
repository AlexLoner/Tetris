import numpy as np
import settings as sts


class GameBoard:

    def __init__(self):
        self.board = np.zeros((sts.rows, sts.cols), dtype=np.int8)
    
    def transform_position(self, block):
        return block.rect.centery // sts.cell_size, block.rect.centerx // sts.cell_size

    def add_block(self, block):
        row, col = self.transform_position(block)
        self.board[row, col] = 1

    def clean_lines(self, inactive_blocks):
        block_at_rows = np.sum(self.board, axis=1)
        indexes_to_burn = np.where(block_at_rows == sts.cols)[0]
        if len(indexes_to_burn) == 0:
            return 0
        
        # Убираем заполненные полностью линии 
        for block in inactive_blocks[:]:
            row, _ = self.transform_position(block)
            if row in indexes_to_burn:
                inactive_blocks.remove(block)
        self.board[indexes_to_burn] = 0

        for index in indexes_to_burn:
            for block in inactive_blocks[:]:
                row, col = self.transform_position(block)
                if index > row:
                    block.move(0, sts.cell_size)
                    self.board[row, col] -= 1
                    self.board[row + 1, col] += 1

        return len(indexes_to_burn)
    
    
