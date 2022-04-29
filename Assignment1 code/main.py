import Tkinter as tk #change when on ilabs
import math
import heapq

offset = 20

gridfile = open('grid.txt', 'r')
# read first 2 lines which are start and goal
Lines = gridfile.readlines()  # Lines is array now

# read next line which is grid dimensions
# print(Lines[2])
dimensions = Lines[2].split()
# print(dimensions[0])
# print(dimensions[1])
x = int(dimensions[0])
y = int(dimensions[1])

begin = Lines[0].split()
beginx = int(begin[0])
beginy = int(begin[1])

goal = Lines[1].split()
goalx = int(goal[0])
goaly = int(goal[1])

blacklist = list()

squareobstacle = list()

shortestpath = list()

# 30 is offset from border
# 50 is room for information about certain node / point
graphx = x * 15 + 30 + 15 + 50 + 50
graphy = y * 15 + 30 + 50

window = tk.Tk()
window.title('Drawing on a ' + str(graphx) + ' x ' + str(graphy) + ' Grid')
window.geometry(str(graphx) + "x" + str(graphy))

w = tk.Canvas(window, width=graphx, height=graphy)
w.pack()

openlist = list()
closedlist = list()
heap = []
heapcounter = 0

queue = []


class Node:
    def __init__(self, gval=None, hval=None, fval=None):
        self.coordinate = None
        self.parent = None
        self.gval = gval
        self.hval = hval
        self.fval = fval


def createGrid(x, y):
    for h in range(1, y + 1):
        # print(h)
        for i in range(0, x):
            botleft = (i * 15 + offset, (h * 15))
            topright = ((i * 15 + 15 + offset), (h * 15 + 15))
            x1, y1 = botleft
            x2, y2 = topright

            botright = (i * 15 + 15 + offset, (h * 15))
            topleft = ((i * 15 + offset), (h * 15 + 15))
            x3, y3 = botright
            x4, y4 = topleft
            w.create_rectangle(x1, y1, x2, y2, outline='black')
            w.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill='black')
            w.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill='black')
            w.create_oval(x3 - 2, y3 - 2, x3 + 2, y3 + 2, fill='black')
            w.create_oval(x4 - 2, y4 - 2, x4 + 2, y4 + 2, fill='black')


def fillGrid(x, y):
    blacklistedpath = ((x, y), (x, y + 1))  # up and down left side
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x, y + 1), (x, y))
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x, y), (x + 1, y))  # left and right upper
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x + 1, y), (x, y))
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x + 1, y), (x + 1, y + 1))  # up and down right side
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x + 1, y + 1), (x + 1, y))
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x, y + 1), (x + 1, y + 1))  # left and right lower
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x + 1, y + 1), (x, y + 1))
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x, y), (x + 1, y + 1))  # topleft to botright
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x + 1, y + 1), (x, y))
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x + 1, y), (x, y + 1))  # topright to botleft
    blacklist.insert(0, blacklistedpath)
    blacklistedpath = ((x, y + 1), (x + 1, y))
    blacklist.insert(0, blacklistedpath)
    x = x - 1

    # topleft
    x1, y1 = (x * 15) + offset, y * 15
    # botright
    x2, y2 = (x * 15 + 15) + offset, y * 15 + 15
    # botleft
    x3, y3 = (x * 15) + offset, y * 15 + 15
    # topright
    x4, y4 = (x * 15 + 15) + offset, y * 15
    # print(str(x1) + " " + str(y1))
    # print(str(x2) + " " + str(y2))
    # print(str(x3) + " " + str(y3))
    # print(str(x4) + " " + str(y4))
    w.create_rectangle(x1, y1, x2, y2, outline='black', fill='black')

    w.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill='black')
    w.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill='black')
    w.create_oval(x3 - 2, y3 - 2, x3 + 2, y3 + 2, fill='black')
    w.create_oval(x4 - 2, y4 - 2, x4 + 2, y4 + 2, fill='black')


