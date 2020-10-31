import copy
import numpy as np
import pygame


w_height = 600
w_width = 600
case_dim = w_width//8
number_activation = 0
sign = lambda a: (a>0) - (a<0)

def pos(i,j):
    # from index (i,j) to absolute position (x,y) on board
    x = (i + 1 / 2) * case_dim
    y = (j + 1 / 2) * case_dim
    return (x,y)


def check_chess(own_list, adv_list):
    '''check the own chess'''

    own_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in own_list])
    adv_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in adv_list])

    L = []

    for piece in adv_list:
        sub = piece.get_possible_deplacements_without_chess(adv_list, own_list)
        L.append(sub)

    L = [piece[i] for piece in L for i in range(len(piece))]

    if [own_list[0].x_pos, own_list[0].y_pos] in L :
        return True

    else:
        return False



real_pos = np.array([[pos(i,j) for i in range(8)]for j in range(8)]).astype(int)
real_pos = np.swapaxes(real_pos,0,1)


black_pieces_pic = [pygame.image.load('pieces_pic/b_pion.PNG'),
                    pygame.image.load('pieces_pic/b_cav.PNG'),
                    pygame.image.load('pieces_pic/b_fou.PNG'),
                    pygame.image.load('pieces_pic/b_tour.PNG'),
                    pygame.image.load('pieces_pic/b_reine.PNG'),
                    pygame.image.load('pieces_pic/b_roi.PNG')]

white_pieces_pic = [pygame.image.load('pieces_pic/w_pion.PNG'),
                    pygame.image.load('pieces_pic/w_cav.PNG'),
                    pygame.image.load('pieces_pic/w_fou.PNG'),
                    pygame.image.load('pieces_pic/w_tour.PNG'),
                    pygame.image.load('pieces_pic/w_reine.PNG'),
                    pygame.image.load('pieces_pic/w_roi.PNG')]



def is_movement(move):
    #wrapper that check that you don't move the piece to its initial position
    def wrapper(*args):
        if args[0].x_pos == args[1] and args[0].y_pos == args[2] :
            pass
        else:
            move(*args)
    return wrapper


class Piece:
    def __init__(self,x,y,player, picture):
        self.x_pos = x
        self.y_pos = y
        self.x_pos_past = x
        self.y_pos_past = y
        self.player = player
        self.picture = picture
        self.rect = white_pieces_pic[self.picture].get_rect()
        self.rect.center = real_pos[self.x_pos, self.y_pos]
        self.activated = 0
        self.possible_deplacements = None

    def __delete__(self, instance):
        del self

    def actualize_picture(self):
        self.rect = white_pieces_pic[self.picture].get_rect()
        self.rect.center = real_pos[self.x_pos, self.y_pos]

    def draw(self,window):
        if self.player == 0 :
            window.blit(white_pieces_pic[self.picture], self.rect)
        if self.player == 1 :
            window.blit(black_pieces_pic[self.picture], self.rect)
        if self.activated == 1:
            pygame.draw.circle(window, (123, 255, 172), self.rect.center, 9)

    def actualize_move(self):
        self.y_pos_past = self.y_pos
        self.x_pos_past = self.x_pos
        self.rect = white_pieces_pic[self.picture].get_rect()
        self.rect.center = real_pos[self.x_pos, self.y_pos]

    def undo_move(self):
        self.y_pos = self.y_pos_past
        self.x_pos = self.x_pos_past

    def get_deplacement_list(self, x_i, y_i, x_f, y_f):
        #get list of visited states between initial position and final one

        if self.__class__.__name__ not in  ['Cavalier', 'Pion']:
            # intermediary states don't need to be taken into account for Cavalier and Pion

            L = []
            x = x_i
            y = y_i

            while (x,y) != (x_f, y_f):
                if (x_f - x_i)==0:
                    x = x_i
                    y = y + int((y_f - y_i) / abs(y_f - y_i))
                    L.append([x,y])

                if (y_f-y_i)==0:
                    x = x + int((x_f - x_i) / abs(x_f - x_i))
                    y = y_i
                    L.append([x, y])

                if (y_f-y_i)!=0 and (x_f-x_i)!=0 :
                    x = x + int((x_f - x_i)/abs(x_f - x_i))
                    y = y + int((y_f - y_i)/abs(y_f - y_i))
                    L.append([x, y])

            if len(L)!=0:
                L.pop(-1)

        else:
            L = []
            
        return L


    def get_final_deplacements(self, own_list, adv_list):
        # check all possible moves that respect the mobility of the desired piece 
        # but also that there is no checkmate involved 

        list_of_possible_deplacements = self.get_possible_deplacements_without_chess(own_list, adv_list)

        x_pos_past = copy.deepcopy(self.x_pos)
        y_pos_past = copy.deepcopy(self.y_pos)
        final_possible_depla = []

        for pos_dep in list_of_possible_deplacements:

            self.x_pos = pos_dep[0]
            self.y_pos = pos_dep[1]

            in_advserse_pos = False
            for k, adv_piece in enumerate(adv_list):  #we tcheck after removing adverse piece if checkmate
                if (self.x_pos, self.y_pos) == (adv_piece.x_pos, adv_piece.y_pos):
                    deleted_element = adv_list.pop(k)

                    if check_chess(own_list, adv_list) == False:
                        final_possible_depla.append([self.x_pos, self.y_pos])

                    adv_list.insert(k, deleted_element)
                    in_advserse_pos = True
                    break

            if in_advserse_pos == False:
                if check_chess(own_list, adv_list) == False:
                    final_possible_depla.append([self.x_pos, self.y_pos])

            self.x_pos = x_pos_past
            self.y_pos = y_pos_past

        self.possible_deplacements = final_possible_depla




