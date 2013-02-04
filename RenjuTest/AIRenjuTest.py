import unittest
from Renju import *
from StoneBuilder import StoneBuilder, stop, stos

class TestAIPlayerPattern(unittest.TestCase):

    def setUp(self):
        self.FourInARowPattern = {
            '|****': 100,
            }

        self.ThreeInARowPattern = {
            '|***_': 50,
            }

    def testAIPlayerShouldGiveThePatternRank(self):
        player = AIRenjuPlayer(white, self.FourInARowPattern)
        board = RenjuBoard()
        board.places(stos('XXXX_'))
        move = player.getMyMove(board)
        self.assertEqual(move, stop('____O'))

    def testAIPlayerShouldWorkWithBlackStoneAsWell(self):
        player = AIRenjuPlayer(black, self.FourInARowPattern)
        board = RenjuBoard()
        board.places(stos('OOOO_'))
        move = player.getMyMove(board)
        self.assertEqual(move, stop('____O'))

    def testAIPlayerShouldChooseTheMoveWithHighestRank(self):
        player = AIRenjuPlayer(white, dict(self.FourInARowPattern.items() + self.ThreeInARowPattern.items()))
        board = RenjuBoard()
        board.places(stos('XXXX_', 8))
        board.places(stos('_XXX_', 3))
        move = player.getMyMove(board)
        self.assertEqual(move, stop('____O', 8))



class TestAIPlayer(unittest.TestCase):

    def setUp(self):
        self.player = AIRenjuPlayer(white)
        self.stoneBuilder = StoneBuilder()
        self.board = RenjuBoard()

    def testNewMoveShouldTakeEmptyPlace(self):
        game = RenjuBoard(2).place(black, (0, 0)).place(black, (0, 1)).place(black, (1, 0))
        move = self.player.getMyMove(game)
        self.assertEquals((1, 1), move)
        
    def testNewMoveShouldTakeEmptyPlace2(self):
        game = RenjuBoard(2).place(black, (0, 0)).place(black, (0, 1)).place(black, (1, 1))
        move = self.player.getMyMove(game)
        self.assertEquals((1, 0), move)

    def aiMoveForPatternShouldBeIn(self, stones, lowRankStones, expects):
        board = RenjuBoard()
        board.places(stos(stones))
        self.board.places(stos(lowRankStones, 3))
        move = self.player.getMyMove(board)
        self.assertIn(move, [stop(e) for e in expects])

    def testAIPlayerWantsToWin(self):
        self.aiMoveForPatternShouldBeIn("OOOO_", "XXXX_", ["____O"])
        self.aiMoveForPatternShouldBeIn("OOO_O", "XXXX_", ["___O"])
        self.aiMoveForPatternShouldBeIn("OO_OO", "XXXX_", ["__O"])

    def testAIPlayerDoesNotWantOtherToWin(self):
        self.aiMoveForPatternShouldBeIn("XXXX_", "_OOO_", ["____O"])
        self.aiMoveForPatternShouldBeIn("X_XXX", "_OOO_", ["_O"])
        self.aiMoveForPatternShouldBeIn("XX_XX", "_OOO_", ["__O"])

    def testAIPlayerShouldForm4InARowWhenPossible(self):
        self.aiMoveForPatternShouldBeIn("_OOO__X", "_XXX_", ["____O"])
        self.aiMoveForPatternShouldBeIn("_O_OO_X", "_XXX_", ["__O"])
        self.aiMoveForPatternShouldBeIn("_OO_O_X", "_XXX_", ["___O"])

    def testAIPlayerShouldStopOppose3InARow(self):
        self.aiMoveForPatternShouldBeIn("_XXX__O", "", ["____O"])
        self.aiMoveForPatternShouldBeIn("_X_XX_O", "", ["__O"])
        self.aiMoveForPatternShouldBeIn("_XX_X_O", "", ["___O"])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
