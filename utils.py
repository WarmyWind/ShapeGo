import math
import global_setting as gs
import pygame

# Board area
board_left_X = gs.screen_width / 2 - gs.board_width / 2
board_right_X = gs.board_width + board_left_X
board_top_Y = gs.screen_height / 2 - gs.board_height / 2
board_bottom_Y = gs.board_height + board_top_Y

# Shape area
shape_width = gs.board_width / 4
shape_margin = 0.1 * gs.board_width  # margin between two shape
shape_area_width = gs.board_width + 3 * shape_margin

r = shape_width / (6 * 1.1 + 0.2 * 2)  # radius of circle drawed in shape area
shape_area_Y_base1 = board_bottom_Y + 4.5 * r
shape_area_Y_base2 = board_top_Y - 4.5 * r

shape_area_left_X = board_left_X - 0.15 * gs.board_width
# shape_area1_base_X = shape_area_left_X + 0.5 * shape_width
shape_area_right_X = shape_area_left_X + shape_area_width
shape_area1_top_Y = shape_area_Y_base1 - shape_width / 2
shape_area1_bottom_Y = shape_area_Y_base1 + shape_width / 2
shape_area2_top_Y = shape_area_Y_base2 - shape_width / 2
shape_area2_bottom_Y = shape_area_Y_base2 + shape_width / 2

def show_newboard(screen):
    board = pygame.image.load(gs.board_png)
    screen.blit(board, (board_left_X, board_top_Y))
    #screen.blit(board, (gs.screen_width/2-gs.board_width/2, gs.screen_height/2-gs.board_height/2))
    return board

def show_piece(screen, piece, position):
    position_X, position_Y = position  # 棋子的棋盘坐标，（0,0）到（2,2）
    # centre是（1,1）的相对棋盘像素位置
    centre_X, centre_Y = (gs.board_width/2-gs.piece_width/2, gs.board_height/2-gs.piece_height/2)
    offset_X, offset_Y = gs.board_width/3-3, gs.board_height/3-3  # 相邻两棋子的像素距离
    X, Y = centre_X + offset_X*(position_X-1), centre_Y + offset_Y*(position_Y-1)
    screen.blit(piece, (X + board_left_X, Y + board_top_Y))
    # board.blit(piece, (X, Y))

def show_collected_shape(screen, player, shape, index, used_flag):
    check_mark = pygame.image.load(gs.check_png)
    base_Y = shape_area_Y_base1 if player == 1 else shape_area_Y_base2

    line_width = 0 if player == 1 else 2
    color = (0,0,0)
    base_X = shape_area_left_X + 0.5 * shape_width \
                     + (index-1)*(shape_width+shape_margin)  # base = shape centre
    for pos in shape:
        pos_X, pos_Y = pos
        position = base_X + 2.4*r*(pos_X-1), base_Y + 2.4*r*(pos_Y-1)
        pygame.draw.circle(screen, color=color, center=position, \
                           radius = r, width=line_width)
    if used_flag == 1:
        screen.blit(check_mark, (base_X+shape_width/3, base_Y+shape_width/3 - 5))

def show_selected_shape(screen, player, area_index):
    base_Y = shape_area_Y_base1 if player == 1 else shape_area_Y_base2
    base_X = shape_area_left_X + 0.5 * shape_width \
             + (area_index)*(shape_width+shape_margin)
    position = (base_X-shape_width/2, base_Y-shape_width/2, shape_width, shape_width)
    color = (0, 0, 0)
    line_width = 2
    pygame.draw.rect(screen, color, position, width=line_width)

def show_result(screen, result, player_id):
    if result == 0:
        font = pygame.font.Font(gs.font_ttf, 56)
        result_str = "Black  Turn" if player_id == 1 else "White  Turn"
        text_result = font.render(result_str, True, (0, 0, 0))
        screen.blit(text_result, (board_left_X, board_top_Y / 4))
    else :
        font = pygame.font.Font(gs.font_ttf, 56)
        result_str = "Black Win!" if result == 1 else "White Win!"
        text_result = font.render(result_str, True, (0,0,0))
        screen.blit(text_result, (board_left_X, board_top_Y/4))

        hint_str = "Press R to reset the game"
        font = pygame.font.Font(gs.font_ttf, 28)
        text_hint = font.render(hint_str, True, (0,0,0))
        screen.blit(text_hint, (board_left_X, board_bottom_Y + board_top_Y / 2))


def is_board(pixel):
    pixel_X, pixel_Y = pixel
    if pixel_X <= board_left_X \
        or pixel_X >= board_right_X \
        or pixel_Y <= board_top_Y \
        or pixel_Y >= board_bottom_Y:
        return False  # 在棋盘外
    else:
        return True

def pixel_to_position(pixel):
    pixel_X, pixel_Y = pixel
    # #  棋盘范围
    #
    # if pixel_X <= board_left_X \
    #     or pixel_X >= board_right_X \
    #     or pixel_Y <= board_top_Y \
    #     or pixel_Y >= board_bottom_Y:
    #     return (-1, -1)  # 在棋盘外
    # else:
    position_X = math.floor((pixel_X-board_left_X)/(gs.board_width/3))
    position_Y = math.floor((pixel_Y-board_top_Y)/(gs.board_height/3))
    return(position_X, position_Y)

def is_shape_area(pixel, player_id):
    pixel_X, pixel_Y = pixel

    shape_area_top_Y, shape_area_bottom_Y = \
        (shape_area1_top_Y, shape_area1_bottom_Y) if player_id == 1\
        else (shape_area2_top_Y, shape_area2_bottom_Y)

    if pixel_X <= shape_area_left_X \
            or pixel_X >= shape_area_right_X \
            or pixel_Y <= shape_area_top_Y \
            or pixel_Y >= shape_area_bottom_Y:
        return False
    else:
        return True

def pixel_to_area_index(pixel):
    pixel_X, pixel_Y = pixel
    area_index = math.floor((pixel_X-shape_area_left_X)/(shape_area_width/4))
    return area_index

def add_tuple(tupleA, tupleB):
    ax, ay = tupleA
    bx, by = tupleB
    return ax+bx, ay+by

def minus_tuple(tupleA, tupleB):
    bx, by = tupleB
    return add_tuple(tupleA, (-bx, -by))