def createSquare(x, y):
    for i in blacklist:
        if (((x, y), (x, y + 1)) == i):
            blacklist.remove(((x, y), (x, y + 1)))
            blacklist.remove(((x, y + 1), (x, y)))
        if (((x, y), (x + 1, y)) == i):
            blacklist.remove(((x, y), (x + 1, y)))
            blacklist.remove(((x + 1, y), (x, y)))
        if (((x + 1, y), (x + 1, y + 1)) == i):
            blacklist.remove(((x + 1, y), (x + 1, y + 1)))
            blacklist.remove(((x + 1, y + 1), (x + 1, y)))
        if (((x, y + 1), (x + 1, y + 1)) == i):
            blacklist.remove(((x, y + 1), (x + 1, y + 1)))
            blacklist.remove(((x + 1, y + 1), (x, y + 1)))
        if (((x, y), (x + 1, y + 1)) == i):
            blacklist.remove(((x, y), (x + 1, y + 1)))
            blacklist.remove(((x + 1, y + 1), (x, y)))
        if (((x + 1, y), (x, y + 1)) == i):
            blacklist.remove(((x + 1, y), (x, y + 1)))
            blacklist.remove(((x, y + 1), (x + 1, y)))

    x = x - 1
    # topleft
    x1, y1 = (x * 15) + offset, y * 15
    # botright
    x2, y2 = (x * 15 + 15) + offset, y * 15 + 15
    # botleft
    x3, y3 = (x * 15) + offset, y * 15 + 15
    # topright
    x4, y4 = (x * 15 + 15) + offset, y * 15

    w.create_rectangle(x1, y1, x2, y2, outline='black')

    w.create_oval(x1 - 2, y1 - 2, x1 + 2, y1 + 2, fill='black')
    w.create_oval(x2 - 2, y2 - 2, x2 + 2, y2 + 2, fill='black')
    w.create_oval(x3 - 2, y3 - 2, x3 + 2, y3 + 2, fill='black')
    w.create_oval(x4 - 2, y4 - 2, x4 + 2, y4 + 2, fill='black')


# line path
def path(startcd, to):
    x1, y1 = startcd
    x2, y2 = to
    x1 = x1 * 15 - 15 + offset
    y1 = (y1 * 15)
    x2 = x2 * 15 - 15 + offset
    y2 = (y2 * 15)
    w.create_line((x1, y1), (x2, y2), fill='red', width=2)


def pathgreen(startcd, to):
    x1, y1 = startcd
    x2, y2 = to
    x1 = x1 * 15 - 15 + offset
    y1 = (y1 * 15)
    x2 = x2 * 15 - 15 + offset
    y2 = (y2 * 15)
    w.create_line((x1, y1), (x2, y2), fill='green', width=2)


def drawShortestPath(array):
    for h, j in zip(array, array[1:]):
        pathgreen(h, j)


def createStart():
    point = Lines[0].split()
    x1 = int(point[0])
    y1 = int(point[1])
    x1 = x1 * 15 - 15 + offset
    y1 = (y1 * 15)
    w.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, outline='red', fill='red')


def createGoal():
    point = Lines[1].split()
    x1 = int(point[0])
    y1 = int(point[1])
    x1 = x1 * 15 - 15 + offset
    y1 = (y1 * 15)
    w.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, outline='green', fill='green')


def aheuristic(point):
    x1, y1 = point
    x1, y1 = int(x1), int(y1)

    straight = math.sqrt(2) * min(math.fabs(x1 - goalx), math.fabs(y1 - goaly)) + max(math.fabs(x1 - goalx),
                                                                                      math.fabs(y1 - goaly)) - min(
        math.fabs(x1 - goalx), math.fabs(y1 - goaly))
    # print("heuristic: " + str(straight))
    return straight


def thetaheuristic(point):
    x1, y1 = point
    x1, y1 = int(x1), int(y1)

    straight = math.sqrt(((math.fabs(x1 - goalx)) ** 2) + ((math.fabs(y1 - goaly)) ** 2))
    # print("thetaheuristic: " + str(straight))
    return straight