class Pion(Piece):
    def __init__(self,x,y,player, picture):
        Piece.__init__(self, x,y,player, picture)
        self.material_value = 100
        self.position_value = np.array([[0,  0,  0,  0,  0,  0,  0,  0],
                                        [50, 50, 50, 50, 50, 50, 50, 50],
                                        [10, 10, 20, 30, 30, 20, 10, 10],
                                        [ 5,  5, 10, 25, 25, 10,  5,  5],
                                        [ 0,  0,  0, 20, 20,  0,  0,  0],
                                        [ 5, -5,-10,  0,  0,-10, -5,  5],
                                        [ 5, 10, 10,-20,-20, 10, 10,  5],
                                        [ 0,  0,  0,  0,  0,  0,  0,  0]])
        if self.player == 1:
            self.position_value = np.flip(self.position_value, axis = 0)


    def get_possible_deplacements_without_chess(self,own_list,adv_list):

        own_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in own_list])
        adv_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in adv_list])

        L=[]

        for i in range(8):
            for j in range(8):
                (x_fin, y_fin) = (i,j)
                if ([x_fin, y_fin] not in own_pieces_pos.tolist()):

                    if self.player == 0:

                        if (((self.y_pos ==6 and y_fin==4) and (x_fin==self.x_pos)) and ([x_fin, y_fin] not in adv_pieces_pos.tolist())) or \
                            (y_fin == self.y_pos - 1 and x_fin == self.x_pos) and ([x_fin, y_fin] not in adv_pieces_pos.tolist()) or \
                            ((self.y_pos-y_fin)==1 and abs((self.x_pos-x_fin) * (y_fin - self.y_pos)) == 1) and ([x_fin, y_fin] in adv_pieces_pos.tolist()):

                            deplacements_list = self.get_deplacement_list(self.x_pos, self.y_pos, x_fin, y_fin)
                            assert_mov = True
                            for intermediary_case in deplacements_list:
                                if (intermediary_case in own_pieces_pos.tolist()) or (intermediary_case in adv_pieces_pos.tolist()):
                                    assert_mov = False

                            if assert_mov:
                                if (i,j) != (self.x_pos, self.y_pos):
                                    L.append([i, j])


                    if self.player == 1:

                        if (((self.y_pos ==1 and y_fin==3) and (x_fin==self.x_pos))and ([x_fin, y_fin] not in adv_pieces_pos.tolist())) or \
                                (y_fin == self.y_pos + 1 and x_fin == self.x_pos and ([x_fin, y_fin] not in adv_pieces_pos.tolist())) or \
                                (((self.y_pos - y_fin) == -1 and abs((self.x_pos - x_fin) * (y_fin - self.y_pos)) == 1) and ([x_fin, y_fin] in adv_pieces_pos.tolist())):

                            deplacements_list = self.get_deplacement_list(self.x_pos, self.y_pos, x_fin, y_fin)
                            assert_mov = True
                            for intermediary_case in deplacements_list:
                                if (intermediary_case in own_pieces_pos.tolist()) or (intermediary_case in adv_pieces_pos.tolist()):
                                    assert_mov = False
                            if assert_mov:
                                if (i,j) != (self.x_pos, self.y_pos):
                                    L.append([i, j])

        return L


    def move(self,x_fin, y_fin, own_list, adv_list):

        self.get_final_deplacements(own_list, adv_list)

        if [x_fin, y_fin] in self.possible_deplacements:
            self.y_pos = y_fin
            self.x_pos = x_fin

            if self.y_pos == 0 or self.y_pos==7:  # DAME
                self.__class__ = Dame
                self.picture = 4



