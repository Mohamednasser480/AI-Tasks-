from collections import deque
from queue import PriorityQueue
from math import *
import collections
class Node:

    id = None  # Unique value for each node.
    up = None  # Represents value of neighbors (up, down, left, right).
    down = None
    right = None
    left = None
    previousNode = None  # Represents value of neighbors.
    edgeCost = None  # Represents the cost on the edge from any parent to this node.
    gOfN = None  # Represents the total edge cost
    hOfN = None  # Represents the heuristic value
    heuristicFn = None  # Represents the value of heuristic function

    def __init__(self, value):
        self.value = value


class SearchAlgorithms:
    ''' * DON'T change Class, Function or Parameters Names and Order
        * You can add ANY extra functions,
          classes you need as long as the main
          structure is left as is '''
    path = []  # Represents the correct path from start node to the goal node.
    fullPath = []  # Represents all visited nodes from the start node to the goal node.
    totalCost = -1  # Represents the total cost in case using UCS, AStar (Euclidean or Manhattan)

    def __init__(self, mazeStr, edgeCost=None):
        ''' mazeStr contains the full board
         The board is read row wise,
        the nodes are numbered 0-based starting
        the leftmost node'''
        self.nodedata = self.setdata(mazeStr, edgeCost)

        # self.read(self.mazeStr)

        pass


    def setdata(self, mazeStr, edgeCost):
        nodedata = []
        maze = []
        for i in mazeStr.split(' '):
            cell = i.split(',')
            maze.append(cell)
        counter = 0
        for i in maze:
            l = []
            for j in i:
                n = Node(j)
                n.p=500;
                if j == "S":
                    n.gOfN = 0
                if edgeCost == None:
                    n.edgeCost = 1
                if edgeCost!=None:
                    n.edgeCost = edgeCost[counter]

                n.id = counter
                counter =counter+ 1
                l.append(n)

            nodedata.append(l)



        for x in range(len(nodedata)):
            for y in range(len(nodedata[x])):
                if x != 0:
                    nodedata[x][y].up = nodedata[x - 1][y]

                if x == 0:
                    nodedata[x][y].up = None
                if y !=0:
                    nodedata[x][y].left = nodedata[x][y - 1]

                if y == 0:
                    nodedata[x][y].up = None

                if x < nodedata.__len__() - 1:
                    nodedata[x][y].down = nodedata[x + 1][y]
                if y <nodedata[x].__len__() - 1:
                    nodedata[x][y].right = nodedata[x][y + 1]
        return nodedata


    def start_end_index(self, state):
        x = 0
        for i in self.nodedata:
            y = 0
            for j in i:
                if (j.value == state):
                    return x, y
                y += 1
            x += 1

    def DFS(self):
        visited = list()
        start = self.start_end_index("S")   # get start node
        stack = list()
        stack.append(self.nodedata[start[0]][start[1]])     # add start node to stack
        visited.append(self.nodedata[start[0]][start[1]])   # make start node visited
        while stack:
            current = stack[0]
            stack.remove(stack[0])               # remove top of stack add store it in current to add child
            self.fullPath.append(current.id)     # add this node to full path list
            # check if this node is the target node if true get the path and break
            if current.value == 'E':
                while current != None:
                    self.path.append(current.id)
                    current = current.previousNode
                self.path.reverse()
                break
            #########################################
            # push in stack valid child and make them visited and set previousNode value in each node
            # the child is valid if != '#' and not visited before
            if self.vaild(current.right, visited):
                stack.insert(0, current.right)
                visited.append(current.right)
                n = current.right
                n.previousNode = current
                current.right = n
            if self.vaild(current.left, visited):
                stack.insert(0, current.left)
                visited.append(current.left)
                n = current.left
                n.previousNode = current
                current.left = n
            if self.vaild(current.down, visited):
                stack.insert(0, current.down)
                visited.append(current.down)
                n = current.down
                n.previousNode = current
                current.down = n
            if self.vaild(current.up, visited):
                stack.insert(0, current.up)
                visited.append(current.up)
                n = current.up
                n.previousNode = current
                current.up = n

        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        return self.path, self.fullPath

    @property
    def BFS(self):
        self.fullPath.clear()    # clear full path list from full path of DFS
        self.path.clear()        # clear path of DFS
        visited = list()
        start = self.start_end_index("S")    # get start node
        queue = collections.deque([self.nodedata[start[0]][start[1]]])     # push start node in queue
        visited.append(self.nodedata[start[0]][start[1]])                  # make start node visited
        # while queue is not empty && the front node != target node
        # remove the front node and push the valid child in the queue
        # valid child != '#' and not visited before
        # if the child is valid make it visited and Push it to my queue and set previousNode value
        # if the front node is the target node get the path from this node to the start node and reverse it
        while queue:
            current = queue.popleft()
            self.fullPath.append(current.id)
            if current.value == 'E':
                while current != None:
                    self.path.append(current.id)
                    current = current.previousNode
                break
            if self.vaild(current.up, visited):
                visited.append(current.up)
                queue.append(current.up)
                n = current.up
                n.previousNode = current
                current.up = n
            if self.vaild(current.down, visited):  # Down
                visited.append(current.down)
                queue.append(current.down)
                n = current.down
                n.previousNode = current
                current.down = n
            if self.vaild(current.left, visited):
                visited.append(current.left)
                queue.append(current.left)
                n = current.left
                n.previousNode = current
                current.left = n
            if self.vaild(current.right, visited):
                visited.append(current.right)
                queue.append(current.right)
                n = current.right
                n.previousNode = current
                current.right = n

        self.path.reverse()

        return self.path, self.fullPath


    def updateCost(self, n1, n2):
        n2.gOfN = n1.gOfN + n2.edgeCost
        n2.previousNode = n1
        return n2

    def vaild(self,node,visited):
        if (node != None and node not in visited  and node.value != "#"  ):
            return True
        return False


    def UCS(self):
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath = []


        start = self.start_end_index("S")
        notvisited = []
        visited = []
        notvisited.append(self.nodedata[start[0]][start[1]])
        while notvisited.__len__!=0:
            notvisited.sort( key=lambda node: node.gOfN , reverse=True)
            node = notvisited.pop()
            visited.append(node)

            if self.vaild(node.up,visited):
                node.up = self.updateCost(node, node.up)
                notvisited.append(node.up)
            if self.vaild(node.down, visited):
                node.down = self.updateCost(node, node.down)
                notvisited.append(node.down)
            if self.vaild(node.right, visited):
                node.right = self.updateCost(node, node.right)
                notvisited.append(node.right)
            if self.vaild(node.left, visited):
                node.left = self.updateCost(node, node.left)
                notvisited.append(node.left)

            if node.value == "E":
                break
        end = self.start_end_index("E")
        self. path = []
        n = self.nodedata[end[0]][end[1]]
        self.path.append(n.id)
        while n.previousNode!=None:
            self.path.append(n.previousNode.id)
            n = n.previousNode
        self.path.reverse()
        self.totalCost = self.nodedata[end[0]][end[1]].gOfN
        for n in visited:
            self.fullPath.append(n.id)

        return self.path, self.fullPath, self.totalCost


    def AStarEuclideanHeuristic(self):
        # Cost for a step is calculated based on edge cost of node
        # and use Euclidean Heuristic for evaluating the heuristic value
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath = []

        start = self.start_end_index("S")
        notvisited = []
        visited = []
        notvisited.append(self.nodedata[start[0]][start[1]])
        while notvisited.__len__ != 0:
            notvisited.sort(key=lambda node: node.heuristicFn, reverse=True)
            node = notvisited.pop()
            visited.append(node)

            if self.vaild(node.up, visited):
                node.up = self.updateCost_heuristic(node, node.up)
                notvisited.append(node.up)
            if self.vaild(node.down, visited):
                node.down = self.updateCost_heuristic(node, node.down)
                notvisited.append(node.down)
            if self.vaild(node.right, visited):
                node.right = self.updateCost_heuristic(node, node.right)
                notvisited.append(node.right)
            if self.vaild(node.left, visited):
                node.left = self.updateCost_heuristic(node, node.left)
                notvisited.append(node.left)

            if node.value == "E":
                break
        end = self.start_end_index("E")
        self.path = []
        n = self.nodedata[end[0]][end[1]]
        self.path.append(n.id)
        while n.previousNode != None:
            self.path.append(n.previousNode.id)
            n = n.previousNode
        self.path.reverse()
        self.totalCost = self.nodedata[end[0]][end[1]].gOfN
        for n in visited:
            self.fullPath.append(n.id)

        return self.path, self.fullPath, self.totalCost



    def updateCost_heuristic(self,n1,n2):
       n2.previousNode=n1
       n2.gOfN =  n2.edgeCost+n1.gOfN
       Ex, Ey = self.start_end_index("E")
       x1 = 0;
       for i in self.nodedata:
           y1 = 0
           for j in i:
               if (j.id == n2.id):
                   break
               y1 += 1
           x1 += 1
       n2.hOfN = pow((pow((Ex - x1),2) + (pow((Ey - y1),2))),0.5)
       n2.heuristicFn = n2.gOfN + n2.hOfN
       return n2

    def AStarManhattanHeuristic(self):
        # Cost for a step is calculated based on edge cost of node
        # and use Euclidean Heuristic for evaluating the heuristic value
        # Fill the correct path in self.path
        # self.fullPath should contain the order of visited nodes
        self.fullPath = []
        start = self.start_end_index("S")
        notvisited = []
        visited = []
        notvisited.append(self.nodedata[start[0]][start[1]])
        while notvisited.__len__ != 0:
            notvisited.sort(key=lambda node : node.heuristicFn, reverse=True)
            node = notvisited.pop()
            if visited.count(node) == 0:
                visited.append(node)
            if self.vaild(node.up, visited):
                node.up = self.updateabsheuristic(node, node.up)
                notvisited.append(node.up)

            if self.vaild(node.down, visited):
                node.down = self.updateabsheuristic(node, node.down)
                notvisited.append(node.down)

            if self.vaild(node.left, visited):
                node.left = self.updateabsheuristic(node, node.left)
                notvisited.append(node.left)

            if self.vaild(node.right, visited):
                node.right = self.updateabsheuristic(node, node.right)
                notvisited.append(node.right)

            if node.value == "E":
                break
        end = self.start_end_index("E")
        self.path = []
        n = self.nodedata[end[0]][end[1]]
        self.path.append(n.id)
        while n.previousNode != None:
            self.path.append(n.previousNode.id)
            n = n.previousNode
        self.path.reverse()
        self.totalCost = self.nodedata[end[0]][end[1]].gOfN
        for n in visited:
            self.fullPath.append(n.id)

        return self.path, self.fullPath, self.totalCost
    def updateabsheuristic(self,n1,n2):
       n2.previousNode = n1
       n2.gOfN =  n2.edgeCost+n1.gOfN
       x1 = 0
       for i in self.nodedata:
           y1=0
           for j in i:
               if (j.id == n2.id):
                   break
               y1 += 1
           x1 += 1
       end = self.start_end_index("E")
       n2.hOfN = ( abs(end[0] - x1) + abs(end[1] - y1))
       n2.heuristicFn = n2.gOfN + n2.hOfN
      # n2.heuristicFn 😞 abs(Ex - x1) + abs(Ey - y1))
       return n2

