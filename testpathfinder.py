# Public tests for project 5
import unittest, os, json
from pathfinder import *
from gameboard  import *
from players    import *
from map        import *

# Various maps / levels
# These are all 20x20
level1 = "maps/level1.map"
level2 = "maps/level2.map"
level3 = "maps/level3.map"

class TestPathFinder(unittest.TestCase):
    # Setup code for the tests. Do not modify this
    # x / y    -- Starting coordinates
    # endX/Y   -- Ending coordinates (where the nut is)
    # mapfile  -- Map file to use (e.g., level1, level2, level3)
    def setup(self,x,y,endX,endY,width,height,mapfile):
        f = open(os.path.join("./config.json"))
        jsonData = f.read()
        f.close()
        self.cfg = json.loads(jsonData)
        self.height = height
        self.width = width
        self.tileSize = self.cfg["tileSize"]
        self.observers = []
        self.tickObservers = []
        self.tileFactory = TileFactory(self.cfg)
        #pygame.init()
        self.board = GameBoard(self.cfg, width, height)
        self.mainCharacter = Squirrel((x,y), self.board)
        self.board.addTile(self.mainCharacter)
        self.endX = endX
        self.endY = endY
        self.endTile = Exit((endX,endY), self.board)
        self.board.addTile(self.endTile)
        levelMap = Map(self.tileFactory, mapfile, width, height)
        levelMap.loadMap()
        levelMap.loadToBoard(self.board)
        self.pathfinder = PathFinder(self.board, self.mainCharacter)
        return self.pathfinder

    # Tests for `canMoveTo`
    def test_canMoveTo(self):
        self.setup(1,1,5,5,20,20,level1)
        self.assertEqual(self.pathfinder.canMoveTo(1,2), True)
        self.assertEqual(self.pathfinder.canMoveTo(1,3), True)
        self.assertEqual(self.pathfinder.canMoveTo(3,19), False)
        self.assertEqual(self.pathfinder.canMoveTo(4,19), True)
        self.assertEqual(self.pathfinder.canMoveTo(4,20), False)
        self.assertEqual(self.pathfinder.canMoveTo(4,20), False)

    # Tests for `checkValidPath`
    def test_checkValidPath(self):
        self.setup(1,1,5,5,20,20,level1)
        path1 = [(1, 13), (1, 0), (1, 0), (1, 0), (1, 0)
                 ,(0, -1), (0, -1), (0, -1), (0, -1)
                 , (0, -1), (0, -1), (0, -1), (0, -1)]
        path2 = [(1, 13), (-1, 0), (-1, 0)]
        self.assertEqual(self.pathfinder.checkValidPath(path1), True)
        self.assertEqual(self.pathfinder.checkValidPath(path2), False)

    # Tests for `checkValidPath`
    def test_checkValidPath(self):
        self.setup(1,1,5,5,20,20,level1)
        path1 = [(1, 13), (1, 0), (1, 0), (1, 0), (1, 0)
                 ,(0, -1), (0, -1), (0, -1), (0, -1)
                 , (0, -1), (0, -1), (0, -1), (0, -1)]
        path2 = [(1, 13), (-1, 0), (-1, 0)]
        self.assertEqual(self.pathfinder.checkValidPath(path1), True)
        self.assertEqual(self.pathfinder.checkValidPath(path2), False)

    def test_canSolve(self):
        self.setup(19,1,5,5,20,20,level3)
        self.assertEqual(self.pathfinder.canSolve((5,5)), False)
        self.setup(1,1,5,5,20,20,level3)
        self.assertEqual(self.pathfinder.canSolve((5,5)), True)

    def test_findPath(self):
        self.setup(19,1,5,5,20,20,level3)
        self.assertEqual(self.pathfinder.canSolve((5,5)), False)
        self.setup(1,1,5,5,20,20,level3)
        # Note that I will use my own implementation of
        # `checkValidPath` for the actual (secret) tests
        self.assertEqual(self.pathfinder.checkValidPath(self.pathfinder.findPath((5,5))), True)

unittest.main()
