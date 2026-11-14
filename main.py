import pygame, sys
from pygame.locals import *
import pygame.freetype
import asyncio

aspeed = 5
bspeed = 5
WINWIDTH = 800
WINHEIGHT = 500
CAPTION = "Easy Mode"
YELLOW = (252, 236, 3)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (16, 201, 28)
AQUA = (50, 237, 234)
BLUE = (12, 19, 207)
WHITE = (255, 255, 255)

score = 0
lives = 3

pygame.init()
pygame.freetype.init()

fpsClock = pygame.time.Clock()
mySurface = pygame.display.set_mode((WINWIDTH, WINHEIGHT), 0, 32)
pygame.display.set_caption(CAPTION)

def makePygameFont(message, size, colour, xPos, yPos):
    font = pygame.freetype.Font(None, size)
    text = font.render(message, colour)
    textpos = text[1]
    textpos.centerx = xPos
    textpos.centery = yPos
    mySurface.blit(text[0], textpos)

def makePygameRectangle(colour, xPos, yPos, width, height):
    myRect = pygame.Rect(xPos, yPos, width, height)
    pygame.draw.rect(mySurface, colour, myRect)
    return myRect

def events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

async def main():
    global aspeed, bspeed, score, lives
    
    x = 0
    y = 425
    a = 200
    b = 200
    L = True

    left = pygame.image.load("download.png").convert_alpha()
    left = pygame.transform.scale(left, (67, 75))

    right = pygame.image.load("hi.png").convert_alpha()
    right = pygame.transform.scale(right, (67, 75))

    blocks = []
    colours = [RED, YELLOW, GREEN, AQUA, BLUE]

    for row in range(5):
        for col in range(5):
            block = pygame.Rect(40 + col * 150, 30 + row * 40, 120, 30)
            blocks.append([block, colours[row]])

    while True: 
        mySurface.fill(BLACK)
        events()
        key = pygame.key.get_pressed()

        if lives > 0:
            if key[K_LEFT]:
                x = x - 10
                L = True
            if key[K_RIGHT]:
                x = x + 10
                L = False
            if x < 0:
                x = 0
            if x > WINWIDTH - 67:
                x = WINWIDTH - 67

            if L:
                mySurface.blit(left, (x, y))
                makePygameRectangle(RED, x-13, y-5, 100, 15)
            else:
                mySurface.blit(right, (x, y))
                makePygameRectangle(RED, x-13, y-5, 100, 15)

            pygame.draw.ellipse(mySurface, (255, 255, 255), (a, b, 40, 40))

            a += aspeed
            b += bspeed

            if a >= 760 or a <= 0:
                aspeed *= -1
            if b <= 0:
                bspeed *= -1
            if (b >= y-45 and b <= y) and (a+40 >= x-13 and a <= x+87) and bspeed > 0:
                bspeed *= -1

            ballRect = pygame.Rect(a, b, 40, 40)

            for block in blocks[:]:
                if ballRect.colliderect(block[0]):
                    blocks.remove(block)
                    bspeed *= -1
                    score += 10
                    break
                
            if b > WINHEIGHT:
                lives -= 1
                a = 200
                b = 200
                aspeed = 5
                bspeed = 5

            for block in blocks:
                pygame.draw.rect(mySurface, block[1], block[0])

            makePygameRectangle(RED, x-13, y-5, 100, 15)
            makePygameFont("Score: " + str(score), 25, WHITE, 80, 475)
            makePygameFont("Lives: " + str(lives), 25, WHITE, 720, 475)
            if lives <= 0:
                makePygameFont("GAME OVER", 60, RED, 400, 250)
            if len(blocks) == 0:
                makePygameFont("YOU WIN!", 60, GREEN, 400, 250)

        else:
            makePygameFont("GAME OVER", 60, RED, 400, 250)
            makePygameFont("Final Score: " + str(score), 30, WHITE, 400, 310)

        fpsClock.tick(30)
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
