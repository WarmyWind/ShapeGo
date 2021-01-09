import pygame

# Screen
screen_size = (800,600)
screen_width, screen_height = screen_size

# Caption and icon
icon_png = "./img/icon.png"
icon = pygame.image.load(icon_png)

# Board and pieces
board_png = "./img/board2.png"
black_png = "./img/black.png"
white_png = "./img/white.png"
board = pygame.image.load(board_png)
board_size = board.get_size()
board_width, board_height = board_size
black_piece = pygame.image.load(black_png)
white_piece = pygame.image.load(white_png)
piece_size = black_piece.get_size()
piece_width, piece_height = piece_size

# Check mark
check_png = "./img/check24.png"

# Font
font_ttf = "./font/MTCORSVA.TTF"
# font = pygame.font.Font(font_ttf, 30)