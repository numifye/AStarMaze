# Author: Naomi Campbell

import sys
import math


class Node:
    def __init__(self,x,y,p):
        self.x = x
        self.y = y
        self.parent = p  # not used
        self.f = 0


class AStarMaze:
    def __init__(self, mazeList, heuristic):
        self.maze = mazeList
        self.h = heuristic
        self.numRows = len(mazeList)
        self.numCols = len(mazeList[0])
        self.costSoFar = 0  # c in  A* --> f = c+h
        self.x = 0  # keep track of last move
        self.y = 0  # keep track of last move
        self.frontier = []  # ordered by f=c+h
        self.explored = set([])
        self.success = False

    def push(self, node):
        self.frontier.append(node)

    def pop(self):
        return self.frontier.pop()

    # function to see if node is in the list or set (variable box)
    def is_in(self, node, box):
        for item in box:
            if item.x == node.x and item.y == node.y:
                return True
        return False

    # function play begin the game
    def play(self):
        # get nario's initial coordinates
        x = self.numRows - 1  # nario is initially always in last row
        y = self.maze[self.numRows - 1].index('@')
        # create node & add to frontier
        node = Node(x, y, None)
        node.f = self.costSoFar + self.calc_heurist(0,0,node.x,node.y)
        self.push(node)

        # loop do
        while True:
            if len(self.frontier) == 0:
                self.success = False
                break
            node = self.pop()
            # move nario to location of popped node & draw
            self.move_nario(node); self.draw(); print('\n')
            # after maze is drawn
            if (node.x == 0 and node.y == 0):  # if node just popped == goal state
                self.success = True
                break
            self.costSoFar += 1  # cost +1 in f = c+h
            self.explored.add(node)
            self.x = node.x; self.y = node.y  # set x and y to node just popped
            # for each move (up, down, left, right, wrapl, wrapr)
            # from node, get adjacent squares in a list
            children = self.get_children(node)
            for child in children:
                if not (self.is_in(child, self.frontier) or self.is_in(child, self.explored)):
                    self.push(child)
                    # sort frontier after add
                    sorted(self.frontier, key=lambda node:node.f, reverse=True)
                # remove successors already on queue with higher f
                elif self.is_in(child, self.frontier):
                    for item in self.frontier:
                        # find the node w/ equivalent state
                        if item.x == child.x and item.y == child.y:
                            if item.f > child.f:
                                self.frontier.remove(item)
                                self.push(child)
                                sorted(self.frontier, key=lambda node: node.f, reverse=True)
        if self.success == False:
            print('NO PATH')
        else:
            print('Nario reached the goal')

    def get_children(self, parent):
        children = []
        child = None
        # wrap around to left if at column 0 & free square in last column
        if parent.y == 0 and self.maze[parent.x][self.numCols-1] != '=':
            child = Node(parent.x, self.numCols-1, parent)
            child.f = self.costSoFar + self.calc_heurist(0, 0, child.x, child.y)
            children.append(child)
        # wrap around to right if at last column & square in column 0
        if self.y == self.numCols-1 and self.maze[parent.x][0] != '=':
            child = Node(parent.x, 0, parent)
            child.f = self.costSoFar + self.calc_heurist(0, 0, child.x, child.y)
            children.append(child)
        # left
        if self.y > 0 and self.maze[parent.x][parent.y-1] != '=':
            child = Node(parent.x, parent.y-1, parent)
            child.f = self.costSoFar + self.calc_heurist(0, 0, child.x, child.y)
            children.append(child)
        # right
        if self.y < self.numCols-1 and self.maze[parent.x][parent.y + 1] != '=':
            child = Node(parent.x, parent.y+1, parent)
            child.f = self.costSoFar + self.calc_heurist(0, 0, child.x, child.y)
            children.append(child)
        # up
        if self.x > 0 and self.maze[parent.x-1][parent.y] != '=':
            child = Node(parent.x-1, parent.y, parent)
            child.f = self.costSoFar + self.calc_heurist(0, 0, child.x, child.y)
            children.append(child)
        # down
        if self.x < self.numRows-1 and self.maze[parent.x+1][parent.y] != '=':
            child = Node(parent.x+1, parent.y, parent)
            child.f = self.costSoFar + self.calc_heurist(0, 0, child.x, child.y)
            children.append(child)
        return children

    # function places nario in new location, replaces old
    # square with '.', and updates nario's coordinates
    def move_nario(self, node):
        #write a "." at old location
        row = ""
        for i in range(self.numCols):
            if i == self.y:
                row += "."
            else:
                row += self.maze[self.x][i]
        self.maze[self.x] = row
        #put nario in new location
        self.add(node)

    # function is helper for move_nario function, places nario in new location
    def add(self, node):
        row = ""
        for i in range(self.numCols):
            if i == node.y:
                # if i matches column, row string += piece at column i
                row += '@'
            else:
                # otherwise, row += [row x][current column]
                row += self.maze[node.x][i]
        self.maze[node.x] = row  # replace row x with new row

    # function draw draws the maze
    def draw(self):
        for i in range(self.numRows):
            print(self.maze[i])  # print every row in maze

    # function uses specified heuristic and returns calculation
    def calc_heurist(self, x1, y1, x2, y2):
        if self.h == 'manhattan':  # gets manhattan distance |x1-x2| + |y1-y2|
            x3 = abs(x1 - x2)
            y3 = abs(y1 - y2)
            return x3 + y3
        if self.h == 'euclidian':  # gets euclidian distance sqrt((x1-x2)^2 + (y1-y2)^2)
            x3 = (x1 - x2) ** 2
            y3 = (y1 - y2) ** 2
            return math.sqrt(x3 + y3)
        if self.h == 'my_own':
            a = abs(x1 - y1)
            b = abs(x2 - y2)
            return math.sqrt(a + b)


def main():
    if (len(sys.argv)) != 3:
        print('Please supply a filename and heuristic')
        raise SystemExit(1)
    f = open(sys.argv[1])
    lines = f.read().splitlines()  # readlines()
    f.close()
    heuristic = ''
    heuristic += sys.argv[2]
    maze = AStarMaze(lines, heuristic)
    maze.play()

if __name__ == '__main__':
    main()