def main():
    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.DFS()
    print('**DFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')

    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath = searchAlgo.BFS
    print('**BFS**\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\n\n')
    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                                  [0, 15, 2, 100, 60, 35, 30, 3
                                      , 100, 2, 15, 60, 100, 30, 2
                                      , 100, 2, 2, 2, 40, 30, 2, 2
                                      , 100, 100, 3, 15, 30, 100, 2
                                      , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.UCS()
    print('** UCS **\nPath is: ' + str(path) + '\nFull Path is: ' + str(fullPath) + '\nTotal Cost: ' + str(
        TotalCost) + '\n\n')
    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.',
                                  [0, 15, 2, 100, 60, 35, 30, 3
                                      , 100, 2, 15, 60, 100, 30, 2
                                      , 100, 2, 2, 2, 40, 30, 2, 2
                                      , 100, 100, 3, 15, 30, 100, 2
                                      , 100, 0, 2, 100, 30])
    path, fullPath, TotalCost = searchAlgo.AStarEuclideanHeuristic()
    print('**ASTAR with Euclidean Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')

    #######################################################################################

    searchAlgo = SearchAlgorithms('S,.,.,#,.,.,. .,#,.,.,.,#,. .,#,.,.,.,.,. .,.,#,#,.,.,. #,.,#,E,.,#,.')
    path, fullPath, TotalCost = searchAlgo.AStarManhattanHeuristic()
    print('**ASTAR with Manhattan Heuristic **\nPath is: ' + str(path) + '\nFull Path is: ' + str(
        fullPath) + '\nTotal Cost: ' + str(TotalCost) + '\n\n')


main()