def pathCost(start, to):
    startx, starty = start
    tox, toy = to
    cost = math.sqrt(math.pow(math.fabs(starty - toy), 2) + math.pow(math.fabs(startx - tox), 2))
    # print("cost: " + str(cost))
    return cost


def acalculateSurrounding(node, surrounding):
    limit = (x + 1, y + 1)
    if (node.coordinate[0] <= limit[0] and node.coordinate[1] <= limit[1]):  # within the grid
        h = aheuristic(surrounding)


def checkBlackList(coordinate):
    if coordinate in squareobstacle:
        return True
    else:
        return False


def LineOfSight(node, surrounding):
    x0, y0 = node.coordinate
    x1, y1 = surrounding
    count = 0
    dy = y1 - y0
    dx = x1 - x0

    if dy < 0:
        dy = -dy
        sy = -1
    else:
        sy = 1

    if dx < 0:
        dx = -dx
        sx = -1
    else:
        sx = 1

    if dx >= dy:
        while x0 != x1:
            count = count + dy
            if count >= dx:
                if checkBlackList((x0 + ((sx - 1) / 2), y0 + ((sy - 1) / 2))):
                    return False
                y0 = y0 + sy
                count = count - dx
            if count != 0 and checkBlackList((x0 + ((sx - 1) / 2), y0 + ((sy - 1) / 2))):
                return False
            if dy == 0 and checkBlackList((x0 + ((sx - 1) / 2), y0)) and checkBlackList((x0 + ((sx - 1) / 2), y0 - 1)):
                return False
            x0 = x0 + sx
    else:
        while y0 != y1:
            count = count + dx
            if count >= dy:
                if checkBlackList((x0 + ((sx - 1) / 2), y0 + ((sy - 1) / 2))):
                    return False
                x0 = x0 + sx
                count = count - dy
            if count != 0 and checkBlackList((x0 + ((sx - 1) / 2), y0 + ((sy - 1) / 2))):
                return False
            if dy == 0 and checkBlackList((x0, y0 + ((sy - 1) / 2))) and checkBlackList((x0 - 1, y0 + ((sy - 1) / 2))):
                return False
            y0 = y0 + sy

    return True

def searchforVertex():
    vertexSearch = raw_input("Please type in a vertex coordinate in format: x,y to show its information")
    if vertexSearch.isalpha():
        print("Input was incorrect, try again")

    coord = tuple(map(int, vertexSearch.split(',')))
    if len(coord) < 2:
        print("Input was not formatted correctly, try again")
    for i in heap:
        if coord == i[2].coordinate:
            print("Information on node: " + str(i[2].coordinate))
            print("gvalue: " + str(i[2].gval))
            print("hvalue: " + str(i[2].hval))
            print("fvalue: " + str(i[2].fval))
            return
    for i in closedlist:
        if coord == i.coordinate:
            print("Information on node: " + str(i.coordinate))
            print("gvalue: " + str(i.gval))
            print("hvalue: " + str(i.hval))
            print("fvalue: " + str(i.fval))
            return
    print("Could not find info on " + vertexSearch)
    return

def nodeInfo(node): #h, g and f values conputed
    print("Information on node: " + str(node.coordinate))
    print("gvalue: " + str(node.gval))
    print("hvalue: " + str(node.hval))
    print("fvalue: " + str(node.fval))

def bfs(): # true or false
    visited = []
    queue.append((beginx, beginy))
    while queue:
        current = queue.pop(0)
        currentx, currenty = current
        if current == (goalx, goaly):
            return True
        surrounding = [((currentx - 1), (currenty - 1)), (currentx, (currenty - 1)),
                       ((currentx + 1), (currenty - 1)), ((currentx - 1), currenty),
                       ((currentx + 1), currenty), ((currentx - 1), (currenty + 1)),
                       (currentx, (currenty + 1)), ((currentx + 1), (currenty + 1))]
        for j in surrounding:
            # print(j)
            surroundingx, surroundingy = j
            if x + 1 >= surroundingx > 0 and y + 1 >= surroundingy > 0 and j not in visited and (current, j) not in blacklist and j not in queue:
                queue.append(j)

        visited.append(current)
    return False



