import random, pygame, sys, time
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
BOARDWIDTH = 10 # number of columns of icons
BOARDHEIGHT = 7 # number of rows of icons
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = [100, 100, 100]
NAVYBLUE = [ 60,  60, 100]
WHITE    = [255, 255, 255]
RED      = [255,   0,   0]
LIGHTRED = [175,  20,  20]
GREEN    = [  0, 255,   0]
BLUE     = [  0,   0, 255]
LIGHTBLUE= [ 20,  20, 210]
YELLOW   = [255, 255,   0]
ORANGE   = [255, 128,   0]
PURPLE   = [255,   0, 255]
CYAN     = [  0, 255, 255]

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
TEXTCOLOR = RED
TEXTSHADOWCOLOR = LIGHTRED


DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN]
ALLSHAPES = [DONUT, SQUARE, DIAMOND, LINES, OVAL]
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 75)
    pygame.display.set_caption('Candy Crush')
    DISPLAYSURF.fill(LIGHTBLUE)

    showTextScreen('Candy Crush')

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event

    icons = getList()
    mainBoard = getRandomizedBoard(icons)
    print(mainBoard)
    
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None # stores the (x, y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)


    while True: # main game loop
        for boxx in range(BOARDWIDTH-3):
            for boxy in range(BOARDHEIGHT):
                if mainBoard[boxx][boxy] == mainBoard[boxx+1][boxy] == mainBoard[boxx+2][boxy] == mainBoard[boxx+3][boxy]:
                    mainBoard[boxx][boxy]=None
                    mainBoard[boxx+1][boxy]=None
                    mainBoard[boxx+2][boxy]=None
                    mainBoard[boxx+3][boxy]=None
                    pygame.display.flip()
        for boxx in range(BOARDWIDTH-2):
            for boxy in range(BOARDHEIGHT):            
                if mainBoard[boxx][boxy] == mainBoard[boxx+1][boxy] == mainBoard[boxx+2][boxy]:
                    mainBoard[boxx][boxy]=None
                    mainBoard[boxx+1][boxy]=None
                    mainBoard[boxx+2][boxy]=None
                    pygame.display.flip()

        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT-3):            
                if mainBoard[boxx][boxy] == mainBoard[boxx][boxy+1] == mainBoard[boxx][boxy+2] == mainBoard[boxx][boxy+3]:
                    mainBoard[boxx][boxy]=None
                    mainBoard[boxx][boxy+1]=None
                    mainBoard[boxx][boxy+2]=None
                    mainBoard[boxx][boxy+3]=None
                    pygame.display.flip()
        for boxx in range(BOARDWIDTH):
            for boxy in range(BOARDHEIGHT-2): 
                if mainBoard[boxx][boxy] == mainBoard[boxx][boxy+1] == mainBoard[boxx][boxy+2]:
                    mainBoard[boxx][boxy]=None
                    mainBoard[boxx][boxy+1]=None
                    mainBoard[boxx][boxy+2]=None 
                    pygame.display.flip()
        
        

        # remove empty space and insert new icon at the front of the list
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if mainBoard[x][y] == None:
                    refill(mainBoard, icons)
                   
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        drawBoard(mainBoard)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #elif event.type == MOUSEMOTION:
                #mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            # The mouse is currently over a box.
            if mouseClicked:
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                    drawHighlightBox(boxx, boxy)
                    
                    
                else: # the current box was the second box clicked
                    if -1 <= boxx - firstSelection[0] <= 1 and boxy==firstSelection[1] or -1 <= boxy - firstSelection[1] <= 1 and boxx==firstSelection[0]: 
                        swapIfValid(mainBoard, firstSelection[0], firstSelection[1], boxx, boxy)   
                        

                        pygame.display.flip()

                        # Reset the board
                        #mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)
                        
                        # Show the fully unrevealed board for a second.
                        drawBoard(mainBoard)
                        pygame.display.update()
                        #pygame.time.wait(1)

                        # Replay the start game animation.
                        firstSelection = None
            if firstSelection != None:
                drawHighlightBox(firstSelection[0], firstSelection[1])
        

        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the additional "Press a key to play." text.
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard(list):
    icons = list * 10
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    return board

def getList():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( [shape, color] )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 10) # calculate how many icons are needed
    icons = icons[:numIconsUsed]
    return icons

def getNewIcon(list):
    icons = list * 30
    random.shuffle(icons)

    icons.pop(0)
    return icons[0]

def refill(board, list):
    # remove any empty spaces and insert a new icon at the top
    time.sleep(0.8)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == None:
                board[x].pop(y)
                board[x].insert(0, getNewIcon(list))


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def swapIfValid(board, x_a, y_a, x_b, y_b):
    # swap if valid move
    a=board[x_a][y_a]
    b=board[x_b][y_b]
    board[x_a][y_a]=b
    board[x_b][y_b]=a
    if not status(board):
        a=board[x_a][y_a]
        b=board[x_b][y_b]
        board[x_a][y_a]=b
        board[x_b][y_b]=a

def status(board):
    # if there are valid matches on the board, return True
    # otherwise, return False
    for boxx in range(BOARDWIDTH-3):
            for boxy in range(BOARDHEIGHT):
                if board[boxx][boxy] == board[boxx+1][boxy] == board[boxx+2][boxy] == board[boxx+3][boxy] and board[boxx][boxy] is not None:
                    return True
    for boxx in range(BOARDWIDTH-2):
        for boxy in range(BOARDHEIGHT):            
            if board[boxx][boxy] == board[boxx+1][boxy] == board[boxx+2][boxy] and board[boxx][boxy] is not None:
                return True

    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT-3):            
            if board[boxx][boxy] == board[boxx][boxy+1] == board[boxx][boxy+2] == board[boxx][boxy+3] and board[boxx][boxy] is not None:
                return True
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT-2): 
            if board[boxx][boxy] == board[boxx][boxy+1] == board[boxx][boxy+2] and board[boxx][boxy] is not None:
                return True
    return False        


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            if board[boxx][boxy] != None:
                left, top = leftTopCoordsOfBox(boxx, boxy)
                shape, color = board[boxx][boxy]
                drawIcon(shape, color, boxx, boxy)
    



def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, BLUE, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True


if __name__ == '__main__':
    main()
