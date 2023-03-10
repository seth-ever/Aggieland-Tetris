'''
Tetris Project 
Creators:
    Seth Webb, Sarah Rosinbaum, Paul Vetter, Anna Woodruff
Engr 102 final project
The game will consist of 6 different classes:
    Piece - a single tetris peice 
    JTetris - present the GUI for tetris in a window and do animation
    Brain - simple heuristic logic that knows how to play the tetris
    JBrainTetris - a subclass of JTetris that uses a brain to play the game w/ out a human player
    BrainTester - Possibly include this class to test our brain and implement machine learning
Using Tetris-Architecture.html for guidance and resources 
'''

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Instructions
left arrow or "a" key moves piece left
right arrow or "d" key moves piece right
up arrow or "w" key rotates piece
holding down the down arrow or "s" key will cause the piece to fall twice as fast
Press Space to store a piece once per turn.
Press p to toggle pause.

When inputing New Highscore Name, DO NOT USE CONSOLE, just type it normally, backspace works, enter to submit.
DO NOT put in names longer than four characters!

PLay Long Enough and discover the hidden musical easteregg!
"""

"""
Things still left to do:
Add a Menu Before the Game Starts
Add an AI to play and get better at the game.
"""
import pygame
import random
import turtle as t
from turtle import bgcolor

#Intialize
pygame.init()

clock = pygame.time.Clock()

#Global Variables
score = 0 #Initialized to be 0 for new game.
windowWidth = 800
windowHeight = 600
playWidth = 300  # meaning 300 // 10 = 30 width per block
playHeight = 600  # meaning 600 // 20 = 20 height per blo ck
cellSize = 30
topLeftOfPlayX = (windowWidth - playWidth) // 2
isPieceStored = False





#Create font Object
fontObj = pygame.font.Font('8-BIT WONDER.ttf', 30)
fontObjSmall = pygame.font.Font('8-BIT WONDER.ttf', 20)
fontObjSmallest = pygame.font.Font('8-BIT WONDER.ttf', 15)


high = open('High Score.txt', 'r')
player1Name = high.readline().strip()
player1Score = high.readline().strip()


player2Name = high.readline().strip()
player2Score = high.readline().strip()


player3Name = high.readline().strip()
player3Score = high.readline().strip()


player4Name = high.readline().strip()
player4Score = high.readline()

newName = ''
high.close()

pygame.mixer.music.load("Chip Tone Aggie War Hymn.mp3")
pygame.mixer.music.set_volume(0.1)

"""
Lists currently empty unitl Paul creates the shape grids, need to make sure the order is correct, and that we match the 
order of the shapes with the order of the colors. This will be passed into the piece class, also need his variable names.
Shape grids now created in a new fromat to be better used, don't worry about it anymore.
"""
smashBoy = [['00000',
             '00000',
             '01100',
             '01100',
             '00000']]

rhodeIslandZ = [['00000',
                 '00000',
                 '00110',
                 '01100',
                 '00000'],
                ['00000',
                 '00100',
                 '00110',
                 '00010',
                 '00000']]

clevelandZ = [['00000',
               '00000',
               '01100',
               '00110',
               '00000'],
              ['00000',
               '00100',
               '01100',
               '01000',
               '00000']]

hero = [['00100',
         '00100',
         '00100',
         '00100',
         '00000'],
        ['00000',
         '11110',
         '00000',
         '00000',
         '00000']]

blueRicky = [['00000',
              '01000',
              '01110',
              '00000',
              '00000'],
             ['00000',
              '00110',
              '00100',
              '00100',
              '00000'],
             ['00000',
              '00000',
              '01110',
              '00010',
              '00000'],
             ['00000',
              '00100',
              '00100',
              '01100',
              '00000']]

orangeRicky = [['00000',
                '00010',
                '01110',
                '00000',
                '00000'],
               ['00000',
                '00100',
                '00100',
                '00110',
                '00000'],
               ['00000',
                '00000',
                '01110',
                '01000',
                '00000'],
               ['00000',
                '01100',
                '00100',
                '00100',
                '00000']]

teeWee = [['00000',
           '00100',
           '01110',
           '00000',
           '00000'],
          ['00000',
           '00100',
           '00110',
           '00100',
           '00000'],
          ['00000',
           '00000',
           '01110',
           '00100',
           '00000'],
          ['00000',
           '00100',
           '01100',
           '00100',
           '00000']]

shapes = [smashBoy, rhodeIslandZ, clevelandZ, hero, blueRicky, orangeRicky, teeWee]
colors = [(255, 255, 0), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 165, 0), (0, 0, 255), (130, 0, 130)]


class Piece(object):
    """
    Takes in a spawn position, x and y, and takes in what shape the piece will be.
    Used to create elements of pieces to be used by other of functions. Refrenced mainly by position, and color.
    Shape used when displaying next and stored pieces.
    """
   # x = 20
    #y = 10
    def __init__(self, x, y, shape): #self is like this from java, funny enough turns out you can do other words not self, but to keep it easy for Dr. Ritchey to Grade I say we keep it as self.
        self.x  = x
        self.y = y
        self.shape = shape
        self.color = colors[shapes.index(shape)] # Returns the color of the shape being passed
        self.rotation = 0 #Defaulted to 0, will incremint when up arrow is pressed, number will refrence which list to display.

    

def main(screen):
    """
    Takes in a window, named screen.
    Initializes a blank dictionary locked positions and then creates a grid based off of the dictionary,
    storing it in the varibale grid.
    initializes variables to fit the start conditions of the game.
    
    The game loop is initiated.
    The music manager is the first thing evaluated in the game loop.
    Next, the falling of the pieces is managed by set fall times and the clock rawtime,
    whenever the current clock time is greater than the set fall check time, the piece is moved down one posistion.
    We also recreate the grid variable based on the dictionary of locked positions.
    
    If the user exits out of the window it will exit out of the gameloop.
    
    We have specialized inputs to the state of the piece based on keyboard inputs given.
    
    we have the calls for next piece and stored piece when applicable.
    
    We then call the rendering near the bottem to ensure it displays the most current information.
    
    At the end of the game loop we check to see if the player has lost based on if there are pieces above the allowed play area.
    
    After the game loop we check to see if we need to update the score.
    """
    lockedPositions = {} #Initialize Locked Postitions as a blank dictionary
    grid = createGrid(lockedPositions) #Passes the dictionary into our method 
    
    
    isStored = False
    storedThisTurn = False
    storedPiece = 0
    holdPiece = 0
    
    changePiece = False #default this false or else itll constantly change pieces, will use this as a check later to know when to change piece.
    run = True #Initialize run for our while loop later, game will run while thise is true, stop when false.
    
    clock = pygame.time.Clock()# Sarahs clock that actually ended up being needed for controlling the falling piece
    fallTime = 0 #Will be refrenced later to controll when the piece drops.
    
    currentPiece = getShape() #Literally the only remaining part of the original code other than the window, changed to fit the getShape Method.
    nextPiece = getShape() #A benifit of this I just noticed is we only have to keep track of two sets of self. keeps memory relatively free. Only two objectives of the shape Class. 
    fastFall = 1
    
    musicCount = 1
    
    #THE GAME LOOP, AS FROM THE ORIGINAL BUILD, BEFORE EVERYTHING WENT BAD
    while run:
        
        
        
        
        #This is a little easteregg left in be the development team, whats a game without eggs :)
        if not pygame.mixer.music.get_busy():
            if musicCount % 3 == 0:
                pygame.mixer.music.load("Video Game medley.mp3")
                pygame.mixer.music.set_volume(0.4)
            else: 
                pygame.mixer.music.load("Chip Tone Aggie War Hymn short.mp3")
                pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play()
            musicCount += 1
        
        fallCheck = 0.30/fastFall #should divide by fast fall, speed * fastFall during fast fall
        grid = createGrid(lockedPositions) #Called because we need to update the grid BEFORE ANYTHING ELSE
        fallTime += clock.get_rawtime() #Adds how much time has passed since last tick
        clock.tick() # Resets the raw time for next fall time update. 
        
        if fallTime / 1000 > fallCheck:  # in ms so divide by 1000
            fallTime = 0 #reset this for next interval
            currentPiece.y += 1 #In squares not pixels, Remember Y goes down so plus not minus.
            if not(valid(currentPiece, grid)) and currentPiece.y > 0: #Checks if touching invalid spot, so long as not above screen
                currentPiece.y += -1 #move it back up to valid, gonna just go ahead and slide that bad boy back up there
                changePiece = True #I knew this would come in handy, *pats self on back*
                storedThisTurn = False
        
        for event in pygame.event.get(): #Pygame makes this so so sweet
            if event.type == pygame.QUIT:
                run = False #this breaks out of the while Loop
                
                
            if event.type == pygame.KEYDOWN: #means if key is being pressed, not down key
                #there will be or's to check for wasd and arrow key control :)    
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    currentPiece.x += -1 #Moves Left One Square
                    if not ( valid(currentPiece, grid) ):
                        currentPiece.x += 1 #Oppisite of the movement from key
                    
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    currentPiece.x += 1 #Moves Right One Square
                    if not ( valid(currentPiece, grid) ):
                        currentPiece.x += -1 #Oppisite of the movement from key
                        
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    fastFall = 7 #The higher this number the faster the fall
                
                if event.key == pygame.K_p:
                    run = pause(screen)
                    
              
                       
                
                if event.key == pygame.K_SPACE:
                    if not isStored:
                        storedPiece = currentPiece
                        currentPiece = nextPiece
                        nextPiece = getShape()
                        storedThisTurn = True
                        isStored = True
                    elif not storedThisTurn:
                        holdPiece = storedPiece
                        storedPiece = currentPiece
                        currentPiece = Piece(5,0, holdPiece.shape)
                        storedThisTurn = True
                        
                    
                
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    currentPiece.rotation += 1 #Changes the rotation cycles the layouts of shape. 
                    if not (valid(currentPiece, grid)):
                        currentPiece.rotation += -1
            if event.type == pygame.KEYUP: #When Key Is let go, used to reset fast fall
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    fastFall = 1 #Should return drop to normal speed
        
        shapePosition = convertShape(currentPiece)
        
        for i in range(len(shapePosition)):
             x, y = shapePosition[i]
             if y > -1:
                grid[y][x] = currentPiece.color   #y,x not x,y. We are about learning from our mistakes.
        
        
        if changePiece: #time for foresite to pay off, note only do this if automatic next,not user store will need other method for that.
            for pos in shapePosition: # SO MANY POS VARIABLES TO KEEP TRACK OF AHHAHAHHAHAHAH 
                p = (pos[0], pos[1])
                lockedPositions[p] = currentPiece.color #updates the tuple dictionary, note can be equal because the piece colors have already been passed
            
            #Enable the game to display next piece like in Real Tetris
            currentPiece = nextPiece
            nextPiece = getShape()
            changePiece = False #because we don't want to rapid change, have to reset this to default.
            
            #Call Clear Rows here because this is when piece stops.
            clearRows(grid, lockedPositions)
            
         
        #Our Draw Method Calls
        
        drawWindow(screen, grid)
        drawStoredShape(screen, storedPiece, isStored)
        drawNextShape(nextPiece, screen)
        drawScore(screen)
        drawHighScore(screen)
        
        
        pygame.display.update()
        
        if  checkLost(lockedPositions): #We pass locked positions because they will contain all positions.
            run = False #Will exit the game Loop, the While Loop.
    
      
    pygame.mixer.music.stop()
    
    
    if int(score) >= int(player4Score):
        newHighScore(screen)
        newHigh = open('High Score.txt', 'w')
        if int(score) >= int(player1Score): #New First Place
            newHigh.write(newName+"\n")
            newHigh.write(str(score)+"\n")
            
            newHigh.write(player1Name+"\n")
            newHigh.write(player1Score+"\n")
            
            newHigh.write(player2Name+"\n")
            newHigh.write(player2Score+"\n")
            
            newHigh.write(player3Name+"\n")
            newHigh.write(player3Score)
            
        elif int(score) >= int(player2Score):
            newHigh.write(player1Name+"\n")
            newHigh.write(player1Score+"\n")
            
            newHigh.write(newName+"\n")
            newHigh.write(str(score)+"\n")
                
            newHigh.write(player2Name+"\n")
            newHigh.write(player2Score+"\n")
            
            newHigh.write(player3Name+"\n")
            newHigh.write(player3Score)
            
        elif int(score) >= int(player3Score):
            newHigh.write(player1Name+"\n")
            newHigh.write(player1Score+"\n")
            
            newHigh.write(player2Name+"\n")
            newHigh.write(player2Score+"\n")
            
            newHigh.write(newName+"\n")
            newHigh.write(str(score)+"\n")
            
            newHigh.write(player3Name+"\n")
            newHigh.write(player3Score)
    
        else:
            newHigh.write(player1Name+"\n")
            newHigh.write(player1Score+"\n")
            
            newHigh.write(player2Name+"\n")
            newHigh.write(player2Score+"\n")
            
            newHigh.write(player3Name+"\n")
            newHigh.write(player3Score+"\n")
            
            newHigh.write(newName+"\n")
            newHigh.write(str(score))
            
        newHigh.close()
     
   
    #End of Main Functon.

def createGrid(lockedPositions = {}):
    """
    Creates a 2d matrix of values 0,0,0. Representing the color black.
    Then it checks for every possible position stored in the dictionary locked positions and return a color value if there exists
    a key corisponding to that position, updating and returning a grid, 2d matrix, filled with the color values needed.
    """
    grid = [[(0,0,0,) for x in range(10)] for y in range(20)] #Draws a 20 X 10 Black-(0,0,0) Grid
    
    #Checks the grid for already played pieces
    for i in range(20):
        for j in range(10):
            if (j, i) in lockedPositions:
                pointColor = lockedPositions[(j,i)] #pointColor refferring to the color of the piece at that point
                grid[i][j] = pointColor
                
    return grid #returns the black grid with all the played pieces on it.


def getShape():
    """
    Passes an object into the piece class and return the corrisponding set of values.
    Object values passed are x, y, shape
    is 5 and 0 because we are refferencing squares on the board not pixels
    The shape that is passed is chosen via random.choice form the list of shapes.
    """
    global shapes, colors

    return Piece(5, 0, random.choice(shapes))
  


def convertShape(currentShape):
    """
    Takes in a shape argument.
    creates an empty list called positions that will be added to during the conversion.
    The roation is a cycle of the different sets of values possible for the shapes, since it loops a modulus is used.
    posistions is appeneded based on whether or not the value of the set of shapes is a 0 or a 1,
    1's get apended.
    """
    positions = [] #new empty list
    form = currentShape.shape[currentShape.rotation % len(currentShape.shape)] #Modulus allows us to cycle through rotations :) hope that helps you in your design, Pual
    
    for i, line in enumerate(form): #had a lot of fun with this one. Sarcasm = True
        row = list(line)
        for j, column in enumerate(row):
            if column == '1':             # 1 being where block is, based on Pauls form. Note This *********IMPORTANT*********
                positions.append((currentShape.x + j, currentShape.y + i))
                
    for i, pos in enumerate(positions):
        positions[i] = (pos[0]-2 , pos[1] -4) #may or may not need offsets, will check when Paul passes his shapes
    
    return positions

def valid(shape, grid):
    """
    Passes in the shape of the current piece and the 2d list of color values grid.
    makes a list of accepted positions based on whether or not that postion in grid is black or not, black is accepted.
    Then gets a converted form of the shape by passing shape into convert shape.
    If the any of the positions of the piece is in a position not shared by accepted positions list, it will return False
    Otherwise, if all positions are shared by acceptedPositions it will return true.

    """
    #The ifgrid[i][j] == black checks if empty space, we only want to add empty spaces to our valid list, for obvious reasons.
    acceptedPositions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0) ] for i in range(20)] #A tuple of all accepted positions allowed in the grid. Did it this way was tired of nested for loops, sue me. 
    acceptedPositions = [j for sub in acceptedPositions for j in sub] #Had to look up how to do this, turns matrix into a list, 2D to 1D Emailed Ritchey to ask about will see when she responds
    """
    [[1,2] , [3,4]]
    becomes 
    [1,2,3,4]
    for refrence of before and after structure.
    """ 
    converted = convertShape(shape) #Makes the info Usable
    
    for position in converted:
        if position not in acceptedPositions: #Checks list of accepted positions
            if position[1] > -1: #Incase Piece starts above the screen, otherwise the game would end before it started and thats no good. Would help with potentially needed offsets
                return False #I KEEP WANTING TO PUT SEMI COLONS AFTER RETURN AHHHHHHHHHHHHHHHHHHH
    return True #Because that means all must be true, all passed.

def checkLost(positions):
    """
    Is given the dictionary locked positions as positions.
    Checks to see if any of the key positions y values exists outside the play area, if so returns True and makes main exit 
    the game loop, otherwise; if none postions are outside the play are it returns False and the game loop continues.
    """
    for position in positions: #Note Singular versus Plural, this is important !!!!!!!
        x, y = position
        if y < 1: #Checks to see if above screen
            return True  #Uh OH Thats A Game Over, Once we code that part...
        
    return False #you may live, for now -_-
        


def clearRows(grid, lockedPositions ):
    """
    Is given both the 2d list grid and the dictionary lockedPositions.
   Checks to see if a row(s) contain no black spaces, and makes count equal to the number of rows not containing a black space.
   I also stores the value of that row as remember.
   Next we clear the row set as remember. 
   Now based on the count of rows cleared we incriment the scroe and downshift the dictionary of locked positions so we dont
   have floating incomplete row. 
    """
    #ALot harder than I though because of gravity, but I think I found a useful method, need to Test with Puals Shapes.
    
    count = 0
    for i in range(19, -1, -1): #Counting Backwards, check to see if I did the math right Please. Count backwards to not overwrite rows.
        
        if (0,0,0,) not in grid[i]: # If there are no blank black spaces
            count += 1
            remember = i
            for j in range(10):
                try: 
                    del lockedPositions[(j,i)] #the current position
                except:
                    continue #Im pretty sure we needed a try as part of our grade, this was the best spot I could think of
            
            
    
    """
    To Paul,
    If you dont understand how python handles Global variable refrence and how we keep the function from 
    creating its own local variable, these two links might help give insight. - Seth
    https://www.python-course.eu/python3_global_vs_local_variables.php
    https://stackoverflow.com/questions/10506973/can-not-increment-global-variable-from-function-in-python
    """
    global score#DO NOT REMOVE, This is needed or else it keeps trying to create a local variable score and the whole things crashes when you clear a line
     
    
    
    if count > 0: #Meaning we cleared at least one line
    #Score increase from clearing lines
        if count == 1:
            score += 100
        if count == 2:
            score += 250
        if count == 3:
            score += 400
        if count == 4:
            score += 600
    
        
    
        """"
        This next line basically sorts elements of the list be their Y values, it's a bit trippy and weird to explain but it works like this
        unsorted (1,2) , (5,3) (9,1)
        sorted (9,1) , (1,2) , (5,3)
        
       
        I didn't Use i and j because it needs to be key for that lamda sort. Hopefully it is easier to follow than write.
        For information on the sorts check these two websites, they had useful info, especially the first one.
        https://docs.python.org/3/howto/sorting.html
        https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python
        """
        for key in sorted(list(lockedPositions), key = lambda x: x[1])[::-1]: #Definitely had to look this up, converted it to work with our variables and matrix based data, that lambda stuff is funky. Probably best to not touch, convert things to work with this not vise verse
            x,y = key #Because key is a touple because of our 2D Matrix
            if y < remember:
                newkey = (x, y + count)
                lockedPositions[newkey] = lockedPositions.pop(key)
        
        #DO NOT DO THE FOLLOWING LINE, CRASHES CODE. THE ERROR IS RARE AND NON GAME BREAKING, LEAVE IT FOR NOW AND IF WE HAVE TIME TRY TO FIX IT.
        #clearRows(grid, lockedPositions)#Testing out this reccursion, theres a weird glitch where sometimes when multiple line clears occour than are unconcurerent lines. Reccurive calls on succesful clears should help.  
        
        

def drawGrid(screen, grid):
    """
    Draws grid lines to split up the cells of play arean making it easier to line up pieces.
    """
    
    #Draws A Grid Of Lines
    for i in range(20):
        pygame.draw.line(screen, (255, 255, 255), (topLeftOfPlayX, i * cellSize), (topLeftOfPlayX + playWidth, i * cellSize)) #Horizontal Line
        for j in range(10):
             pygame.draw.line(screen, (255, 255, 255), (topLeftOfPlayX + j * cellSize, 0), (topLeftOfPlayX + j * cellSize, playHeight)) #vert lines
            
   


def drawNextShape(shape, screen):
    """
    Takes in a shape and the window.
    Renders the word next.
    Then renders the piece corrisponding to the shape value passed, which should be the same is the shape value stored
    as next in the game loop, making the graphic and the gameplay corrispond.
    It draws the piece be seeing the shape and going through a 2d list evaluation of where it is defined, similar to convert shape.
    0 means not exist, 1 means exist. Like a boolean.

    """
    textscreenObj = fontObj.render('Next', True, (255, 255, 255))#Next Shape wouldn't fit, changed to Next
   
    
    nextPieceX = topLeftOfPlayX + playWidth + 50
    nextPieceY = playHeight // 2 - 270
    
    screen.blit(textscreenObj, (nextPieceX +20, nextPieceY))#Prints out Next Shape in white 8-bit letter
    
    form = shape.shape[shape.rotation % len(shape.shape)] #Same line as in convert shape, See that for Documentation
    
    for i, line in enumerate(form):
        row = list(line)
        for j, column in enumerate(row):
            if column == "1":
                #Rather than add postion, which we care not for, we will draw it, simmilar to the line in the drawWindow method below. wave at it, its a friend.
                pygame.draw.rect(screen, shape.color, (nextPieceX + j * cellSize, nextPieceY + i*cellSize + 45, cellSize, cellSize), 0) 
    
def drawStoredShape(screen, shape, check):
    """
    Takes in the weindow, the shape of the stroed piece, and a boolean check which tells if a piece is stored.
    Draws the word stroed,
    It evaluates check, if true meaning there is a piece it will the render the piece based on the shape value given.
    For rendering details, see function drawNextShape.
    """
    textscreenObj = fontObj.render('Stored', True, (255, 255, 255))
   
    
    storedPieceX = topLeftOfPlayX + playWidth + 50
    storedPieceY = playHeight // 2 + 30
    
    screen.blit(textscreenObj, (storedPieceX - 10, storedPieceY))#Prints out stored in white 8-bit letter

    if check:
        
        form = shape.shape[shape.rotation % len(shape.shape)] #Same line as in convert shape, See that for Documentation
    
        for i, line in enumerate(form):
            row = list(line)
            for j, column in enumerate(row):
                if column == "1":
                    #Rather than add postion, which we care not for, we will draw it, simmilar to the line in the drawWindow method below. wave at it, its a friend.
                    pygame.draw.rect(screen, shape.color, (storedPieceX + j * cellSize, storedPieceY + i*cellSize + 45, cellSize, cellSize), 0)

def drawWindow(screen, grid):
    """
    Takes in a window, screen. Takes in a 2d list, grid.
    makes the window a solid maroon to be used as a background.
    cellSize is presdetirmed and is used to make more than one pixel be drawn.
    It then calls the funciton drawGrid, passing in the Screen and grid.
    """
    screen.fill((67,0,48)) #Draws the maroon background.
     
    for i in range(20):
        for j in range(10):
            #Draws onto screen the color of grid[i][j], at the correct position, height and width of the draw, and the 0 at the end to make sure it filles the draw, without it it only draws borders
            pygame.draw.rect(screen, grid[i][j], (topLeftOfPlayX + j * cellSize, i * cellSize, cellSize, cellSize), 0) 
            
            
    
    
    
    drawGrid(screen, grid) #Calls the draw grid method, to draw the grid 
    

def drawScore(screen):
     """
     Evaluates the number of digits in the global variable score and then
     renders it in a location based on its length, the longer the score the more leftward it is rendered.
     y value is unnaffected.

   

     """
     textscreenObj = fontObj.render('Score', True, (255, 255, 255) )
     screen.blit(textscreenObj,( 40,330))#Prints out Score in white 8-bit letters
     
     #Format where the score is drawn based on its length
     digits = 0
     holder = score
     while holder >= 10:
         holder = holder // 10
         digits += 1
     textscreenObj = fontObj.render(str(score), True, (255, 255, 255) )
     screen.blit(textscreenObj,( 100 - digits * 12.5 ,380))

def drawHighScore(screen):
     """
     Takes in the previously defined player names and scores and renders them accordingly in the top left corner of the screen.
     """
     textscreenObj = fontObjSmall.render('Leaderboard', True, (255, 255, 255) )
     screen.blit(textscreenObj,(15,30))#Prints out Score in white 8-bit letters
     
     #Format where the score is drawn based on its length
     
     textscreenObj = fontObjSmallest.render(player1Name, True, (255, 255, 255) )
     screen.blit(textscreenObj,(15,80))
     textscreenObj = fontObjSmallest.render(player1Score, True, (255, 255, 255) )
     screen.blit(textscreenObj,(95,80))
    
     textscreenObj = fontObjSmallest.render(player2Name, True, (255, 255, 255) )
     screen.blit(textscreenObj,(15,100))
     textscreenObj = fontObjSmallest.render(player2Score, True, (255, 255, 255) )
     screen.blit(textscreenObj,(95,100))
     
     textscreenObj = fontObjSmallest.render(player3Name, True, (255, 255, 255) )
     screen.blit(textscreenObj,(15,120))
     textscreenObj = fontObjSmallest.render(player3Score, True, (255, 255, 255) )
     screen.blit(textscreenObj,(95,120))
     
     textscreenObj = fontObjSmallest.render(player4Name, True, (255, 255, 255) )
     screen.blit(textscreenObj,(15,140))
     textscreenObj = fontObjSmallest.render(player4Score, True, (255, 255, 255) )
     screen.blit(textscreenObj,(95,140))

def newHighScore(screen):
    """
    Draws a black screen and looks for keyboard inputs, based on inputs it concatinates to a string and then 
    renders the string into the middle of the screen. 
    The string of the name is made global so it can be refrenced in the Main function when creating the new txt file.
    """
    global newName
    run = True
    screen.fill((0,0,0))
    while run:    
        
        textScreenObj = fontObjSmall.render('Enter Your Initials', True, (255, 255, 255) )
        screen.blit(textScreenObj,(225,30))#Prints out Score in white 8-bit letters
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                #Oh Boy THis will be fun
                if event.key == pygame.K_a:
                    newName += "A"
                if event.key == pygame.K_b:
                    newName += "B"
                if event.key == pygame.K_c:
                    newName += "C"
                if event.key == pygame.K_d:
                    newName += "D"
                if event.key == pygame.K_e:
                    newName += "E"
                if event.key == pygame.K_f:
                    newName += "F"
                if event.key == pygame.K_g:
                    newName += "G"
                if event.key == pygame.K_h:
                    newName += "H"
                if event.key == pygame.K_i:
                    newName += "I"
                if event.key == pygame.K_j:
                    newName += "J"
                if event.key == pygame.K_k:
                    newName += "K"
                if event.key == pygame.K_l:
                    newName += "L"
                if event.key == pygame.K_m:
                    newName += "M"
                if event.key == pygame.K_n:
                    newName += "N"
                if event.key == pygame.K_o:
                    newName += "O"
                if event.key == pygame.K_p:
                    newName += "P"
                if event.key == pygame.K_q:
                    newName += "Q"
                if event.key == pygame.K_r:
                    newName += "R"
                if event.key == pygame.K_s:
                    newName += "S"
                if event.key == pygame.K_t:
                    newName += "T"
                if event.key == pygame.K_u:
                    newName += "U"
                if event.key == pygame.K_v:
                    newName += "V"
                if event.key == pygame.K_w:
                    newName += "W"
                if event.key == pygame.K_x:
                    newName += "X"
                if event.key == pygame.K_y:
                    newName += "Y"
                if event.key == pygame.K_z:
                    newName += "Z"
                if event.key == pygame.K_BACKSPACE:
                    newName = newName[0:-1]
                    screen.fill((0,0,0))
                    textScreenObj = fontObjSmall.render('Enter Your Initials', True, (255, 255, 255) )
                    screen.blit(textScreenObj,(225,30))#Prints out Score in white 8-bit letters
                
                if event.key == pygame.K_RETURN:
                    run = False
                
                textscreenObj = fontObjSmallest.render(newName, True, (255, 255, 255) )
                screen.blit(textscreenObj, (300,300))
                pygame.display.update()
                
                
            pygame.display.update()
            
def pause(screen):
    """
    Pauses the game, displays the pause message, unpauses when p is pressed again.
    Also pauses the music when pressed, resumes the music if the funciton is about to go back.
    Has a boolean return incase the user closes the window while paused, will stop music and exit game loop if returned false.
    """
    
    pygame.mixer.music.pause()
    
    pause = True
    while pause:
        for event in pygame.event.get(): #Pygame makes this so so sweet
            if event.type == pygame.QUIT:
                pause = False
                pygame.mixer.music.stop()
                return False
            textScreenObj = fontObjSmall.render('Paused', True, (255, 255, 255) )
            screen.blit(textScreenObj,(350,300))
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
            pygame.display.update()
            
    pygame.mixer.music.unpause()
    return True
    
def MenuDisplay():
  """
    A simple collection of turtle graphic instructions that draws out 
    welecome to aggieland tetris.
    Starts by initializing speed and color and mode.
    Next is all the movement instructions.

  """
  #Welcome to Aggieland Tetris
  #Welcome to
  #Setting place
  
  
  t.speed(0)
  t.pensize(4)
  bgcolor('black')
  t.colormode(255)
  t.pencolor(67,0,48)
  
  t.penup()
  t.left(90)
  t.forward(100)
  t.left(90)
  t.forward(140)
  
  #W
  
  t.pendown()
  t.right(90)
  t.forward(34)
  t.right(180)
  t.forward(34)
  t.left(90)
  t.forward(15)
  t.left(90)
  t.forward(15)
  t.right(180)
  t.forward(15)
  t.left(90)
  t.forward(15)
  t.left(90)
  t.forward(34)
  t.penup()
  t.right(180)
  t.forward(34)
  t.left(90)
  t.forward(13)
  
  #e
  t.pendown()
  t.left(90)
  t.forward(18)
  t.right(90)
  t.forward(12)
  t.right(90)
  t.forward(5)
  t.right(90)
  t.forward(12)
  t.left(90)
  t.forward(13) 
  t.left(90)
  t.forward(12)
  t.penup()
  
  #l
  
  t.forward(14)
  t.pendown()
  t.left(90)
  t.forward(35)
  t.penup()
  
  #c
  
  t.left(180)
  t.forward(35)
  t.left(90)
  t.forward(12)
  t.pendown()
  t.forward(15)
  t.right(180)
  t.forward(15)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(15)
  t.penup()
  t.right(90)
  t.forward(18)
  t.left(90)
  t.forward(10)
  
  #o
  
  t.left(90)
  t.pendown()
  t.forward(18)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(18)
  t.penup()
  t.right(180)
  t.forward(27)
  
  #m
  t.pendown()
  t.left(90)
  t.forward(21)
  t.right(180)
  t.forward(3)
  t.left(90)
  t.forward(13)
  t.right(90)
  t.forward(18)
  t.left(180)
  t.forward(18)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(18)
  t.penup()
  
  #e
  t.left(90)
  t.forward(10)
  t.pendown()
  t.left(90)
  t.forward(18)
  t.right(90)
  t.forward(12)
  t.right(90)
  t.forward(5)
  t.right(90)
  t.forward(12)
  t.left(90)
  t.forward(13) 
  t.left(90)
  t.forward(12)
  t.penup()
  
  #t
  t.forward(38)
  t.pendown()
  t.forward(10)
  t.right(180)
  t.forward(10)
  t.right(90)
  t.forward(27)
  t.right(180)
  t.forward(7)
  t.left(90)
  t.forward(8)
  t.left(180)
  t.forward(16)  
  t.left(180)
  t.forward(8)
  t.right(90)
  t.forward(20)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(6)
  t.penup()
  
  #o
  t.right(180)
  t.forward(6)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.pendown()
  t.forward(18)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(18)
  t.penup()
  t.right(180)
  t.forward(27)
    
  
  
  #A

  t.pensize(3)
  t.home()
  t.left(180)
  t.penup()
  t.forward(250)
  t.pendown()
  t.forward(5)
  t.left(90)
  t.pendown()
  t.forward(10)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(5)
  t.right(115)
  t.forward(13)
  t.right(65)
  t.forward(15)
  t.right(65)
  t.forward(13)
  t.right(115)
  t.forward(5)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(5)
  t.right(65)
  t.forward(40)
  t.right(115)
  t.forward(6)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(25)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(6)
  t.right(115)
  t.forward(40)
  t.left(115)
  t.penup()
  t.forward(18)
  t.left(90)
  t.forward(20)
  t.right(90)
  t.pendown()
  t.forward(10)
  t.left(115)
  t.forward(13)
  t.left(135)
  t.forward(13)
  t.left(110)
  t.penup()
  t.forward(45)
  t.right(90)
  t.forward(30)
  t.left(205)
  t.pendown()
  #G
  t.forward(12)
  t.right(25)
  t.forward(35)
  t.right(25)
  t.forward(12)
  t.right(65)
  t.forward(35)
  t.right(65)
  t.forward(12)
  t.right(25)
  t.forward(8)
  t.right(90)
  t.forward(12)
  t.right(90)
  t.forward(6)
  t.left(90)
  t.forward(22)
  t.left(90)
  t.forward(30)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(8)
  t.left(90)
  t.forward(5)
  t.right(90)
  t.forward(8)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(17)
  t.right(25)
  t.forward(15)
  t.right(65)
  t.forward(32)
  t.penup()
  #G
  t.right(180)
  t.forward(53)
  t.left(115)
  t.pendown()
  t.forward(12)
  t.right(25)
  t.forward(35)
  t.right(25)
  t.forward(12)
  t.right(65)
  t.forward(35)
  t.right(65)
  t.forward(12)
  t.right(25)
  t.forward(8)
  t.right(90)
  t.forward(12)
  t.right(90)
  t.forward(6)
  t.left(90)
  t.forward(22)
  t.left(90)
  t.forward(30)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(8)
  t.left(90)
  t.forward(5)
  t.right(90)
  t.forward(8)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(17)
  t.right(25)
  t.forward(15)
  t.right(65)
  t.forward(32)
  #I
  t.right(180)
  t.penup()
  t.forward(47)
  t.left(90)
  t.pendown()
  t.forward(13)
  t.right(90)
  t.forward(13)
  t.left(90)
  t.forward(30)
  t.left(90)
  t.forward(13)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(35)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(13)
  t.left(90)
  t.forward(30)
  t.left(90)
  t.forward(13)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(35)
  t.right(180)
  t.penup()
  t.forward(50)
  #E
  t.pendown()
  t.left(180)
  t.forward(8)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(7)
  t.left(90)
  t.forward(30)
  t.left(90)
  t.forward(7)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(50)
  t.right(90)
  t.forward(20)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(8)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(9)
  t.left(90)
  t.forward(12)
  t.right(90)
  t.forward(12)
  t.right(90)
  t.forward(13)
  t.left(90)
  t.forward(9)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(12)
  t.right(90)
  t.forward(13)
  t.right(90)
  t.forward(26)
  t.right(90)
  t.forward(45)
  t.right(180)
  t.penup()
  t.forward(60)
  #L
  t.left(180)
  t.pendown()
  t.forward(6)
  t.right(90)
  t.forward(14)
  t.right(90)
  t.forward(6)
  t.left(90)
  t.forward(32)
  t.left(90)
  t.forward(6)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(18)
  t.right(90)
  t.forward(42)
  t.left(90)
  t.forward(21)
  t.left(90)
  t.forward(6)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(20)
  t.right(90)
  t.forward(44)
  t.right(180)
  t.penup()
  t.forward(56)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.pendown()

  #A
  t.forward(5)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.pendown()
  t.forward(20)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(5)
  t.right(115)
  t.forward(13)
  t.right(65)
  t.forward(15)
  t.right(65)
  t.forward(13)
  t.right(115)
  t.forward(5)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(5)
  t.right(65)
  t.forward(40)
  t.right(115)
  t.forward(6)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(25)
  t.left(90)
  t.forward(10)
  t.left(90)
  t.forward(6)
  t.right(115)
  t.forward(40)
  t.left(115)
  t.penup()
  t.forward(18)
  t.left(90)
  t.forward(20)
  t.right(90)
  t.pendown()
  t.forward(10)
  t.left(115)
  t.forward(13)
  t.left(135)
  t.forward(13)
  t.left(110)
  t.penup()
  t.forward(45)
  t.right(90)
  t.forward(30)
  t.left(205)
  t.right(115)
  t.forward(7)
  t.left(180)

  #N
  t.pendown()
  t.forward(8)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(8)
  t.left(90)
  t.forward(36)
  t.left(90)
  t.forward(8)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(20)
  t.right(65)
  t.forward(50)
  t.left(155)
  t.forward(38)
  t.left(90)
  t.forward(8)
  t.right(90)
  t.forward(8)
  t.right(90)
  t.forward(25)
  t.right(90)
  t.forward(8)
  t.right(90)
  t.forward(6)
  t.left(90)
  t.forward(39)
  t.left(90)
  t.forward(6)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(24)
  t.right(65)
  t.forward(36)
  t.left(155)
  t.forward(22)
  t.left(90)
  t.forward(6)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(20)

  #D
  t.penup()
  t.right(180)
  t.forward(68)
  t.left(180)
  t.pendown()
  t.forward(8)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(8)
  t.left(90)
  t.forward(37)
  t.left(90)
  t.forward(8)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(48)
  t.right(65)
  t.forward(13)
  t.right(25)
  t.forward(33)
  t.right(25)
  t.forward(13)
  t.right(65)
  t.forward(40)
  t.right(180)
  t.penup()
  t.forward(10)
  t.left(90)
  t.forward(12)
  t.pendown()
  t.forward(33)
  t.right(90)
  t.forward(20)
  t.right(65)
  t.forward(8)
  t.right(25)
  t.forward(20)
  t.right(25)
  t.forward(8)
  t.right(65)
  t.forward(21)
  
  
  #T
  t.pensize(2.5)
  t.penup()
  t.home()
  t.right(90)
  t.forward(120)
  t.right(90)
  t.forward(110)
  t.right(90)
  t.pendown()
  t.forward(50)
  t.left(90)
  t.forward(10)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(35)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(10)
  t.left(90)
  t.forward(50)
  t.right(90)
  t.forward(15)
  t.right(180)
  t.penup()
  t.forward(30)
  
  #E
  t.pendown()
  t.left(90)
  t.forward(60)
  t.right(90)
  t.forward(35)
  t.right(115)
  t.forward(13)
  t.right(65)
  t.forward(17)
  t.left(90)
  t.forward(8)
  t.left(90)
  t.forward(14)
  t.right(115)
  t.forward(9)
  t.right(65)
  t.forward(8)
  t.left(90)
  t.forward(20)
  t.left(90)
  t.forward(22)
  t.right(65)
  t.forward(13)
  t.right(115)
  t.forward(42)

  #T
  t.penup()
  t.right(180)
  t.forward(49)
  t.left(90)
  t.pendown()
  t.forward(50)
  t.left(90)
  t.forward(10)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(35)
  t.right(90)
  t.forward(10)
  t.right(90)
  t.forward(10)
  t.left(90)
  t.forward(50)
  t.right(90)
  t.forward(15)
  t.right(180)
  t.penup()
  t.forward(30)
  
  #R
  t.pendown()
  t.left(90)
  t.forward(60)
  t.right(90)
  t.forward(37)
  t.right(130)
  t.forward(25)
  t.left(130)
  t.forward(8)
  t.right(65)
  t.forward(46)
  t.right(115)
  t.forward(20)
  t.right(65)
  t.forward(41)
  t.right(55)
  t.forward(18)
  t.left(120)
  t.forward(10)
  t.left(90)
  t.forward(53)
  t.right(90)
  t.forward(10)
  t.left(180)
  t.penup()
  t.forward(48)
  
  #I
  t.pendown()
  t.forward(10)
  t.left(90)
  t.forward(45)
  t.left(90)
  t.forward(15)
  t.left(90)
  t.forward(32)
  t.right(180)
  t.forward(33)
  t.penup()
  t.forward(4)
  t.right(90)
  t.pendown()
  t.forward(15)
  t.left(90)
  t.forward(12)
  t.left(90)
  t.forward(15) 
  t.left(90)
  t.forward(12)
  t.penup()
  t.forward(50)
  t.left(90)
  t.forward(20)
  
  #S
  t.pendown()
  t.left(90)
  t.forward(16.5)
  t.right(90)
  t.forward(20)
  t.left(125)
  t.forward(35)
  t.right(35)
  t.forward(16.5)
  t.right(90)
  t.forward(35)
  t.right(115)
  t.forward(16.5)
  t.right(65)
  t.forward(9)
  t.left(125)
  t.forward(35)
  t.right(35)
  t.forward(18)
  t.right(90)
  t.forward(39)
  t.right(180)
  t.penup()
  t.forward(46)
  
  #shape
  t.pensize(2)
  t.pendown()
  t.left(90)
  t.forward(68)
  t.left(90)
  t.forward(236)
  t.left(90)
  t.forward(76)
  t.left(90)
  t.forward(80)
  t.right(90)
  t.forward(76)
  t.left(90)
  t.forward(76)
  t.left(90)
  t.forward(76)
  t.right(90)
  t.forward(80)
  t.left(90)
  t.forward(10)
  t.left(180)
  t.forward(10)
  t.left(90)
  
  #hideturtle
  t.penup()
  t.forward(20)
  
  
  
  t.bye()
  
  
def mainMenu():
    """
    Starts the music
    Calls the function MenuDisplay
    Creates a window named screen of dimensions windowWidth and windowHeight, global variables,
    and assigns different attributes to the window such as caption and icon.
    Passes the window into the main function.
    Closes the window, we do it here because this function is the bookend of the whole program so it ensures that happens 
    everytime and that it happens last.
    """
    pygame.mixer.music.play()
    MenuDisplay()
    
    #Creates the window, moved down here so it does show till after the animation.
    screen = pygame.display.set_mode((windowWidth, windowHeight)) #Named it screen as nostalgia from the Java Days. 
    pygame.display.set_caption("Aggie Land Tetris!")
    windowIcon = pygame.image.load("Texas A&M Logo.png")
    pygame.display.set_icon(windowIcon)
    
    main(screen)#Passes from the window that was created and passed to main menu
    
    """
    Need this or the kernel will die when the window closes, or game over. 
    Really whenever we exit the game loop. But ITS IMPORTANT SO REMEMBER KEEP THIS AS LAST LINE AFTER THE GAME LOOP
    Put it here in the end so I didn't have to keep moving it when adding new functions and screens'
    """
    pygame.display.quit()  
 
mainMenu()  # Runs to start the game