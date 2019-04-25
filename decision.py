
import numpy as np


def get_score(white_pieces, black_pieces):
    score = 0
    for piece in white_pieces:
        score = score - piece.value - piece.position_value
    for piece in black_pieces:
        score = score + piece.value
    return score


def decision(white_pieces, black_pieces):

    white_pieces_pos = np.array([[[piece.x_pos, piece.y_pos] for piece in white_pieces]])
    black_pieces_pos = np.array([[[piece.x_pos, piece.y_pos] for piece in black_pieces]])
    L_score = []
    white_to_remove = []


    for i,piece in enumerate(black_pieces):
        L_score.append([])
        white_to_remove.append([])
        piece.get_final_deplacements(black_pieces, white_pieces)

        for pos in piece.possible_deplacements:
            white_removed = False
            piece.move(pos[0], pos[1], black_pieces, white_pieces)

            white_pieces_new = white_pieces.copy()
            black_pieces_new = black_pieces.copy()

            for k, w_piece in enumerate(white_pieces):
                if (w_piece.x_pos, w_piece.y_pos) == (pos[0], pos[1]):
                    white_pieces_new.pop(k)
                    white_to_remove[i].append(k)
                    white_removed = True

            L_score[i].append(get_score(white_pieces_new, black_pieces_new))

            if white_removed == False:
                white_to_remove[i].append(-1)
            piece.undo_move()

    max_value, max_index = max((x, (i, j))
                               for i, row in enumerate(L_score)
                               for j, x in enumerate(row))
    print(L_score)
    print(white_to_remove)

    if white_to_remove[max_index[0]][max_index[1]]==-1:
        white_to_remove = None
    else:
        white_to_remove = white_to_remove[max_index[0]][max_index[1]]


    print('sfdddddddddddddddddddddddddddddddd', white_to_remove)

    return (max_value, max_index[0], black_pieces[max_index[0]].possible_deplacements[max_index[1]], white_to_remove)
