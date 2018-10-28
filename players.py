# Tiles, Players, and NPCs
import pygame, sys, os, json
from pygame.locals import *

# The priorities of various elements
class Priority:
    background = 4
    player     = 2
    item       = 3
    arrow      = 1
    wall       = 1

# An exception that gets thrown when a player executes an
# invalid move.
class InvalidMoveException(Exception):
    pass

# The representation of a single tile on the game board
class Tile:
    def __init__(self, tileType):
        # The (x,y) position on the board
        self.xPosition = None
        self.yPosition = None

        # The priority of the tile, lower is higher priority
        self.priority  = Priority.background
        
        # The set of observers on this tile
        self.observers = []

        # The type of this tile
        self.tileType  = tileType

        # The image to render the tile
        self.image     = None
        
        # The set of observers watching for when this tile is collided with
        self.collisionObservers = []

    def getX(self): return self.xPosition
    def getY(self): return self.yPosition
    def getPriority(self): return self.priority
    def setPriority(self, n):
        self.priority = n
        self.fireObservers()

    # Register for collision events
    def registerCollisionObserver(self,o):
        self.collisionObservers.append(o)

    def fireCollision(self,collidedTile):
        for observer in self.collisionObservers:
            observer.handleCollisionWith(collidedTile)

    # Get a copy of this object. All object parameters are copied
    # deeply, but image object is reused.
    def clone(self):
        t = Tile(self.tileType)
        t.xPosition = self.xPosition
        t.priority  = self.priority
        # Should observers be copied..?
        t.observers = self.observers
        t.tileType  = self.tileType
        t.image     = self.image
        return t

    # Set and load the image file for this tile, also firing the
    # observers to update the game board based on this
    def setImage(self,filename):
        try:
            self.image = pygame.image.load(os.path.join(filename))
        except:
            print("Cannot load tile image file {}".format(filename))
            exit(1)
        
        # Now fire observers
        for observer in self.observers:
            observer.handleMove(x, y, x, y)
        return

    # Fire all the observers for this tile
    def fireObservers(self):
        for observer in self.observers:
            observer.handleMove(self, fromX, fromY, x, y)
        return

    # Set the position of the tile, firing all observers
    def setPosition(self,x,y):
        fromX = self.xPosition
        fromY = self.yPosition
        self.xPosition = x
        self.yPosition = y
        for observer in self.observers:
            observer.handleMove(self, fromX, fromY, x, y)
        return

    def registerMoveObserver(self,o):
        self.observers.append(o)
    
    # Get the image for this tile, returns None unless `setImageFile`
    # has been called
    def getImage(self):
        assert(self.image != None)
        return self.image

    # Handle a collision with another tile
    def handleCollisionWith(self, otherTile):
        pass

# A tile factory that returns new tiles based on the character given
class TileFactory:
    def __init__(self,cfg):
        self.tiles = {}
        
        for tileData in cfg["tiles"]:
            tile = Tile(tileData["type"])
            tile.setImage(tileData["filename"])
            tile.setPriority(tileData["priority"])
            tile.id = tileData["id"]
            self.tiles[tileData["mapCharacter"]] = tile
        return

    # Create a fresh new tile from the character with the specified
    # coordinate
    def fromChar(self,character,x,y):
        tile = self.tiles[character].clone()
        tile.setPosition(x,y)
        return tile

# Abstract Player class representing all of the common properties
# shared by a character
class Player(Tile):
    def __init__(self, coordinate, board):
        super(Player, self).__init__("player")
        self.setPosition(coordinate[0], coordinate[1])
        self.board = board
        self.hp = 100
    
    # Attempt to move the player (+x, +y) units, where x is in the
    # range {-1, 0, 1} and y is in the range {-1, 0, 1}. For example,
    # `move(1,0)` would move the character one tile to the right.
    def move(self, x, y):
        tx = self.xPosition + x
        ty = self.yPosition + y
        # Check to ensure we can move there
        if (x < -1 or x > 1 or y < -1 or y > 1):
            # x and y must be in [-1,1]
            raise InvalidMoveException()
        if (tx >= 0 and tx < self.board.width
            and ty >= 0 and ty < self.board.height
            and
            (not self.board.higherPriorityObjectAt(self,tx,ty))):
            # Actually set the position
            self.setPosition(self.xPosition + x, self.yPosition + y)
        else:
            # Either outside of the boundaries of the board or a wall
            # is there
            raise InvalidMoveException()
        
        # Once we've performed the move, we need to update the player
        # statistics. Specifically, we:
        #   - Subtract one fuel
        self.board.state.decrementFuel(1)

# The "exit" tile in the game (i.e., when you get here you win).
class Exit(Player):
    def __init__(self, coordinate, board):
        super(Exit, self).__init__(coordinate, board)
        self.setImage("imgs/nuts.png")
        self.priority = Priority.item

    # If we collide with this tile, the player wins the game!
    def handleCollisionWith(self, other):
        self.board.state.setWon()

# The main player in the game (i.e., the squirrel)
class Squirrel(Player):
    def __init__(self, coordinate, board):
        super(Squirrel, self).__init__(coordinate, board)
        self.nuts = 0
        self.pic = pygame.image.load(os.path.join("imgs/squirrelright.png"))
        self.priority = Priority.player

    # Handle events from the toplevel
    def handleEvent(self,event):
        if event.type == pygame.KEYDOWN:
            try:
                if event.key == pygame.K_LEFT:
                    self.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move(1, 0)
                elif event.key == pygame.K_UP:
                    self.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.move(0, +1)
                elif event.key == pygame.K_SPACE:
                    return
            except InvalidMoveException:
                # They tried to go somewhere they couldn't, do
                # nothing.
                return
                


    def getImage(self):
        return self.pic
