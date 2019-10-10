import pygame, sys, random
from pygame.locals import *
from random import randint

BOARDWIDTH = 4
BOARDHEIGHT = 4
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 60
BLANK = None

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = ( 0, 50, 255)
DARKTURQUOISE = ( 250, 100, 0)
GREEN = ( 0, 204, 0)
DARKGREEN = (0, 100, 0)
DARKBLUE = (0, 0, 139)
PURPLE = (128, 0, 128)
BURGUNDY = (128, 0, 32)
RED = (255, 0, 0)
PINK = (255, 192, 203)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BROWN = (210, 105, 30)
GOLD = (212, 175, 55)

BGCOLOR = DARKTURQUOISE
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = WHITE
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, UNDO_SURF, UNDO_RECT, NEW_SURF, NEW_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('2048')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, GREEN, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    UNDO_SURF, UNDO_RECT = makeText('Undo Last Move', TEXTCOLOR, GREEN, WINDOWWIDTH - 160, WINDOWHEIGHT - 30)

    mainBoard = getStartingBoard()
    lastMove = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(mainBoard[x][y])
        lastMove.append(column)

    while True: # main game looop
        slideTo = None # the direction all the tiles will slide
        msg = '' # contains the message to show in the upper left corner
        if checkWin(mainBoard):
            msg = 'You Win! :D'
        elif checkLose(mainBoard):
            msg = 'You Lose! :('

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                if (spotx, spoty) == (None, None):
                    if NEW_RECT.collidepoint(event.pos):
                        mainBoard = getStartingBoard()
                    elif UNDO_RECT.collidepoint(event.pos):
                        for x in range(BOARDWIDTH):
                            for y in range(BOARDHEIGHT):
                                mainBoard[x][y] = lastMove[x][y]
            elif event.type == KEYUP:
                for x in range(BOARDWIDTH):
                    for y in range(BOARDHEIGHT):
                        lastMove[x][y] = mainBoard[x][y]
                if event.key in (K_LEFT, K_a):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s):
                    slideTo = DOWN
        if slideTo:
            slideAnimation(mainBoard, slideTo, msg, 32)
            if not mainBoard == lastMove:
                addTile(mainBoard)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeText(text, color, bgcolor, top, left):
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def getStartingBoard():
    board = []
    posOne = [randint(0, 3), randint(0, 3)]
    var = True
    while var:
        posTwo = [randint(0, 3), randint(0, 3)]
        if not posTwo == posOne:
            var = False
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            if x == posOne[0] and y == posOne[1]:
                if randint(1, 10) == 1:
                    column.append(4)
                else:
                    column.append(2)
            elif x == posTwo[0] and y == posTwo[1]:
                if randint(1, 10) == 1:
                    column.append(4)
                else:
                    column.append(2)
            else:
                column.append(0)
        board.append(column)
    return board

