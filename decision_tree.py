import copy
import numpy as np
from classes import Pion, Cavalier, Fou, Tour, Dame, Roi


def get_score(own_pieces, adv_pieces):
    # to get value of a certain board position
    score = 0
    for piece in adv_pieces:
        score = score - piece.material_value + piece.position_value[piece.x_pos, piece.y_pos]
    for piece in own_pieces:
        score = score + piece.material_value + piece.position_value[piece.x_pos, piece.y_pos]
    return score


def minimax_alpha_beta_pruning(own_pieces, adv_pieces, depth, isMaximizingPlayer, alpha, beta):

    # if node is a leaf node :
    # return value of the node
    if depth == 2:
        return get_score(own_pieces, adv_pieces)

    bestVal = -9999999
    L_score = []
    if isMaximizingPlayer:

        # for each child
        for i, piece in enumerate(own_pieces):
            print('-', end ='')
            
            piece.get_final_deplacements(own_pieces, adv_pieces)
            initial_class_name = piece.__class__.__name__
            (a, b) = (piece.x_pos, piece.y_pos)

            for pos in piece.possible_deplacements:
                one_removed = False
                piece.move(pos[0], pos[1], own_pieces, adv_pieces)

                for k, w_piece in enumerate(adv_pieces):
                    if (w_piece.x_pos, w_piece.y_pos) == (pos[0], pos[1]):
                        removed = adv_pieces.pop(k)
                        one_removed = True
                        break

                score_i = minimax_alpha_beta_pruning(adv_pieces, own_pieces, depth + 1, False, alpha, beta)

                if one_removed is False:
                    k = None

                if depth == 0:
                    L_score.append([score_i, i, pos, k])

                # restablish ancient config
                if one_removed:
                    adv_pieces.insert(k, removed)
                if str(piece.__class__.__name__) == 'Dame' and str(initial_class_name) == 'Pion' and piece.y_pos in [0, 7]:
                    piece.__class__ = Pion
                    piece.picture = 0
                (piece.x_pos, piece.y_pos) = (a, b)
                bestVal = max(bestVal, score_i)
                alpha = max(alpha, bestVal)
                if beta <= alpha and depth > 1:
                    return bestVal

    if isMaximizingPlayer is False:
        bestVal = -bestVal

        # for each child
        for i, piece in enumerate(own_pieces):
            piece.get_final_deplacements(own_pieces, adv_pieces)
            initial_class_name = piece.__class__.__name__

            for pos in piece.possible_deplacements:
                one_removed = False
                (a, b) = (piece.x_pos, piece.y_pos)
                piece.move(pos[0], pos[1], own_pieces, adv_pieces)

                for k, w_piece in enumerate(adv_pieces):
                    if (w_piece.x_pos, w_piece.y_pos) == (pos[0], pos[1]):
                        removed = adv_pieces.pop(k)
                        one_removed = True
                        break

                score_i = minimax_alpha_beta_pruning(adv_pieces, own_pieces, depth + 1, True, alpha, beta)

                if one_removed is False:
                    k = None

                if depth == 0:
                    L_score.append([score_i, i, pos, k])

                if one_removed:
                    adv_pieces.insert(k, removed)
                if str(piece.__class__.__name__) == 'Dame' and str(initial_class_name) == 'Pion' and piece.y_pos in [0, 7]:
                    piece.__class__ = Pion
                    piece.picture = 0
                (piece.x_pos, piece.y_pos) = (a, b)

                bestVal = min(bestVal, score_i)
                alpha = min(alpha, bestVal)
                if beta <= alpha and depth > 1:
                    return bestVal

    if depth == 0:
        return np.array(L_score)

    return bestVal

def final_decision(own_pieces, adv_pieces):
    print('[', end='')
    L = minimax_alpha_beta_pruning(own_pieces, adv_pieces , 0, True, -9999999, +9999999)
    print(']')
    index_max_posi = np.argmax(L[:,0])
    max_score, index_piece, final_position, index_white_to_remove = L[index_max_posi]
    return max_score, index_piece, final_position, index_white_to_remove





