import unittest
from sampleData import *
from graphs import *

sgraph1 = ([6,1,2,3,4,5], [(1,2), (3,4), (6,3), (5, 3), (4,5), (6,4), (2,3)])
sgraph2 = ([6,1,2,3,4,5], [(1,2), (2,3), (3,4), (3,5), (5,6), (4,6)])
sgraph3 = ([6,1,2,3,4,5,7,8], [(1,2), (2,3), (4,5), (4,6), (7,8)])
sgraph4 = ([6,1,2,3,4,5,7,8], [(1,2), (2,3), (2,3), (4,5), (4,6), (7,8)])

coloring1 = [[1, "red"], [2, "red"], [3, "red"], [4,"red"], [5, "red"], [6,"red"]]
coloring2 = [[1, "red"], [2, "blue"], [3, "red"], [4,"blue"], [5, "green"], [6,"yellow"]]
coloring3 = [[1, "red"], [2, "blue"], [3, "red"], [4,"blue"], [5, "blue"], [6,"red"]]
coloring4 = [[1, "red"], [2, "blue"], [3, "red"], [4,"blue"], [5, "blue"], [6,"blue"]]

class TestP3(unittest.TestCase):
    def test_isValidColoringA(self):
        self.assertEqual(isValidColoring(sgraph1, coloring1), False)

    def test_isValidColoringB(self):
        self.assertEqual(isValidColoring(sgraph1, coloring2), True)

    def test_isValidColoringC(self):
        self.assertEqual(isValidColoring(sgraph2, coloring3), True)

    def test_isValidColoringD(self):
        self.assertEqual(isValidColoring(sgraph2, coloring4), False)

    def test_setEquals(self):
        self.assertEqual(setEquals([1], [1]), True)
        self.assertEqual(setEquals([], []), True)
        self.assertEqual(setEquals([2], [2]), True)
    
    def test_setEqualsSecretA(self):
        self.assertEqual(setEquals([1], [2]), False)
        self.assertEqual(setEquals([2], []), False)
        self.assertEqual(setEquals([], [2]), False)

    def test_setEqualsSecretC(self):
        self.assertEqual(setEquals([3,5,8,1,4], [4,3,5,8,1]), True)
        self.assertEqual(setEquals([8,3,4,2], [3,4,2]), False)
        self.assertEqual(setEquals([3,4,2], [8,3,4,2]), False)

    def test_calculateNextSet(self):
        self.assertEqual(setEquals(calculateNextSet(graph1, [1], []), [1,2]), True)

    def test_calculateNextSetSecA(self):
        x = calculateNextSet(graph1, [3,1], [2])
        y = [2,4,6,5]
        x.sort()
        y.sort()
        self.assertEqual(x,y)

    def test_calculateNextSetSecB(self):
        x = calculateNextSet(graph2, [6,3], [])
        y = [2,4,5]
        x.sort()
        self.assertEqual(x,y)

    def test_extraCreditA(self):
        self.assertEqual(calculateBipartite(graph3), True)
        self.assertEqual(calculateBipartite(graph4), False)

unittest.main()