if __name__ == '__main__':
    print("Initializing...")
    createGrid(x, y)
    nodeButton = tk.PhotoImage(file="button2.png")

    # read txt file for blackspots
    for line in range(3, len(Lines)):
        gridinfo = Lines[line].split()
        if int(gridinfo[2]) == 1:
            fillGrid(int(gridinfo[0]), int(gridinfo[1]))
            squareobstacle.insert(0, (int(gridinfo[0]), int(gridinfo[1])))
    for line in range(3, len(Lines)):  # put the lines back for some squares
        gridinfo = Lines[line].split()
        if int(gridinfo[2]) == 0:
            createSquare(int(gridinfo[0]), int(gridinfo[1]))
    createStart()
    createGoal()

    start = Node(gval=0, hval=aheuristic((beginx, beginy)), fval=0 + aheuristic((beginx, beginy)))
    start.coordinate = (beginx, beginy)
    heapq.heappush(heap, (start.fval, heapcounter, start)) #HEAP
    heapcounter += 1
    button = tk.Button(window, image=nodeButton, borderwidth=0, command=searchforVertex)
    button.place(x=(x * 15) + 20 + offset, y=y * 15)
    w.create_text((x * 15) + 50 + offset, y * 15 - 30, text="Press Button\n to find \ninfo on a vertex")

    # openlist.insert(0, start)
    prev = start.coordinate
    foundPath = False

    istheta = False
    while True:
        aortheta = raw_input('Type "a" for A* or "t" for Theta*') # change to raw_input in ilabs
        if aortheta == 'a':
            print("doing A")
            istheta = False
            break
        elif aortheta == 't':
            print("doing theta")
            istheta = True
            break
        else:
            print("Input is incorrect, please type in correct letter")
            # keep input method until correct letter ***********************

    reachable = True
    if bfs() is not True:
        reachable = False

    while heap:
        if reachable is not True:
            break

        count = heapq.heappop(heap)[2]
        prev = count.coordinate
        if count.parent is not None:
            path(count.parent.coordinate, count.coordinate)
        if count.hval == 0:
            closedlist.insert(0, count)
            print("path found")
            print("path is: ")
            while count:
                shortestpath.insert(0, count.coordinate)
                count = count.parent

            print(shortestpath)
            drawShortestPath(shortestpath)
            foundPath = True
            break

        temppointx, temppointy = count.coordinate
        surrounding = [((temppointx - 1), (temppointy - 1)), (temppointx, (temppointy - 1)),
                       ((temppointx + 1), (temppointy - 1)), ((temppointx - 1), (temppointy)),
                       ((temppointx + 1), (temppointy)), ((temppointx - 1), (temppointy + 1)),
                       ((temppointx), (temppointy + 1)), ((temppointx + 1), (temppointy + 1))]
        for i in surrounding:  # make sure it is in the range of the grid and NOT BLACKLISTED
            surroundingx, surroundingy = i
            # print(i)
            if surroundingx > x + 1 or surroundingy > y + 1 or surroundingx < 1 or surroundingy < 1 or (
                    count.coordinate, i) in blacklist:  # CHECK IF IN RANGE AND NOT BLACKLISTED PATH
                continue
            isInClosed = False
            isInOpened = False

            for closednodes in closedlist:
                if i == closednodes.coordinate:
                    isInClosed = True
                    break
            if isInClosed == False:
                # updateVertex portion
                if istheta:  # theta* algorithm

                    if count.parent and LineOfSight(count.parent, i):
                        gsprime = count.gval + pathCost(count.coordinate, i)
                        if count.parent.gval + pathCost(count.parent.coordinate, i) < gsprime:
                            tempnode = Node(gval=count.parent.gval + pathCost(count.parent.coordinate, i), hval=thetaheuristic(i), fval=count.parent.gval + pathCost(count.parent.coordinate, i) + thetaheuristic(i))
                            tempnode.parent = count.parent
                            tempnode.coordinate = i
                            for openednodes in heap:
                                if i == openednodes[2].coordinate:
                                    heap.remove(openednodes)
                                    heapq.heapify(heap)
                                    break
                            # openlist.insert(0, tempnode)
                            heapq.heappush(heap, (tempnode.fval, heapcounter, tempnode))
                            heapcounter += 1
                    else:
                        for openednodes in heap:
                            if (i == openednodes[2].coordinate and pathCost(openednodes[2].coordinate,
                                                                         count.coordinate) + count.gval < openednodes[2].gval):
                                # print("found better path")
                                isInOpened = True
                                heap.remove(openednodes)
                                heapq.heapify(heap)
                                tempnode = Node(gval=count.gval + pathCost(count.coordinate, i),
                                                hval=aheuristic(i),
                                                fval=count.gval + pathCost(count.coordinate, i) + aheuristic(i))
                                tempnode.coordinate = i
                                tempnode.parent = count
                                # openlist.insert(0, tempnode)
                                heapq.heappush(heap, (tempnode.fval, heapcounter, tempnode))
                                heapcounter += 1
                                break
                        if not isInOpened:
                            tempnode = Node(gval=count.gval + pathCost(count.coordinate, i), hval=aheuristic(i),
                                            fval=count.gval + pathCost(count.coordinate, i) + aheuristic(i))
                            tempnode.coordinate = i
                            tempnode.parent = count
                            # openlist.insert(0, tempnode)
                            heapq.heappush(heap, (tempnode.fval, heapcounter, tempnode))
                            heapcounter += 1
                else:  # A* algorithm

                    for openednodes in heap:
                        if (i == openednodes[2].coordinate and pathCost(openednodes[2].coordinate,
                                count.coordinate) + count.gval < openednodes[2].gval):
                            # print("found better path")
                            isInOpened = True
                            heap.remove(openednodes)
                            heapq.heapify(heap)
                            tempnode = Node(gval=count.gval + pathCost(count.coordinate, i),
                                            hval=aheuristic(i),
                                            fval=count.gval + pathCost(count.coordinate, i) + aheuristic(i))
                            tempnode.coordinate = i
                            tempnode.parent = count
                            # openlist.insert(0, tempnode)
                            heapq.heappush(heap, (tempnode.fval, heapcounter, tempnode))
                            heapcounter += 1
                            break
                    if not isInOpened:
                        tempnode = Node(gval=count.gval + pathCost(count.coordinate, i), hval=aheuristic(i),
                                        fval=count.gval + pathCost(count.coordinate, i) + aheuristic(i))
                        tempnode.coordinate = i
                        tempnode.parent = count
                        # openlist.insert(0, tempnode)
                        heapq.heappush(heap, (tempnode.fval, heapcounter, tempnode))
                        heapcounter += 1

        closedlist.insert(0, count)
    if not foundPath:
        print("Goal is potentially blocked")
        print("No Successful path found :(")
    w.create_text(offset + 15, graphy - 50 + 10, text="Start")
    w.create_text(offset + 15, graphy - 50 + 10 + 15, text="Goal")
    w.create_oval(offset - 2, graphy - 50 + 10 + 2, offset + 2, graphy - 50 + 10 - 2, fill='red', outline='red')
    w.create_oval(offset - 2, graphy - 50 + 10 + 15 + 2, offset + 2, graphy - 50 + 10 + 15 - 2, fill='green', outline='green')

    w.create_text(offset + 15 + 80, graphy - 50 + 10, text="Explored Paths")
    w.create_text(offset + 15 + 80, graphy - 50 + 10 + 15, text="Shortest Path")
    w.create_line(offset + 50 - 10, graphy - 50 + 10, offset + 50 + 15 - 10, graphy - 50 + 10, fill='red', width=2)
    w.create_line(offset + 50 - 5, graphy - 50 + 10 + 15, offset + 50 + 15 - 5, graphy - 50 + 10 + 15, fill='green', width=2)

    window.mainloop()