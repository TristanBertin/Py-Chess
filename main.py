import pygame
pygame.init()

win = pygame.display.set_mode((500,500))

pygame.display.set_caption("First Game")

x = 250
y = 250
width = 40
height = 60
vel = 5
isJump = False
jumpcount = 10

run=True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run =False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x = x - vel

    if keys[pygame.K_RIGHT] and x < 495-width:
        x = x + vel

    if not isJump:
        if keys[pygame.K_UP] and y > vel:
            y = y - vel

        if keys[pygame.K_DOWN] and y < 495 - height:
            y = y + vel

        if keys[pygame.K_SPACE]:
            isJump = True
            jumpcount = 10
            init_y = y
    else:
        if jumpcount >= -10 :
            print(jumpcount > -10)
            if jumpcount < 0 :
                y += (jumpcount**2) * 0.5
            else :
                y -= (jumpcount**2) * 0.5
            jumpcount -= 1
            print(jumpcount)

        else:
            isJump = False
            jumpcount = 10


    win.fill((4,4,0,0))
    pygame.draw.rect(win, (255,0,0), (x,y,width,height))
    pygame.display.update()


pygame.quit()







