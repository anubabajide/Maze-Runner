import random

##Node class
class Node:
    def __init__(self):
        self.parentNode = None
        self.tested = False
        self.rightChild = None
        self.leftChild = None
        self.middleChild = None
        self.direction = [0,0]
    def addRightChild(self):
        self.rightChild = Node()
    def addLeftChild(self):
        self.leftChild = Node()
    def addMiddleChild(self):
        self.middleChild = Node()
##-------------------------------------------
class MazeRunnerTree:
##    constructor
    def __init__(self):
        self.currentNode = Node()
##-------------------------------------------
def turnRight():
    print("i turned right");
def turnLeft():
    print("i turned left");
def setDirection(path):
    if tree.currentNode.rightChild == path:
        tree.currentNode.direction = [0,1]
    elif tree.currentNode.leftChild == path:
        tree.currentNode.direction = [1,0]
def resetDirection():
    if tree.currentNode.direction == [0,1]:
        turnLeft()
    elif tree.currentNode.direction == [1,0]:
        turnRight()
    tree.currentNode.direction == [0,0]
    
tree = MazeRunnerTree()
start = 0
temp = None
goingBackwards = False

##while moving
while(True):
##    sensors that turn on when there is an opening "0" for off and "1" for on
    
    rightSensor = random.randrange(0,2)
    leftSensor = random.randrange(0,2)
    middleSensor = random.randrange(0,2)

    availablePath = []
##run this block if it went backwards and already know the openings
    if (rightSensor == 1 or leftSensor == 1 or middleSensor == 0):
        
        if (goingBackwards):
            resetDirection()
            if(tree.currentNode.rightChild):
                if(tree.currentNode.rightChild.tested == False):
                    availablePath.append(tree.currentNode.rightChild)
            if(tree.currentNode.leftChild):
                if(tree.currentNode.leftChild.tested == False):
                    availablePath.append(tree.currentNode.leftChild)
            if(tree.currentNode.middleChild):
                if(tree.currentNode.middleChild.tested == False):
                    availablePath.append(tree.currentNode.middleChild)
                    
    ##------------------------------------------------------------------------                                     
    ##    else create node if sensor sees an opening
        if(goingBackwards == False):
            if(rightSensor == 1):
                tree.currentNode.addRightChild()
                availablePath.append(tree.currentNode.rightChild)
            if(leftSensor == 1):
                tree.currentNode.addLeftChild()
                availablePath.append(tree.currentNode.leftChild)
            if(middleSensor == 1):
                tree.currentNode.addMiddleChild()
                availablePath.append(tree.currentNode.middleChild)
    ##------------------------------------------------------------------------
            
    ##    if there is a path to take, take it and update tested to true
        if(len(availablePath) != 0):
            print("these are the available paths {} ".format(availablePath))
            setDirection(availablePath[0])
            temp = tree.currentNode
            tree.currentNode = availablePath[0]
            goingBackwards = False
            
            if(start == 0):
                tree.currentNode.parentNode = None
            else:
                tree.currentNode.parentNode = temp
                print("this is the node i entered {} \n".format(tree.currentNode))
               
##                print(tree.currentNode.parentNode)
                tree.currentNode.tested = True
            start += 1
    ##------------------------------------------------------------------------                                
    ##    else move back to parent node and update available path with nodes whose tested is false 
        else:
            print("i went back")
            tree.currentNode = tree.currentNode.parentNode
            goingBackwards = True
    ##------------------------------------------------------------------------
    else:
        continue
##conditions for making decisions
    
            
        
        
    
    
