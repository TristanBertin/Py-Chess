import pygame
import numpy as np
from classes import Pion, Cavalier, Fou, Tour, Dame, Roi
from classes import real_pos, get_deplacement_list
import os

pygame.init()
w_height = 600
w_width = 600
case_dim = w_width//8
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 70)
win = pygame.display.set_mode((w_width+200,w_width))
pygame.display.set_caption("First Game")

new_game_button = pygame.Rect(630, 150, 140, 50)
font = pygame.font.SysFont('Arial', 25)

circles = [pygame.image.load('pieces_pic/circle__1.PNG'),
           pygame.image.load('pieces_pic/circle_0.PNG'),
            pygame.image.load('pieces_pic/circle_1.PNG'),
            pygame.image.load('pieces_pic/circle_2.PNG'),
            pygame.image.load('pieces_pic/circle_3.PNG'),
            pygame.image.load('pieces_pic/circle_4.PNG'),
           pygame.image.load('pieces_pic/circle_3.PNG'),
           pygame.image.load('pieces_pic/circle_2.PNG'),
           pygame.image.load('pieces_pic/circle_1.PNG'),
           pygame.image.load('pieces_pic/circle_0.PNG'),]

anim_count = 0

def new_game():

    global alive_pieces_white
    global alive_pieces_black
    global white_score
    global black_score
    global already_selected
    global run
    global white_turn
    global white_chess
    global black_chess
    global potential_depla
    global final_mate

    alive_pieces_white = [Roi(4,7,0,5), Pion(0,6,0,0),Pion(1, 6, 0, 0),Pion(2, 6, 0, 0),Pion(3, 6, 0, 0),Pion(4, 6, 0, 0),Pion(5, 6, 0, 0),Pion(6, 6, 0, 0),Pion(7, 6, 0, 0),
                          Cavalier(1,7,0,1),Cavalier(6,7,0,1),
                          Fou(2,7,0,2),Fou(5,7,0,2),
                          Tour(0,7,0,3),Tour(7,7,0,3),
                          Dame(3,7,0,4)]

    alive_pieces_black = [Roi(4,0,1,5), Pion(0,1,1,0),Pion(1, 1, 1, 0),Pion(2, 1, 1, 0),Pion(3, 1, 1, 0),Pion(4, 1, 1, 0),Pion(5, 1, 1, 0),Pion(6, 1, 1, 0),Pion(7, 1, 1, 0),
                          Cavalier(1,0,1,1),Cavalier(6,0,1,1),
                          Fou(2,0,1,2),Fou(5,0,1,2),
                          Tour(0,0,1,3),Tour(7,0,1,3),
                          Dame(3,0,1,4)]

    black_score = 0
    white_score = 0
    already_selected = 0
    run = True
    white_turn = 1

    black_chess = False
    white_chess = False
    potential_depla = []
    final_mate = False


def check_chess(own_list, adv_list):
    '''check the own chess'''

    L = []

    for piece in adv_list:
        piece.get_possible_deplacements(adv_list, own_list)
        L.append(piece.possible_deplacements)

    L = [piece[i] for piece in L for i in range(len(piece))]

    if [own_list[0].x_pos, own_list[0].y_pos] in L :
        return True

    else:
        return False


def check_mate(own_list, adv_list):

    mate = True
    for piece in own_list:
        piece.get_final_deplacements(own_list, adv_list)
        if len(piece.possible_deplacements) > 0:
            mate=False
            break
    return mate


new_game()