class Cavalier(Piece):
    def __init__(self,x,y,player, picture):
        Piece.__init__(self, x,y,player, picture)
        self.material_value = 320
        self.position_value = np.array([[-50,-40,-30,-30,-30,-30,-40,-50],
                                        [-40,-20,  0,  0,  0,  0,-20,-40],
                                        [-30,  0, 10, 15, 15, 10,  0,-30],
                                        [-30,  5, 15, 20, 20, 15,  5,-30],
                                        [-30,  0, 15, 20, 20, 15,  0,-30],
                                        [-30,  5, 10, 15, 15, 10,  5,-30],
                                        [-40,-20,  0,  5,  5,  0,-20,-40],
                                        [-50,-40,-30,-30,-30,-30,-40,-50]])
        if self.player == 1:
            self.position_value = np.flip(self.position_value, axis = 0)


    def get_possible_deplacements_without_chess(self, own_list, adv_list):

        own_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in own_list])

        L = []

        for i in range(8):
            for j in range(8):
                (x_fin, y_fin) = (i, j)
                if ([x_fin, y_fin] not in own_pieces_pos.tolist()):
                    if (abs(x_fin - self.x_pos) == 2 and abs(y_fin - self.y_pos) == 1) or (
                            (abs(y_fin - self.y_pos) == 2) and (abs(x_fin - self.x_pos) == 1)):
                        if (i,j) != (self.x_pos, self.y_pos):
                            L.append([i, j])

        return L

    def move(self, x_fin, y_fin, own_list, adv_list):

        self.get_final_deplacements(own_list, adv_list)

        if [x_fin, y_fin] in self.possible_deplacements:
            self.y_pos = y_fin
            self.x_pos = x_fin



class Fou(Piece):
    def __init__(self,x,y,player, picture):
        Piece.__init__(self, x,y,player, picture)
        self.material_value = 330
        self.position_value = np.array([[-20,-10,-10,-10,-10,-10,-10,-20],
                                        [-10,  0,  0,  0,  0,  0,  0,-10],
                                        [-10,  0,  5, 10, 10,  5,  0,-10],
                                        [-10,  5,  5, 10, 10,  5,  5,-10],
                                        [-10,  0, 10, 10, 10, 10,  0,-10],
                                        [-10, 10, 10, 10, 10, 10, 10,-10],
                                        [-10,  5,  0,  0,  0,  0,  5,-10],
                                        [-20,-10,-10,-10,-10,-10,-10,-20]])
        if self.player == 1:
            self.position_value = np.flip(self.position_value, axis = 0)

    def get_possible_deplacements_without_chess(self, own_list, adv_list):

        own_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in own_list])
        adv_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in adv_list])

        L = []
        for i in range(8):
            for j in range(8):
                (x_fin, y_fin) = (i, j)
                if (([x_fin, y_fin] not in own_pieces_pos.tolist()) and (
                        abs(y_fin - self.y_pos) == abs(x_fin - self.x_pos))):
                    deplacements_list = self.get_deplacement_list(self.x_pos, self.y_pos, x_fin, y_fin)
                    assert_mov = True
                    for intermediary_case in deplacements_list:
                        if (intermediary_case in own_pieces_pos.tolist()) or (
                                intermediary_case in adv_pieces_pos.tolist()):
                            assert_mov = False
                    if assert_mov:
                        if (i,j) != (self.x_pos, self.y_pos):
                            L.append([i, j])

        return L

    def move(self, x_fin, y_fin, own_list, adv_list):

        self.get_final_deplacements(own_list, adv_list)

        if [x_fin, y_fin] in self.possible_deplacements:
            self.y_pos = y_fin
            self.x_pos = x_fin






