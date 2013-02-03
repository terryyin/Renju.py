import unittest
from Renju import *

class StoneBuilder:
    dirs = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
    def __init__(self):
        self.origin = (0, 0)
        self.stones = []
        self.currentIndex = 0
        
    def From(self, position):
        self.origin = position
        return self
    
    def stone(self, who):
        self.who = who
        return self
    
    def toEast(self):
        self.dx = 1
        self.dy = 0
        return self
    
    def toWest(self):
        self.dx = -1
        self.dy = 0
        return self
    
    def to(self, directionIndex):
        self.dx = self.dirs[directionIndex][0]
        self.dy = self.dirs[directionIndex][1]
        return self
    
    def skip(self, n):
        self.currentIndex += n
        return self
    
    def count(self, n):
        for i in range(self.currentIndex, self.currentIndex + n):
            self.stones.append((self.who, (self.origin[0] + self.dx * i, self.origin[1] + self.dy * i)))
        self.currentIndex += n
        return self
    
    def get(self):
        stones = self.stones
        self.stones = []
        return stones

class TestAIPlayer(unittest.TestCase):

    def setUp(self):
        self.player = AIRenjuPlayer(white)
        self.stoneBuilder = StoneBuilder()

    def testNewMoveWillTakeEmptyPlace(self):
        game = RenjuGame(2).place(black, (0, 0)).place(black, (0, 1)).place(black, (1, 0))
        move = self.player.getMyMove(game)
        self.assertEquals((1, 1), move)
        
    def testNewMoveWillTakeEmptyPlace2(self):
        game = RenjuGame(2).place(black, (0, 0)).place(black, (0, 1)).place(black, (1, 1))
        move = self.player.getMyMove(game)
        self.assertEquals((1, 0), move)

    def testAIPlayerWantsToWin(self):
        game = RenjuGame(5)
        stones = self.stoneBuilder.stone(white).From((0, 0)).toEast().count(4).get();
        game.places(stones)
        move = self.player.getMyMove(game)
        expectedPlace = self.stoneBuilder.count(1).get()[0][1]
        self.assertEquals(expectedPlace, move)

    def testAIPlayerDoesNotWantOtherToWin(self):
        game = RenjuGame(5)
        stones = self.stoneBuilder.stone(black).From((0, 0)).toEast().count(4).get();
        game.places(stones)
        move = self.player.getMyMove(game)
        expectedPlace = self.stoneBuilder.count(1).get()[0][1]
        self.assertEquals(expectedPlace, move)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
