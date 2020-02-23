from PIL import Image
from timeit import default_timer as timer
import pygame
import pygame.gfxdraw

mazeImage = Image.open('mazeSmall.png')
pix = mazeImage.load()
size = mazeImage.size
width = size[0]
height = size[1]
maze = []
solution = []
wasHere = set()
scaleFactor = 4
offset = 2


def mazeCreator():
    for y in range(0, height):
        mazeX = []
        for x in range(0, width):
            if pix[x, y] == (0, 0, 0):
                mazeX.append("B")
            elif pix[x, y] == (255, 255, 255):
                mazeX.append("W")
        maze.append(mazeX)


def findPoints():
    indexA = 0
    pointA = 0
    indexB = 0
    pointB = 0
    try:
        pointA = [i for i, j in enumerate(maze[0]) if j == "W"][0]
        indexA = 0

        if not pointA:
            pointA = [i for i, j in enumerate(maze[height - 1]) if j == "W"][0]
            indexA = height - 1
        else:
            pointB = [i for i, j in enumerate(maze[height - 1]) if j == "W"][0]
            indexB = height - 1
    except:
        pass

    if not pointA:
        for x in range(0, len(maze)):
            if maze[x][0] == "W":
                indexA = x
                pointA = 0
    else:
        for x in range(0, len(maze)):
            if maze[x][0] == "W":
                indexB = x
                pointB = 0

    for x in range(0, len(maze)):
        if maze[x][width - 1] == "W":
            indexB = x
            pointB = width - 1
    return indexA, pointA, indexB, pointB


def recursiveSolve(y, x):
    while (y, x) != (exitY, exitX):
        pos = (y, x)
        wasHere.add((y, x))
        solution.append((y, x))
        visualiseSolver(x, y, (255, 0, 0))
        if maze[y - 1][x] == "W" and (y - 1, x) not in wasHere:
            # print("Up")
            possibleSteps = (y - 1, x)
        elif maze[y][x + 1] == "W" and (y, x + 1) not in wasHere:
            # print("Right")
            possibleSteps = (y, x + 1)
        elif maze[y + 1][x] == "W" and (y + 1, x) not in wasHere:
            # print("Down")
            possibleSteps = (y + 1, x)
        elif maze[y][x - 1] == "W" and (y, x - 1) not in wasHere:
            # print("Left")
            possibleSteps = (y, x - 1)
        else:
            # print("Stuck", pos)
            solution.pop()
            possibleSteps = (solution[-1][0], solution[-1][1])
            solution.pop()
            visualiseSolver(x, y, (255, 255, 255))

        y = possibleSteps[0]
        x = possibleSteps[1]
    solution.append((exitY, exitX))
    visualiseSolver(exitX, exitY, (255, 0, 0))
    print("Solution:", solution)


def printImage():
    for x in solution:
        pix[x[1], x[0]] = (255, 0, 0)
    mazeImage.save("mazeSol.png")


def visualise():
    pygame.init()
    windowSize = 1920, 1080
    screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.DOUBLEBUF)
    screen.set_alpha(None)
    pygame.display.set_caption('Maze Solver')
    screen.fill((255, 255, 255))

    return screen


def visualiseMaze():
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == "B":
                rect = pygame.Rect((x * scaleFactor) + offset, (y * scaleFactor) + offset, scaleFactor, scaleFactor)
                pygame.draw.rect(screen, (0, 0, 0), rect)
                pygame.event.pump()
    pygame.display.flip()


def visualiseSolver(x, y, color):
    rect = pygame.Rect((x * scaleFactor) + offset, (y * scaleFactor) + offset, scaleFactor, scaleFactor)
    pygame.draw.rect(screen, color, rect)
    pygame.display.update(rect)
    pygame.event.pump()


mazeCreator()
(entryY, entryX, exitY, exitX) = findPoints()
print("Entry:", entryY, entryX)
print("Exit:", exitY, exitX)
screen = visualise()
visualiseMaze()
visualiseSolver(entryX, entryY, (0, 255, 0))
visualiseSolver(exitX, exitY, (0, 255, 0))
start = timer()
recursiveSolve(entryY, entryX)
printImage()

timeTaken = timer() - start
print("Time Taken: ", timeTaken)

running = True

while running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