while run:
    pygame.time.delay(100)

    white_pieces_pos = np.array([[[piece.x_pos, piece.y_pos] for piece in alive_pieces_white]])
    black_pieces_pos = np.array([[[piece.x_pos, piece.y_pos] for piece in alive_pieces_black]])

    if already_selected == 1:
        anim_count += 0.5
        if anim_count == 10:
            anim_count =0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run =False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]//case_dim
            mouse_y = pos[1]//case_dim

            if new_game_button.collidepoint(pos): # new Game
                new_game()

            if final_mate == False:

                if already_selected==0:

                    pos = pygame.mouse.get_pos()

                    for piece in alive_pieces_white :
                        if white_turn == 1:
                            if pos[0] > piece.rect.center[0] - piece.rect.size[0] // 2 and pos[0] < piece.rect.center[0] + piece.rect.size[0] // 2:
                                if pos[1] > piece.rect.center[1] - piece.rect.size[1]//2 and pos[1] < piece.rect.center[1] + piece.rect.size[1]//2:
                                    piece.activated = 1
                                    already_selected = 1
                                    piece.get_final_deplacements(alive_pieces_white,alive_pieces_black)
                                    for pos in piece.possible_deplacements:
                                        potential_depla.append([real_pos[pos[0],pos[1],0], real_pos[pos[0],pos[1],1]])


                    for piece in alive_pieces_black :

                        if white_turn == 0:
                            if pos[0] > piece.rect.center[0] - piece.rect.size[0] // 2 and pos[0] < piece.rect.center[0] + piece.rect.size[0] // 2:
                                if pos[1] > piece.rect.center[1] - piece.rect.size[1]//2 and pos[1] < piece.rect.center[1] + piece.rect.size[1]//2:
                                    piece.activated = 1
                                    already_selected = 1
                                    piece.get_final_deplacements(alive_pieces_black,alive_pieces_white)
                                    for pos in piece.possible_deplacements:
                                        potential_depla.append([real_pos[pos[0],pos[1],0], real_pos[pos[0],pos[1],1]])





                elif already_selected == 1:

                    for piece in alive_pieces_white + alive_pieces_black :
                        if piece.activated == 1 :

                            previous_pos = (piece.x_pos,piece.y_pos)

                            if piece.player == 0:
                                piece.move(mouse_x, mouse_y, alive_pieces_white, alive_pieces_black)
                                piece.actualize_move()

                            if piece.player==1:
                                piece.move(mouse_x, mouse_y, alive_pieces_black, alive_pieces_white)
                                piece.actualize_move()

                            if (piece.x_pos,piece.y_pos) != previous_pos:  #has moved

                                white_pieces_pos = np.array([[[piece.x_pos, piece.y_pos] for piece in alive_pieces_white]])
                                black_pieces_pos = np.array([[[piece.x_pos, piece.y_pos] for piece in alive_pieces_black]])

                                if piece.player==0:
                                    for i, b_piece in enumerate(alive_pieces_black):
                                        if (mouse_x, mouse_y) == (b_piece.x_pos, b_piece.y_pos):
                                            alive_pieces_black.pop(i)
                                            white_score += b_piece.value
                                    if check_mate(alive_pieces_black, alive_pieces_white) == True:
                                        final_mate = True

                                if piece.player==1:
                                    for i, w_piece in enumerate(alive_pieces_white):
                                        if (mouse_x, mouse_y) == (w_piece.x_pos, w_piece.y_pos):
                                            alive_pieces_white.pop(i)
                                            black_score += w_piece.value
                                    if check_mate(alive_pieces_white, alive_pieces_black) == True:
                                        final_mate = True

                                white_turn = abs(white_turn - 1)

                            potential_depla=[]
                            piece.activated = 0
                            already_selected = 0


    win.fill((200, 200, 200,))
    color_rect = (80,80,80)
    for i in range(0,8):
        for j in range(0,8):
            if i%2==0:
                if j%2==1:
                    pygame.draw.rect(win, color_rect, (i*case_dim, j*case_dim, case_dim, case_dim))
            else:
                if j%2==0:
                    pygame.draw.rect(win, color_rect, (i * case_dim, j * case_dim, case_dim, case_dim))

    # pygame.draw.circle(win, (123,255,172), (real_pos[i,j,0], real_pos[i,j,1]), 10)
    for b_piece in alive_pieces_black:
        b_piece.draw(win)
    for w_piece in alive_pieces_white:
        w_piece.draw(win)

    pygame.draw.rect(win, (23, 125, 210), new_game_button)  # draw button

    pygame.draw.line(win, (125,123,253), (601,0), (601,600), 4)

    w_score_text = font.render("White Score : %d" % white_score, False, (54, 54, 54))
    w_score_rect = w_score_text.get_rect(center=(685, 300))
    b_score_text = font.render("Black Score : %d" % black_score, False, (54, 54, 54))
    b_score_rect = w_score_text.get_rect(center=(685, 350))
    new_game_text = font.render("NEW GAME", False, (54, 54, 54))
    new_game_rect = new_game_text.get_rect(center=(700, 175))

    for pos in potential_depla:
        image = circles[int(anim_count)%10]
        image_rect = image.get_rect(center=(pos[0], pos[1]))
        win.blit(image, image_rect)
        # pygame.draw.circle(win, (233,34,172), (pos[0], pos[1]), 5)

    win.blit(b_score_text, b_score_rect)
    win.blit(w_score_text, w_score_rect)
    win.blit(new_game_text, new_game_rect)

    if final_mate:

        loose_text = myfont.render("YOU LOOSE", False, (255, 160, 16))
        loose_rect = loose_text.get_rect(center=(300, 300))
        win.blit(loose_text, loose_rect)




            # textsurface = myfont.render('%d,%d'%(i,j), False, (152, 235, 0))
            # win.blit(textsurface, (A[i,j,0], A[i,j,1]))

    # run=False

    pygame.display.update()




