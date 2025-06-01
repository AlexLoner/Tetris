
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
cell_size = 25
step_down = 5
step_side = 12.5

# Game
speed_coef = 2
framerate = 5

# Colors
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
    [[1, 1, 1, 1]],  # I
    
    [[1, 0, 0],
     [1, 1, 1]],      # J
    
    [[0, 0, 1],
     [1, 1, 1]],      # L
    
    [[1, 1],
     [1, 1]],        # O
    
    [[0, 1, 1],
     [1, 1, 0]],      # S
    
    [[0, 1, 0],
     [1, 1, 1]],      # T
    
    [[1, 1, 0],
     [0, 1, 1]]       # Z
]
