import pygame
import numpy as np
from classes import Pion, Cavalier, Fou, Tour, Dame, Roi
from classes import real_pos, check_mate
from decision_tree import minimax_alpha_beta_pruning, get_score
from decision_tree import final_decision

#Hyper-parameters
w_height = 600
w_width = 600
case_dim = w_width//8
anim_count = 0

#Pygame Window initialization
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 70)
win = pygame.display.set_mode((w_width+300,w_width))
pygame.display.set_caption("Chess Game")
new_game_button = pygame.Rect(660, 250, 180, 50)
font = pygame.font.SysFont('Arial', 25)

#Load all images into memory to speed up the process
circles = [pygame.image.load('pieces_pic/circle__1.PNG'),
           pygame.image.load('pieces_pic/circle_0.PNG'),
            pygame.image.load('pieces_pic/circle_1.PNG'),
            pygame.image.load('pieces_pic/circle_2.PNG'),
            pygame.image.load('pieces_pic/circle_3.PNG'),
            pygame.image.load('pieces_pic/circle_4.PNG'),
           pygame.image.load('pieces_pic/circle_3.PNG'),
           pygame.image.load('pieces_pic/circle_2.PNG'),
           pygame.image.load('pieces_pic/circle_1.PNG'),
           pygame.image.load('pieces_pic/circle_0.PNG')]


def new_game():
	# to initialize a new game

	#reset all global varaibles 
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
    global white_mate
    global black_mate

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
    white_mate = False
    black_mate = False



new_game()


#Infinite pygame loop, waiting for actions/events...
while run:

    pygame.time.delay(100)

    #for the moving circles animation
    if already_selected == 1:
        anim_count += 0.5
        if anim_count == 10:
            anim_count = 0

    #if black turn --> run the AI
    if white_turn == 0 and (white_mate==False and black_mate==False):
        max_score, index_piece, final_position, index_white_to_remove = final_decision(alive_pieces_black, alive_pieces_white)
        alive_pieces_black[index_piece].move(final_position[0], final_position[1], alive_pieces_black, alive_pieces_white)
        alive_pieces_black[index_piece].actualize_move()
        if index_white_to_remove != None:
            a = alive_pieces_white.pop(index_white_to_remove)
        white_turn = 1

    #if white turn => player has to play
    for event in pygame.event.get():

    	# quit
        if event.type == pygame.QUIT:
            run =False

        #store mouse position if click 
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            mouse_x = pos[0]//case_dim
            mouse_y = pos[1]//case_dim

            if new_game_button.collidepoint(pos): # new Game
                new_game()

            #if no checkmate 
            if (white_mate==False) and (black_mate==False):

            	#if no piece is already selected
                if already_selected==0:
                    pos = pygame.mouse.get_pos()

                    for piece in alive_pieces_white :
                        if pos[0] > piece.rect.center[0] - piece.rect.size[0] // 2 and pos[0] < piece.rect.center[0] + piece.rect.size[0] // 2:
                            if pos[1] > piece.rect.center[1] - piece.rect.size[1]//2 and pos[1] < piece.rect.center[1] + piece.rect.size[1]//2:
                                piece.activated = 1
                                already_selected = 1
                                piece.get_final_deplacements(alive_pieces_white,alive_pieces_black)

                                # each element in piece.possible_deplacements will generate a moving circle
                                for pos in piece.possible_deplacements:
                                    potential_depla.append([real_pos[pos[0],pos[1],0], real_pos[pos[0],pos[1],1]])

                #if a piece is already selected
                elif already_selected == 1:

                    for piece in alive_pieces_white :
                        if piece.activated == 1 :

                            previous_pos = (piece.x_pos,piece.y_pos)

                            piece.move(mouse_x, mouse_y, alive_pieces_white, alive_pieces_black)
                            piece.actualize_move()

                            if (piece.x_pos,piece.y_pos) != previous_pos:  #has moved
                                for i, b_piece in enumerate(alive_pieces_black):
                                    if (mouse_x, mouse_y) == (b_piece.x_pos, b_piece.y_pos):
                                        alive_pieces_black.pop(i)
                                        white_score += b_piece.material_value
                                if check_mate(alive_pieces_black, alive_pieces_white) == True:
                                    black_mate = True

                                white_turn = abs(white_turn - 1)

                            potential_depla=[]
                            piece.activated = 0
                            already_selected = 0



    # Window display actualization                      	
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

    for b_piece in alive_pieces_black:
        b_piece.draw(win)
    for w_piece in alive_pieces_white:
        w_piece.draw(win)

    pygame.draw.rect(win, (23, 125, 210), new_game_button)  # draw button
    pygame.draw.line(win, (125,123,253), (601,0), (601,600), 4)

    new_game_text = font.render("NEW GAME", False, (1, 1, 1))
    new_game_rect = new_game_text.get_rect(center=(750, 275))

    for pos in potential_depla:
        image = circles[int(anim_count)%10]
        image_rect = image.get_rect(center=(pos[0], pos[1]))
        win.blit(image, image_rect)

    win.blit(new_game_text, new_game_rect)
    white_mate = check_mate(alive_pieces_white, alive_pieces_black)
    black_mate = check_mate(alive_pieces_black, alive_pieces_white)
    if white_mate :
        loose_text = myfont.render("YOU LOOSE", False, (255, 160, 16))
        loose_rect = loose_text.get_rect(center=(300, 300))
        win.blit(loose_text, loose_rect)
    if black_mate:
        loose_text = myfont.render("YOU WIN", False, (255, 160, 16))
        loose_rect = loose_text.get_rect(center=(300, 300))
        win.blit(loose_text, loose_rect)

    pygame.display.update()




