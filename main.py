import pygame
import global_setting as gs
import utils
import game
import numpy as np

pygame.init()

# Screen
screen = pygame.display.set_mode(gs.screen_size)
pygame.display.set_caption("ShapeGo")
pygame.display.set_icon(gs.icon)

running = True
game_state = game.State()
screen.fill((255, 255, 255))
utils.show_newboard(screen)
while running:
    player_id = (game_state.turn) % 2 + 1
    for event in pygame.event.get():  # Event detect and State update
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_state.result == 0:
            mouse_down = event.button  # 1 = left, 2 = wheel, 3 = right
            if utils.is_board(event.pos):  # Click in board
                position = utils.pixel_to_position(event.pos)
                if game_state.convert_shape_selected == -1:  # move/remove
                    game_state.update_board(position, operation = mouse_down)
                else:  # convert
                    game_state.update_board(position, operation=mouse_down)
                    game_state.update_convert_shape_selected(-1, player_id)
            elif utils.is_shape_area(event.pos, player_id):  # Click in shape area
                area_index = utils.pixel_to_area_index(event.pos)
                game_state.update_convert_shape_selected(area_index, player_id)
                print("Selected size: ", game_state.convert_shape_selected)
            else:  # Click in blank, reset mode
                game_state.update_convert_shape_selected(-1, player_id)

            print('Turn{}: \n{} '.format(game_state.turn, game_state.board_state))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                print("Reset the game")
                game_state = game.State()
                print('Turn{}: \n{} '.format(game_state.turn, game_state.board_state))
                # surface = pygame.display.get_surface()
                # print(surface)

        # Check result
        result = game_state.check_result()
        # print("Result:", result)


        # Refresh
        screen.fill((255, 255, 255))
        utils.show_newboard(screen)

        # Redraw
        for i in range(3):
            for j in range(3):
                if game_state.board_state[i,j] == 1:
                    utils.show_piece(screen, gs.black_piece, (i,j))
                elif game_state.board_state[i,j] == -1:
                    utils.show_piece(screen, gs.white_piece, (i,j))

        index1, index2 = 0, 0  # 绘制的是第几个形状
        for i in range(9):
            if game_state.player1.collected_flag[i,0] == 1:
                shape = game_state.player1.collected_shape_dict[i]
                index1 += 1
                used_flag = game_state.player1.collected_flag[i, 1]
                utils.show_collected_shape(screen, player = 1, shape = shape, \
                                           index = index1, used_flag=used_flag)
                # if game_state.player1.collected_flag[i,1] == 1:
                #     utils.show_used_symbol()
            if game_state.player2.collected_flag[i,0] == 1:
                shape = game_state.player2.collected_shape_dict[i]
                index2 += 1
                used_flag = game_state.player2.collected_flag[i, 1]
                utils.show_collected_shape(screen, player = 2, shape = shape, \
                                           index = index2, used_flag=used_flag)

        if game_state.convert_shape_selected != -1:
            area_index = game_state.shape_area_selected_index
            # print('area_index: ', area_index)
            utils.show_selected_shape(screen, player_id, area_index)

        utils.show_result(screen, result, player_id)
    pygame.display.update()