def checkWin(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == 2048:
                return True
    return False

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if not board[tilex][tiley] == 0:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(UNDO_SURF, UNDO_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)

def drawTile(tilex, tiley, number, adjx = 0, adjy = 0):
    left, top = getLeftTopOfTile(tilex, tiley)
    if number == 2:
        pygame.draw.rect(DISPLAYSURF, GREEN, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 4:
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 8:
        pygame.draw.rect(DISPLAYSURF, DARKBLUE, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 16:
        pygame.draw.rect(DISPLAYSURF, PURPLE, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 32:
        pygame.draw.rect(DISPLAYSURF, BURGUNDY, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 64:
        pygame.draw.rect(DISPLAYSURF, RED, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 128:
        pygame.draw.rect(DISPLAYSURF, PINK, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 256:
        pygame.draw.rect(DISPLAYSURF, BLACK, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 512:
        pygame.draw.rect(DISPLAYSURF, ORANGE, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 1024:
        pygame.draw.rect(DISPLAYSURF, BROWN, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    if number == 2048:
        pygame.draw.rect(DISPLAYSURF, GOLD, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def terminate():
    pygame.quit()
    sys.exit()

def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board)):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def slideAnimation(mainBoard, direction, message, animationSpeed):
    if direction == UP:
        for x in range(len(mainBoard)):
            for y in range(len(mainBoard)):
                if not mainBoard[x][y] == 0 and not y == 0 and mainBoard[x][y - 1] == 0:
                    drawBoard(mainBoard, message)
                    baseSurf = DISPLAYSURF.copy()
                    moveLeft, moveTop = getLeftTopOfTile(x, y)
                    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
                    for i in range(0, TILESIZE, animationSpeed):
                        checkForQuit()
                        DISPLAYSURF.blit(baseSurf, (0, 0))
                        drawTile(x, y, mainBoard[x][y], 0, -i)
                    mainBoard[x][y - 1] = mainBoard[x][y]
                    mainBoard[x][y] = 0
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    if y > 1 and mainBoard[x][y - 2] == 0:
                        slideAnimation(mainBoard, UP, message, animationSpeed)
                    elif y > 1 and mainBoard[x][y - 1] == mainBoard[x][y - 2]:
                        mergeTiles(mainBoard, UP, x, y, message, animationSpeed)
                elif not mainBoard[x][y] == 0 and not y == 0 and mainBoard[x][y - 1] == mainBoard[x][y]:
                    mergeTiles(mainBoard, UP, x, y + 1, message, animationSpeed)
    elif direction == LEFT:
        for x in range(len(mainBoard)):
            for y in range(len(mainBoard)):
                if not mainBoard[x][y] == 0 and not x == 0 and mainBoard[x - 1][y] == 0:
                    drawBoard(mainBoard, message)
                    baseSurf = DISPLAYSURF.copy()
                    moveLeft, moveTop = getLeftTopOfTile(x, y)
                    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
                    for i in range(0, TILESIZE, animationSpeed):
                        checkForQuit()
                        DISPLAYSURF.blit(baseSurf, (0, 0))
                        drawTile(x, y, mainBoard[x][y], -i, 0)
                    mainBoard[x - 1][y] = mainBoard[x][y]
                    mainBoard[x][y] = 0
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    if x > 1 and mainBoard[x - 2][y] == 0:
                        slideAnimation(mainBoard, LEFT, message, animationSpeed)
                    elif x > 1 and mainBoard[x - 1][y] == mainBoard[x - 2][y]:
                        mergeTiles(mainBoard, LEFT, x, y, message, animationSpeed)
                elif not mainBoard[x][y] == 0 and not x == 0 and mainBoard[x - 1][y] == mainBoard[x][y]:
                    mergeTiles(mainBoard, LEFT, x + 1, y, message, animationSpeed)
    elif direction == RIGHT:
        for x in range(len(mainBoard)):
            for y in range(len(mainBoard)):
                xVal = 3 - x
                if not mainBoard[xVal][y] == 0 and not x == 0 and mainBoard[xVal + 1][y] == 0:
                    drawBoard(mainBoard, message)
                    baseSurf = DISPLAYSURF.copy()
                    moveLeft, moveTop = getLeftTopOfTile(xVal, y)
                    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
                    for i in range(0, TILESIZE, animationSpeed):
                        checkForQuit()
                        DISPLAYSURF.blit(baseSurf, (0, 0))
                        drawTile(xVal, y, mainBoard[xVal][y], i, 0)
                    mainBoard[xVal + 1][y] = mainBoard[xVal][y]
                    mainBoard[xVal][y] = 0
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    if x > 1 and mainBoard[xVal + 2][y] == 0:
                        slideAnimation(mainBoard, RIGHT, message, animationSpeed)
                    elif x > 1 and mainBoard[xVal + 1][y] == mainBoard[xVal + 2][y]:
                        mergeTiles(mainBoard, RIGHT, xVal, y, message, animationSpeed)
                elif not mainBoard[xVal][y] == 0 and not x == 0 and mainBoard[xVal + 1][y] == mainBoard[xVal][y]:
                    mergeTiles(mainBoard, RIGHT, xVal - 1, y, message, animationSpeed)
    elif direction == DOWN:
        for x in range(len(mainBoard)):
            for y in range(len(mainBoard)):
                yVal = 3 - y
                if not mainBoard[x][yVal] == 0 and not y == 0 and mainBoard[x][yVal + 1] == 0:
                    drawBoard(mainBoard, message)
                    baseSurf = DISPLAYSURF.copy()
                    moveLeft, moveTop = getLeftTopOfTile(x, yVal)
                    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
                    for i in range(0, TILESIZE, animationSpeed):
                        checkForQuit()
                        DISPLAYSURF.blit(baseSurf, (0, 0))
                        drawTile(x, yVal, mainBoard[x][yVal], 0, i)
                    mainBoard[x][yVal + 1] = mainBoard[x][yVal]
                    mainBoard[x][yVal] = 0
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    if y > 1 and mainBoard[x][yVal + 2] == 0:
                        slideAnimation(mainBoard, DOWN, message, animationSpeed)
                    elif y > 1 and mainBoard[x][yVal + 1] == mainBoard[x][yVal + 2]:
                        mergeTiles(mainBoard, DOWN, x, yVal, message, animationSpeed)
                elif not mainBoard[x][yVal] == 0 and not y == 0 and mainBoard[x][yVal + 1] == mainBoard[x][yVal]:
                    mergeTiles(mainBoard, DOWN, x, yVal - 1, message, animationSpeed)

def mergeTiles(mainBoard, direction, x, y, message, animationSpeed):
    if direction == UP:
        drawBoard(mainBoard, message)
        baseSurf = DISPLAYSURF.copy()
        moveLeft, moveTop = getLeftTopOfTile(x, y - 1)
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
        for i in range(0, TILESIZE, animationSpeed):
            checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            drawTile(x, y - 1, mainBoard[x][y - 1], 0, -i)
        mainBoard[x][y - 2] *= 2
        mainBoard[x][y - 1] = 0
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    if direction == LEFT:
        drawBoard(mainBoard, message)
        baseSurf = DISPLAYSURF.copy()
        moveLeft, moveTop = getLeftTopOfTile(x - 1, y)
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
        for i in range(0, TILESIZE, animationSpeed):
            checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            drawTile(x - 1, y, mainBoard[x - 1][y], -i, 0)
        mainBoard[x - 2][y] *= 2
        mainBoard[x - 1][y] = 0
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    if direction == RIGHT:
        drawBoard(mainBoard, message)
        baseSurf = DISPLAYSURF.copy()
        moveLeft, moveTop = getLeftTopOfTile(x + 1, y)
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
        for i in range(0, TILESIZE, animationSpeed):
            checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            drawTile(x + 1, y, mainBoard[x + 1][y], i, 0)
        mainBoard[x + 2][y] *= 2
        mainBoard[x + 1][y] = 0
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    if direction == DOWN:
        drawBoard(mainBoard, message)
        baseSurf = DISPLAYSURF.copy()
        moveLeft, moveTop = getLeftTopOfTile(x, y + 1)
        pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))
        for i in range(0, TILESIZE, animationSpeed):
            checkForQuit()
            DISPLAYSURF.blit(baseSurf, (0, 0))
            drawTile(x, y + 1, mainBoard[x][y + 1], 0, i)
        mainBoard[x][y + 2] *= 2
        mainBoard[x][y + 1] = 0
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def addTile(mainBoard):
    go = True
    posOne = [4, 4]
    while go:
        posOne = [randint(0, 3), randint(0, 3)]
        if mainBoard[posOne[0]][posOne[1]] == 0:
            go = False
    if randint(1, 10) == 1:
        mainBoard[posOne[0]][posOne[1]] = 4
    else:
        mainBoard[posOne[0]][posOne[1]] = 2

def checkLose(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == 0:
                return False
            elif x == 0 and y == 0 and (board[0][1] == board[0][0] or board[1][0] == board[0][0]):
                return False
            elif x == 3 and y == 0 and (board[2][0] == board[3][0] or board[3][1] == board[3][0]):
                return False
            elif x == 0 and y == 3 and (board[0][2] == board[0][3] or board[1][3] == board[0][3]):
                return False
            elif x == 3 and y == 3 and (board[2][3] == board[3][3] or board[3][2] == board[3][3]):
                return False
            elif x == 0 and not y == 0 and not y == 3 and (board[0][y - 1] == board[0][y] or board[1][y] == board[0][y] or board[0][y + 1] == board[0][y]):
                return False
            elif x == 3 and not y == 0 and not y == 3 and (board[3][y - 1] == board[3][y] or board[2][y] == board[3][y] or board[3][y + 1] == board[3][y]):
                return False
            elif y == 0 and not x == 0 and not x == 3 and (board[x - 1][0] == board[x][0] or board[x][1] == board[x][0] or board[x + 1][0] == board[x][0]):
                return False
            elif y == 3 and not x == 0 and not x == 3 and (board[x - 1][3] == board[x][3] or board[x][2] == board[x][3] or board[x + 1][3] == board[x][3]):
                return False
            elif not x == 0 and not x == 3 and not y == 0 and not y == 3 and (board[x - 1][y] == board[x][y] or board[x + 1][y] == board[x][y] or board[x][y + 1] == board[x][y] or board[x][y - 1] == board[x][y]):
                return False
    return True

if __name__ == '__main__':
    main()

