import time
import graphics
#Python has a graphics package, which was downloaded and imported 
from graphics import *
#Imports copy of original grid and numbers as a blank slate
import copy

def displayGrid(grid):
    for row in grid:
        print(row)

def filled(grid):
    for row in grid:
        if 0 in row:
            #0 means not filled in
            return(0)
    #1 means all filled in
    return(1)

def fillSolution():
    step = 0
    rules = ["This was the only candidate in this cell",
             "This was the only cell in this row that could be filled by the candidate",
             "This was the only cell in this column that could be filled by the candidate",
             "This was the only cell in this sub-block, a 3x3 square, that could be filled by the candidate",
             "This number was tried out"]
    for item in trace:
        step = step + 1
        print("Step", step, ":", item[0], item[1], "---->", item[2], "--", rules[item[3] - 1])
        number = Text(Point(21 + 40 * item[1], 21 + 40 * item[0]), item[2])
        #Number filled in by the program will momentarily appear red and bold
        number.setTextColor('red')
        number.setStyle('bold')
        number.setSize(26)
        number.draw(win)
        #Sleep time prevents numbers from all showing up at once
        time.sleep(0.1)
        number.setSize(16)
        if item[3] == 5:
            #Use a different color for a number that was tried out
            number.setTextColor('red')
        else:
            number.setTextColor('magenta')
            number.setStyle('normal')
        time.sleep(0.1)

def drawGrid():
    for i in range(10):
        #Defines where the lines are drawn; a couple extra pixels are given for the thick borders
        hline = Line(Point(1, 40 * i + 1), Point(362, 40 * i + 1))
        vline = Line(Point(40 * i + 1, 1), Point(40 * i + 1, 362))
        #Every third line will be thick because it defines a sub-block
        if i % 3 == 0:
            hline.setWidth(3)
            vline.setWidth(3)
        hline.draw(win)
        vline.draw(win)

#Fill in numbers originally given in the puzzle
def fillKnownNumbers():
    for i in range(9):
        for j in range(9):
            if originalGrid[i][j] != 0:
                #This sets the position of the number in the middle of each cell
                number = Text(Point(21 + 40 * j, 21 + 40 * i), originalGrid[i][j])
                number.setSize(16)
                number.draw(win)

def isValidSolution(grid):
    refSet = set(range(1, 10))
    for i in range(9):
        tmpRow = set(grid[i])
        tmpCol = set([grid[k][i] for k in range(9)])
        blockRow = i // 3;
        blockCol = i % 3;
        tmpBlock = [grid[k][blockCol*3:blockCol*3+3] for k in range(blockRow*3,blockRow*3+3)]
        #Collapses from 2-D to 1-D list and changes into set
        tmpBlock = set([element for row in tmpBlock for element in row])
        if tmpRow != refSet or tmpCol != refSet or tmpBlock != refSet:
            return(0)
    return(1)

def createCandidates(grid):
    loopAgain = 1
    while loopAgain:
        loopAgain = 0

        #Find out the candidates for each unfilled cell
        candidates = []
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    #If a cell has been filled up, there are no candidates
                    candidates.append([])
                else:
                    #If a cell has not been filled up, the candidates are numbers from 1 to 9 excluding the numbers in the same line, same column and the same sub-block
                    tmpCandidates = set(range(1, 10))
                    tmpRow = set(grid[i])
                    tmpCol = set([grid[k][j] for k in range(9)])
                    blockRow = i // 3;
                    blockCol = j // 3;
                    tmpBlock = [grid[k][blockCol*3:blockCol*3+3] for k in range(blockRow*3,blockRow*3+3)]
                    #Collapses from 2-D to 1-D list and changes into set
                    tmpBlock = set([element for row in tmpBlock for element in row])
                    tmpCandidates = tmpCandidates - tmpRow
                    tmpCandidates = tmpCandidates - tmpCol
                    tmpCandidates = tmpCandidates - tmpBlock
                    #Changes back to a list
                    tmpCandidates = list(tmpCandidates)
                    candidates.append(tmpCandidates)
                    if len(tmpCandidates) == 1:
                        grid[i][j] = tmpCandidates[0]
                        print(i, j, "---->", grid[i][j], ": Rule #1 -- The only candidate in an unsolved cell.")
                        trace.append([i, j, grid[i][j], 1])
                        loopAgain = 1
                    elif len(tmpCandidates) == 0:
                        print("Error! Unsuccessful tryout.")
                        return(1, grid, candidates)

        #If the "only candidate" rule cannot solve the puzzle, check that in the whole row, column, or sub-block, only one cell contains a certain number as a candidate
        if loopAgain == 0 and not filled(grid):
            for i in range(9):
                for j in range(9):
                    #Check candidates in row
                    if grid[i][j] == 0:
                        tmpCandidates = candidates[9 * i + j]
                        for k in range(9):
                            if k != j:
                                tmpCandidates = list(set(tmpCandidates) - set(candidates[9 * i + k]))
                                if len(tmpCandidates) == 0:
                                    break
                        if len(tmpCandidates) == 1:
                            grid[i][j] = tmpCandidates[0]
                            print(i, j, "---->", grid[i][j], ": Rule #2 -- The only number in a row.")
                            trace.append([i, j, grid[i][j], 2])
                            loopAgain = 1

                    #Check candidates of column if the current cell is still not filled
                    if grid[i][j] == 0:
                        tmpCandidates = candidates[9 * i + j]
                        for k in range(9):
                            if k != i:
                                tmpCandidates = list(set(tmpCandidates) - set(candidates[9 * k + j]))
                                if len(tmpCandidates) == 0:
                                    break
                        if len(tmpCandidates) == 1:
                            grid[i][j] = tmpCandidates[0]
                            print(i, j, "---->", grid[i][j], ": Rule #3 -- The only number in a column.")
                            trace.append([i, j, grid[i][j], 3])
                            loopAgain = 1

                    #Check candidates od sub-block if the current cell is still not filled
                    if grid[i][j] == 0:
                        tmpCandidates = candidates[9 * i + j]
                        blockRow = i // 3;
                        blockCol = j // 3;
                        for k in range(9):
                            rowNumber = blockRow * 3 + k // 3
                            colNumber = blockCol * 3 + k % 3
                            if rowNumber != i or colNumber != j:
                                tmpCandidates = list(set(tmpCandidates) - set(candidates[9 * rowNumber + colNumber]))
                                if len(tmpCandidates) == 0:
                                    break
                        if len(tmpCandidates) == 1:
                            grid[i][j] = tmpCandidates[0]
                            print(i, j, "---->", grid[i][j], ": Rule #4 -- The only number in a sub-block.")
                            trace.append([i, j, grid[i][j], 4])
                            loopAgain = 1

    if filled(grid):
        if isValidSolution(grid):
            displayGrid(grid)
            print("Sudoku puzzle is solved!")
            print("Solution Steps:")
            fillSolution()
            return(0, grid, candidates)
        else:
            print("Wrong solution! Unsuccessful tryout.")
            displayGrid(grid)
            return(1, grid, candidates)
    else:
        print("Sudoku puzzle is NOT solved! Tryout needed.")
        return(2, grid, candidates)

