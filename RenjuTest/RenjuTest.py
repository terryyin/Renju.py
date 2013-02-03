from Renju import *
from AIRenjuTest import StoneBuilder
import unittest


class TestRenjuGame(unittest.TestCase):

    def setUp(self):
        self.game = RenjuGame()
        self.stoneBuilder = StoneBuilder()

    def test5StonesWin(self):
        stones = self.stoneBuilder.stone(white).From((0, 0)).toEast().count(4).get();
        self.game.places(stones)
        expectedPlace = self.stoneBuilder.count(1).get()[0][1]
        self.assertTrue(self.game.willWinWith(expectedPlace, white))
        
    def test4DoesNot(self):
        stones = self.stoneBuilder.stone(white).From((0, 0)).toEast().count(3).get();
        self.game.places(stones)
        expectedPlace = self.stoneBuilder.count(1).get()[0][1]
        self.assertFalse(self.game.willWinWith(expectedPlace, white))
        
    def testFalseWinningWithOthersStone(self):
        stones = self.stoneBuilder.From((0, 0)).toEast().stone(white).count(3).stone(black).count(1).get();
        self.game.places(stones)
        expectedPlace = self.stoneBuilder.count(1).get()[0][1]
        self.assertFalse(self.game.willWinWith(expectedPlace, white))
        
    def testWinningOnOtherDirection(self):
        def checkWinningOnDirection(directionIndex, self=self):
            stoneBuilder = StoneBuilder()
            game = RenjuGame(11)
            stones = stoneBuilder.From((5, 5)).to(directionIndex).stone(black).count(1).stone(white).count(4).get()
            game.places(stones)
            expectedPlace = stoneBuilder.count(1).get()[0][1]
            self.assertTrue(game.willWinWith(expectedPlace, white))
        map(checkWinningOnDirection, range(8))

    def testWinningInTheMiddle(self):
        stones = self.stoneBuilder.stone(black).From((0, 0)).toEast().count(3).skip(1).count(1).get();
        self.game.places(stones)
        expectedPlace = (3, 0)
        self.assertTrue(self.game.willWinWith(expectedPlace, black))


if __name__ == "__main__":
    unittest.main()