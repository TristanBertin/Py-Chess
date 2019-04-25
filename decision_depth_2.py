import copy
import numpy as np
from classes import Pion


def get_score(own_pieces, adv_pieces):
    score = 0
    for piece in adv_pieces:
        score = score - piece.material_value - piece.position_value[piece.x_pos, piece.y_pos]
    for piece in own_pieces:
        score = score + piece.material_value + piece.position_value[piece.x_pos, piece.y_pos]
    return score


def sub_decision(own_pieces, adv_pieces):

    L_score = []

    for i,piece in enumerate(own_pieces):
        L_score.append([])
        piece.get_final_deplacements(own_pieces, adv_pieces)

        for pos in piece.possible_deplacements:
            (a,b) = (0,0)
            initial_class = copy.deepcopy(piece.__class__)
            (a,b) = (piece.x_pos, piece.y_pos)
            piece.move(pos[0], pos[1], own_pieces, adv_pieces)

            asser = False
            for k, w_piece in enumerate(adv_pieces):
                if (w_piece.x_pos, w_piece.y_pos) == (pos[0], pos[1]):
                    removed = adv_pieces.pop(k)

                    score_i = get_score(own_pieces, adv_pieces)
                    L_score[i].append(score_i)
                    adv_pieces.insert(k,removed)

                    asser = True
                    break

            if asser == False:

                score_i = get_score(own_pieces, adv_pieces)
                L_score[i].append(score_i)


            if str(piece.__class__.__name__) == 'Dame' and  str(initial_class.__name__)=='Pion' and piece.y_pos in [0,7]:
                print('@@@@@@@@@@@@@', str(piece.__class__.__name__), str(initial_class.__name__), piece.y_pos)
                print('dfd')
                piece.__class__ = Pion
                piece.picture = 0


            (piece.x_pos, piece.y_pos) = (a,b)



    max_value, max_index = max((x, (i, j))
                               for i, row in enumerate(L_score)
                               for j, x in enumerate(row))

    return max_value




def decision_depth_2(own_list, adv_list):

    Mega_Score = []
    print('--------------- New Move ---------------------')

    for m,own_piece_1 in enumerate(own_list):
        print('%d / %d'%(m+1, len(own_list)))
        print('************', own_piece_1.__class__,)

        Mega_Score.append([])
        own_piece_1.get_final_deplacements(own_list, adv_list)

        for h,depla in enumerate(own_piece_1.possible_deplacements):
            initial_class = copy.deepcopy(own_piece_1.__class__)
            initial_pos_x = copy.deepcopy(own_piece_1.x_pos)
            initial_pos_y = copy.deepcopy(own_piece_1.y_pos)

            own_piece_1.move(depla[0], depla[1], own_list, adv_list)
            at_least_one_removed = False

            for k, adv_piece_1 in enumerate(adv_list) :
                if (adv_piece_1.x_pos, adv_piece_1.y_pos) == (depla[0], depla[1]):
                    removed_element = adv_list.pop(k)
                    at_least_one_removed = True
                    score = sub_decision(own_list, adv_list)  #here we invert : best decision for the advserse !!!!!!
                    adv_list.insert(k, removed_element)
                    break

            if at_least_one_removed==False:
                score = sub_decision(adv_list, own_list)

            Mega_Score[m].append(score)


            if str(own_piece_1.__class__.__name__) == 'Dame' and  str(initial_class.__name__)=='Pion' and own_piece_1.y_pos in [0,7]:
                print('@@@@@@@@@@@@@', str(own_piece_1.__class__.__name__), str(initial_class.__name__), own_piece_1.y_pos)
                print('dfd')
                own_piece_1.__class__ = Pion
                own_piece_1.picture = 0

            own_piece_1.x_pos = initial_pos_x
            own_piece_1.y_pos = initial_pos_y

    for i in range(len(Mega_Score)):
        if len(Mega_Score[i])== 0:
            Mega_Score[i].append(100000)


    min_value, min_index = min((x, (i, j))
                               for i, row in enumerate(Mega_Score)
                               for j, x in enumerate(row))

    own_list[min_index[0]].get_final_deplacements(own_list, adv_list)

    final_position = own_list[min_index[0]].possible_deplacements[min_index[1]]

    index_white_to_remove = None

    for p,adv_piece in enumerate(adv_list):
        if adv_piece.x_pos == final_position[0] and adv_piece.y_pos==final_position[1]:
            index_white_to_remove = p

    return (-1000, min_index[0], final_position, index_white_to_remove)