class Tour(Piece):
    def __init__(self,x,y,player, picture):
        Piece.__init__(self, x,y,player, picture)
        self.material_value = 500
        self.position_value = np.array([[0,  0,  0,  0,  0,  0,  0,  0],
                                      [5, 10, 10, 10, 10, 10, 10,  5],
                                     [-5,  0,  0,  0,  0,  0,  0, -5],
                                     [-5,  0,  0,  0,  0,  0,  0, -5],
                                     [-5,  0,  0,  0,  0,  0,  0, -5],
                                     [-5,  0,  0,  0,  0,  0,  0, -5],
                                     [-5,  0,  0,  0,  0,  0,  0, -5],
                                      [0,  0,  0,  5,  5,  0,  0,  0]])
        if self.player == 1:
            self.position_value = np.flip(self.position_value, axis = 0)

    def get_possible_deplacements_without_chess(self, own_list, adv_list):

        own_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in own_list])
        adv_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in adv_list])

        L = []
        for i in range(8):
            for j in range(8):
                (x_fin, y_fin) = (i, j)
                if ([x_fin, y_fin] not in own_pieces_pos.tolist()) and (
                        (self.x_pos == x_fin) or (self.y_pos == y_fin)):
                    deplacements_list = self.get_deplacement_list(self.x_pos, self.y_pos, x_fin, y_fin)
                    assert_mov = True
                    for intermediary_case in deplacements_list:
                        if (intermediary_case in own_pieces_pos.tolist()) or (
                                intermediary_case in adv_pieces_pos.tolist()):
                            assert_mov = False

                    if assert_mov:
                        if (i,j) != (self.x_pos, self.y_pos):
                            L.append([i, j])

        return L

    def move(self, x_fin, y_fin, own_list, adv_list):

        self.get_final_deplacements(own_list, adv_list)

        if [x_fin, y_fin] in self.possible_deplacements:
            self.y_pos = y_fin
            self.x_pos = x_fin



class Dame(Piece):
    def __init__(self,x,y,player, picture):
        Piece.__init__(self, x,y,player, picture)
        self.material_value = 900
        self.position_value = np.array([[-20,-10,-10, -5, -5,-10,-10,-20],
                                        [-10,  0,  0,  0,  0,  0,  0,-10],
                                        [-10,  0,  5,  5,  5,  5,  0,-10],
                                        [ -5,  0,  5,  5,  5,  5,  0, -5],
                                        [  0,  0,  5,  5,  5,  5,  0, -5],
                                        [-10,  5,  5,  5,  5,  5,  0,-10],
                                        [-10,  0,  5,  0,  0,  0,  0,-10],
                                        [-20,-10,-10, -5, -5,-10,-10,-20]])
        if self.player == 1:
            self.position_value = np.flip(self.position_value, axis = 0)

    def get_possible_deplacements_without_chess(self, own_list, adv_list):

        own_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in own_list])
        adv_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in adv_list])

        L = []
        for i in range(8):
            for j in range(8):
                (x_fin, y_fin) = (i, j)
                if ([x_fin, y_fin] not in own_pieces_pos.tolist()) and (
                        (abs(y_fin - self.y_pos) == abs(x_fin - self.x_pos)) or (self.x_pos == x_fin) or (
                        self.y_pos == y_fin)):

                    deplacements_list = self.get_deplacement_list(self.x_pos, self.y_pos, x_fin, y_fin)
                    assert_mov = True
                    for intermediary_case in deplacements_list:
                        if (intermediary_case in own_pieces_pos.tolist()) or (
                                intermediary_case in adv_pieces_pos.tolist()):
                            assert_mov = False
                    if assert_mov:
                        if (i,j) != (self.x_pos, self.y_pos):
                            L.append([i, j])

        return L

    def move(self, x_fin, y_fin, own_list, adv_list):

        self.get_final_deplacements(own_list, adv_list)

        if [x_fin, y_fin] in self.possible_deplacements:
            self.y_pos = y_fin
            self.x_pos = x_fin






class Roi(Piece):
    def __init__(self,x,y,player, picture):
        Piece.__init__(self, x,y,player, picture)
        self.material_value = 20000
        self.position_value = np.array([[-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-20,-30,-30,-40,-40,-30,-30,-20],
                                        [-10,-20,-20,-20,-20,-20,-20,-10],
                                        [20, 20,  0,  0,  0,  0, 20, 20],
                                        [20, 30, 10,  0,  0, 10, 30, 20]])
        if self.player == 1:
            self.position_value = np.flip(self.position_value, axis = 0)

    def get_possible_deplacements_without_chess(self, own_list, adv_list):

        own_pieces_pos = np.array([[piece.x_pos, piece.y_pos] for piece in own_list])

        L = []

        for i in range(8):
            for j in range(8):
                (x_fin, y_fin) = (i, j)
                if ([x_fin, y_fin] not in own_pieces_pos.tolist()):
                    if abs(y_fin - self.y_pos) in (0, 1) and abs(x_fin - self.x_pos) in (0, 1):
                        if (i,j) != (self.x_pos, self.y_pos):
                            L.append([i, j])

        return L

    def move(self, x_fin, y_fin, own_list, adv_list):

        self.get_final_deplacements(own_list, adv_list)

        if [x_fin, y_fin] in self.possible_deplacements:
            self.y_pos = y_fin
            self.x_pos = x_fin


for i in range(10):
    if i == 2 :
        break

print(i)









