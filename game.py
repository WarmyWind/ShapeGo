import numpy as np
import utils
# class Piece:
#     def __init__(self,color = 0, pos=(-1,-1)):
#         self.color = color
#         self.pos = pos

class Player:
    def __init__(self, collected_flag=np.zeros(9), collected_shape_dict={}, collected_num=0):
        self.collected_flag = np.zeros((9,2))  # 收集过的点数及是否使用
        self.collected_shape_dict = {}  # 收集到的形状
        self.collect_num = 0  # 收集了几种点数，4种即胜利

    def new_remove(self, position_list, size):
        self.collected_flag[size, 0] = 1
        self.collected_shape_dict[size] = position_list
        self.collect_num += 1

    def new_convert(self):
        pass

class State:
    def __init__(self):
        self.turn = 0
        self.board_state = np.zeros((3,3))  # board_state element: 1=black, -1=white, 0=none
        self.shape_area_selected_index = - 1  # -1 = no select, 0 = first
        self.convert_shape_selected = -1  # -1 = no select, 2 = selected shape size = 2
        self.player1 = Player()  # Black
        self.player2 = Player()  # White
        self.result = 0  # 0 = Going, 1 = Black win, 2 = White win

    def update_board(self, position, operation):
        # operation 1 = move, 3 = remove, 2 = convert
        player = self.player1 if self.turn % 2 == 0 else self.player2
        # if operation == 1 and self.convert_shape_selected == -1:  # move or convert
        #     if self.board_state[position] == 0:
        #         self.board_state[position] = 1 if self.turn % 2 == 0 else -1
        #         self.next_turn()
        if operation == 1 and self.board_state[position] == 0:  # move
            self.board_state[position] = 1 if self.turn % 2 == 0 else -1
            self.next_turn()
        elif operation == 1 and self.convert_shape_selected != -1:  # convert
            selected_shape_size = self.convert_shape_selected
            if player.collected_flag[selected_shape_size, 1] == 0:  # unused
                position_list = self.search_fit_shape(position, selected_shape_size)
                if position_list != []:
                    print("Convert shape")
                    for pos in position_list:
                        self.board_state[pos] *= -1
                    player.collected_flag[selected_shape_size, 1] = 1  # mark as used
                    self.next_turn()
            else: print("This shape has been used")
        elif operation == 3:  # remove
            #if self.board_state[position] == 1 and self.turn % 2 == 0:
            position_list, num_list = self.shape_find(position,pos_list=[],flag=np.zeros((3,3)), num=[0])
            size = num_list.pop()
            print('Remove detect: ',position_list, size)
            if size > 1:
                if player.collected_flag[size, 0] == 0:
                    player.new_remove(position_list, size)
                    # print(self.player1.collected_flag[size,0])
                    for pos in position_list:
                        self.board_state[pos] = 0
                    self.next_turn()

        elif operation == 2:  # wheel click
            pass

    def check_result(self):
        player = player = self.player1 if self.turn % 2 == 0 else self.player2
        chess_color = 1 if self.turn % 2 == 0 else -1
        black_count = 0
        white_count = 0
        # result 0 = Going, 1 = black win, 2 = white win
        if self.player1.collect_num >= 4:
            self.result = 1
            return 1  # white win by collecting 4 shapes
        elif self.player2.collect_num >= 4:
            self.result = 2
            return 2  # black win by collecting 4 shapes
        if self.turn > 1:
            for i in range(3):
                for j in range(3):
                    if self.board_state[i,j] == 1: black_count+=1
                    elif self.board_state[i,j] == -1: white_count+=1
            if black_count == 0:
                self.result = 2
                return 2  # white win by no black pieces existing
            elif white_count == 0:
                self.result = 1
                return 1  # black win by no white pieces existing

        trapped_dead_flag = 0  # Check trapped dead
        if black_count+white_count == 9:
            trapped_dead_flag = 1
            for i in range(3):  # check whether can remove or not
                #if trapped_dead_flag == 1:
                for j in range(3):
                    if self.board_state[i, j] == chess_color:
                        position = (i, j)
                        position_list, num_list = self.shape_find(position, pos_list=[], flag=np.zeros((3, 3)), num=[0])
                        size = num_list.pop()
                        # print('Remove detect: ', position_list, size)
                        if size > 1:
                            if player.collected_flag[size, 0] == 0:
                                print("Find fit shape to remove")
                                trapped_dead_flag = 0  # can do remove
                                break
                if trapped_dead_flag == 0: break

            if trapped_dead_flag == 1:
                for flag_index in range(9):  # check whether can convert or not
                    if trapped_dead_flag == 1 and \
                            player.collected_flag[flag_index, 0] == 1 \
                            and player.collected_flag[flag_index, 1] == 0:
                        for i in range(3):
                            # if trapped_dead_flag == 1:
                            for j in range(3):
                                selected_shape_size = flag_index
                                position = (i, j)
                                position_list = self.search_fit_shape(position, selected_shape_size)
                                if position_list != []:
                                    print("Find fit shape to convert")
                                    trapped_dead_flag = 0  # can do convert
                                    break
                            if trapped_dead_flag == 0: break
                        if trapped_dead_flag == 0: break

        if trapped_dead_flag == 1:
            self.result = 2 if self.turn % 2 == 0 else 1
            # print("Trapped dead!")
            return self.result
        return self.result

    def shape_find(self,position,pos_list,flag,num):
        position_X, position_Y = position
        if position_X < 0 or position_X > 2 or position_Y < 0 or position_Y > 2:
            return
        if (self.board_state[position] == 1 and self.turn % 2 == 0)\
            or (self.board_state[position] == -1 and self.turn % 2) == 1:
            if flag[position] == 0:
                pos_list.append(position)
                flag[position] = 1
                num.append(num.pop() + 1)
                self.shape_find(position=(position_X - 1,position_Y), \
                                pos_list=pos_list, flag=flag, num=num)
                self.shape_find(position=(position_X + 1, position_Y), \
                                pos_list=pos_list, flag=flag, num=num)
                self.shape_find(position=(position_X, position_Y - 1), \
                                pos_list=pos_list, flag=flag, num=num)
                self.shape_find(position=(position_X, position_Y + 1), \
                                pos_list=pos_list, flag=flag, num=num)
        return pos_list,num


    def search_fit_shape(self, target_position, selected_shape_size):
        player = self.player1 if self.turn % 2 == 0 else self.player2
        # selected_shape_size = self.convert_shape_selected
        shape = player.collected_shape_dict[selected_shape_size]
        # print("Shape:", shape)
        rel_XY_list = []  # 存储以第一个点为基准的相对距离
        pos0 = shape[0]
        #pos0_X, pos0_Y = pos0
        for pos in shape:
            #pos_X, pos_Y = pos
            #rel_XY = (pos_X-pos0_X, pos_Y-pos0_Y)
            rel_XY = utils.minus_tuple(pos,pos0)
            rel_XY_list.append(rel_XY)

        # print("rel_XY_list: ", rel_XY_list)
        chess_color = 1 if self.turn % 2 == 0 else -1
        position_list = []
        for i in range(3):
            for j in range(3):
                #if self.board_state[(i,j)] == chess_color:
                fit_color_count = 0
                position_list = []
                click_fit_flag = 0
                for rel_XY in rel_XY_list:
                    check_X, check_Y = utils.add_tuple((i,j), rel_XY)
                    if check_X<0 or check_X>2 or check_Y<0 or check_Y>2:
                        position_list = []
                        break
                    if self.board_state[check_X, check_Y] != -chess_color:
                        position_list = []
                        break
                    # print("fit_color_count: ", fit_color_count)
                    position_list.append((check_X, check_Y))
                    fit_color_count += 1
                    if target_position == (check_X, check_Y): click_fit_flag = 1
                    if fit_color_count == selected_shape_size:
                        if click_fit_flag == 1:
                            # print("Find fit shape")
                            return position_list
                        else:
                            position_list = []
                            break

        return position_list


    def next_turn(self):
        self.turn += 1


    def update_convert_shape_selected(self, area_index, player_id):
        self.shape_area_selected_index = area_index
        if area_index == -1:
            self.convert_shape_selected = -1
            return True
        shape_count = 0
        player = self.player1 if player_id == 1 else self.player2
        for i in range(9):  # convert area_index to convert_shape_selected
            if player.collected_flag[i, 0] == 1:
                shape_count += 1
                if shape_count > area_index:
                    self.convert_shape_selected = i
                    return True
        self.convert_shape_selected = -1
        return False