def tryOut(grid, candidates):
    global trace
    #Keeps a copy of the steps as a starting point if the number that is tried does not work
    traceBackup = copy.deepcopy(trace)
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                #Tells the program to try out numbers from the list of candidates for a cell
                for triedNumber in candidates[i * 9 + j]:
                    #Keeps a copy of the grid in the case that the number that is tried does not work
                    myGrid = copy.deepcopy(grid)
                    trace = copy.deepcopy(traceBackup)
                    myGrid[i][j] = triedNumber
                    print(i, j, "---->", myGrid[i][j], ": Rule #5 -- This is a tryout.")
                    trace.append([i, j, myGrid[i][j], 5])
                    status, tmpGrid, tmpCandidates = createCandidates(myGrid)
                    #If status = 2, then retry with a different number
                    if status == 2:
                        if tryOut(tmpGrid, tmpCandidates) == 0:
                            #Success!
                            return(0)
                    elif status == 0:
                        #Success!
                        return(0)
                    #Status 1 indicates an error or lack of candidates for a cell;
                    #it should only occur when a tried number does not work

#Sudoku

#Example of simple puzzle, can be solved by Rule #1 -- the only candidate in an unsolved cell

##originalGrid = [[4,0,0,0,0,0,3,2,0],
##                [0,8,5,2,4,0,9,0,7],
##                [0,0,1,0,0,0,0,0,4],
##                [0,0,0,8,0,0,0,9,0],
##                [0,0,6,7,2,5,1,0,0],
##                [1,4,0,0,0,3,0,0,0],
##                [8,0,0,0,0,0,7,0,0],
##                [6,0,9,0,3,1,8,5,0],
##                [0,2,3,0,0,0,0,0,1]]

#Example of medium puzzle, has to go through Rules #2/#3/#4 -- the only number in a row/column/subblock

##originalGrid = [[8,0,7,5,0,0,0,0,1],
##                [0,0,0,1,0,0,4,0,0],
##                [0,0,0,0,2,7,0,9,0],
##                [7,0,0,0,1,0,9,6,4],
##                [5,0,0,0,0,0,0,0,3],
##                [6,9,8,0,7,0,0,0,2],
##                [0,5,0,4,8,0,0,0,9],
##                [0,0,9,0,0,1,0,0,0],
##                [1,0,0,0,0,2,3,0,5]]

#Example of hard puzzle, has to go through Rule #5 -- try numbers out at certain steps.

originalGrid = [[3,0,0,0,4,0,8,1,0],
                [0,0,0,0,0,0,7,0,3],
                [0,0,1,2,0,0,0,0,0],
                [0,0,0,0,0,4,0,7,0],
                [8,0,6,0,0,0,1,0,9],
                [0,4,0,1,0,0,0,0,0],
                [0,0,0,0,0,7,3,0,0],
                [1,0,9,0,0,0,0,0,0],
                [0,8,7,0,2,0,0,0,6]]

#Another hard puzzle, has to go through Rule #5 -- try numbers out at certain steps.

##originalGrid = [[3,4,0,0,6,0,7,0,9],
##                [0,0,0,0,0,0,0,2,0],
##                [0,0,2,0,5,9,0,0,0],
##                [5,3,0,0,7,0,0,0,0],
##                [0,0,0,0,0,0,0,0,0],
##                [0,0,0,0,2,0,0,4,1],
##                [0,0,0,1,4,0,8,0,0],
##                [0,5,0,0,0,0,0,0,0],
##                [7,0,8,0,9,0,0,1,5]]

#Draw the sudoku grid
win = GraphWin('Sudoku', 363, 363)
win.setBackground('white')
#Defines the location of the window on the screen
x = 10
y = 10
win.master.geometry('%dx%d+%d+%d' % (363, 363, x, y))
drawGrid()

#Fill in the sudoku numbers given by puzzle
fillKnownNumbers()

trace = []

#createCandidates creates candidates for a cell and fills in cells if
#only one candidate in cell or candidate that appears in only one cell
#in a row, column, or sub-block
status, grid, candidates = createCandidates(originalGrid)

#Not solved yet, need to try numbers out
if status == 2:
    tryOut(grid, candidates)
