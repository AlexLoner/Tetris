import numpy as np


# Screen 
screen_width = 1000
screen_height = 700
bg_color = (66, 158, 245)

# Play Zone
pz_width = 400
pz_height = 600
pz_pos = ((screen_width - pz_width) // 2, (screen_height - pz_height) // 2)
pz_bg_color = (255, 255, 255)

# Block
cell_size = 20
step_down = 5
step_side = 10

# Game
speed_coef = 2
framerate = 5

# Colors
inactive_color = (169, 169, 169)
colors = [
    (0, 255, 255),  # I - голубой
    (0, 0, 255),    # J - синий
    (255, 165, 0),   # L - оранжевый
    (255, 255, 0),   # O - желтый
    (0, 255, 0),     # S - зеленый
    (128, 0, 128),   # T - фиолетовый
    (255, 0, 0)      # Z - красный
]

# Figures form
shapes = [
    np.array([[1, 1, 1, 1]]),  # I
    
    np.array([[1, 0, 0],
             [1, 1, 1]]),      # J
    
    np.array([[0, 0, 1],
             [1, 1, 1]]),      # L
    
    np.array([[1, 1],
              [1, 1]]),        # O
    
    np.array([[0, 1, 1],
              [1, 1, 0]]),      # S
    
    np.array([[0, 1, 0],
              [1, 1, 1]]),      # T
    
    np.array([[1, 1, 0],
              [0, 1, 1]])       # Z
]
