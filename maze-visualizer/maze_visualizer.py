import curses
from curses import wrapper
import queue
import time



maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
] #9x9 2D array

def printMaze(maze, stdscr, path=[]):
    BLUE=curses.color_pair(1) #Default maze colour
    RED=curses.color_pair(2) #Path colour

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i,j*2,"X", RED)
            else:
                stdscr.addstr(i,j*2,value, BLUE)


            
def findStart(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value ==start:
                return i, j
    return None
    

def findPath(maze, stdscr):
    start="O"
    end="X"
    startPos=findStart(maze,start)

    q=queue.Queue() #First in first out data structure
    q.put((startPos, [startPos])) #Current position, path so far

    visited=set()

    while not q.empty():
        currentPosition, path = q.get() #Returns the element at the front of the queue
        row, col = currentPosition

        stdscr.clear()
        printMaze(maze, stdscr, path)
        time.sleep(0.3)
        stdscr.refresh()

        if maze[row][col]==end:
            return path
        
        neighbors=findNeighbors(maze,row,col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r,c=neighbor #Breaks down the tuple (row,column)
            if maze[r][c]=="#":
                continue

            newPath=path+[neighbor] #Current path + current neighbor
            q.put((neighbor, newPath))  
            visited.add(neighbor) 

def findNeighbors(maze, row, col):
    neighbors=[]

    if row>0: #Move up
        neighbors.append((row-1, col)) #Passing 1 value, a 2D position
    if row+1< len(maze): #Move down
        neighbors.append((row+1,col))
    if col>0: #Move left
        neighbors.append((row,col-1))
    if col+1< len(maze[0]): #Move right
        neighbors.append((row,col+1))
    
    return neighbors


def main(stdscr):
    curses.init_pair(1,curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED, curses.COLOR_BLACK)
    blue_and_black=curses.color_pair(1)


    findPath(maze,stdscr)
    stdscr.getch()



wrapper(main) #Initializes the curses modulde, calls the function and passes the stdscr object
