import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#", "#", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", "#", " ", "#", " ", "#", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ", "#"],
    ["O", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", " ", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", " ", "#", "#", " ", " ", "#", " ", "X"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", "#"],
    ["#", " ", "#", "#", "#", "#", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", "#", " ", "#", "#", "#", " ", " ", " ", "#"],
    ["#", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    findPath(maze, stdscr)
    stdscr.getch()


def printMaze(maze, stdscr, path):
    blue = curses.color_pair(1)
    red = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, element in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 3, "X", red)
            else:
                stdscr.addstr(i, j * 3, element, blue)


def findPath(maze, stdscr):

    # This function will be based on the Breadth First Search algorithm that is used to find the
    # shortest path in unweighted graphs. It will involve finding the neighbouring vertices of a
    # starting vertex and then finding the neighbours of those neighbours. This process will repeat
    # and stop as soon as the ending vertex is found in a given path.

    start = "O"
    end = "X"
    startVertexPos = findStart(maze, start)

    currentPath = [startVertexPos]  # list of vertex positions representing the path, beginning with the start vertex
    q = queue.Queue()
    q.put(currentPath)  # initialize the queue with the current path
    visited = []  # list to keep track of already visited vertices

    while not q.empty():
        currentPath = q.get()  # update the current path from the queue
        currentVertexPos = currentPath[-1]  # the last index of the current path will contain the new current vertex
        row, col = currentVertexPos

        # print current path
        stdscr.clear()
        printMaze(maze, stdscr, currentPath)
        time.sleep(0.1)
        stdscr.refresh()

        if maze[row][col] == end:
            return currentPath

        neighbours = findNeighbours(maze, row, col)  # find all neighbours for current vertex

        for neighbour in neighbours:
            if neighbour in visited:
                continue

            rowN, colN = neighbour
            # if a neighbour is a valid vertex, then create a new path which involves the previous path
            # and the current vertex's position
            if maze[rowN][colN] == " " or maze[rowN][colN] == end:
                newPath = currentPath + [neighbour]
                # queue all neighbour position(s) and the new path(s) so that they will become the
                # current vertex/current path on the next iterations of the algorithm
                q.put(newPath)
                visited.append(neighbour)  # mark the neighbour as being visited


def findNeighbours(maze, row, col):
    neighbours = []

    if row > 0:  # checking for neighbours above
        neighbours.append((row - 1, col))
    if row < len(maze) - 1:  # checking for neighbours below
        neighbours.append((row + 1, col))
    if col > 0:  # checking for neighbours to the left
        neighbours.append((row, col - 1))
    if col < len(maze[0]) - 1:  # checking for neighbours to the right
        neighbours.append((row, col + 1))
    if (row > 0 and col > 0) and (row < len(maze[0]) - 1 and col < len(maze) - 1):  # checking for diagonal neighbours
        neighbours.append((row + 1, col + 1))
        neighbours.append((row - 1, col - 1))
        neighbours.append((row + 1, col - 1))
        neighbours.append((row - 1, col + 1))

    return neighbours


def findStart(maze, start):
    for i, row in enumerate(maze):
        for j, element in enumerate(row):
            if element == start:
                return i, j
    return None


wrapper(main)
