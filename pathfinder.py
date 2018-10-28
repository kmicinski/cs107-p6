from dllist import *

# A path finder object isolates the logic to perform a path-finding
# problem on:
# 
#   - An underlying `board` object.
# 
#   - A `player` object, which holds the player's current position and
#   other relevant information about the player.
class PathFinder:
    def __init__(self, board, player):
        # The underlying game board on which tiles live
        self.board   = board
        
        # The underlying player object
        self.player  = player

        # The starting coordinates
        self.startX  = player.getX()
        self.startY  = player.getY()
        
        # The width / height of the board
        self.width   = self.board.width
        self.height  = self.board.height

        # A two-dimensional array to store whether or not the tile has
        # been visited.
        self.visited = [[False for x in range(board.width)]
                        for y in range(board.height)]

        # XXX
        self.winning = False

    # Check whether `path` is a valid path
    def checkValidPath(self,path):
        return False

    # Check whether or not there is a wall (or other solid object) at
    # the coordinates (x,y)
    def wallAt(self,x,y):
        return self.board.higherPriorityObjectAt(self.player,x,y)
    
    # Check whether or not we can move to (x,y) I.e., is there a wall
    # there, or is it out of bounds?
    def canMoveTo(self,tx,ty):
        return False
        
    def canSolve(self, toCoordinate):
        return False

    def findPath(self, toCoordinate):
        return False
