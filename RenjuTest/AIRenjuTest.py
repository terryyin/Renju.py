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
        board.places(stos('A0|XXXX_'))
        move = player.getMyMove(board)
        self.assertEqual(move, stop('A0|____O'))

    def testAIPlayerShouldWorkWithBlackStoneAsWell(self):
        player = AIRenjuPlayer(black, self.FourInARowPattern)
        board = RenjuBoard()
        board.places(stos('A0|OOOO_'))
        move = player.getMyMove(board)
        self.assertEqual(move, stop('A0|____O'))

    def testAIPlayerShouldChooseTheMoveWithHighestRank(self):
        player = AIRenjuPlayer(white, dict(self.FourInARowPattern.items() + self.ThreeInARowPattern.items()))
        board = RenjuBoard()
        board.places(stos('C0|XXXX_'))
        board.places(stos('G0|_XXX_'))
        move = player.getMyMove(board)
        self.assertEqual(move, stop('C0|____O'))



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

    def aiMoveForPatternShouldBeIn(self, stones, expects):
        board = RenjuBoard()
        for s in stones:
            board.places(stos(s))
        move = self.player.getMyMove(board)
        self.assertIn(move, [stop(e) for e in expects])

    def testAIPlayerWantsToWin(self):
        self.aiMoveForPatternShouldBeIn(["A9-OOOO_", "A3-XXXX_"], ["A9-____O"])
        self.aiMoveForPatternShouldBeIn(["A9-OOO_O", "A3-XXXX_"], ["A9-___O"])
        self.aiMoveForPatternShouldBeIn(["A9-OO_OO", "A3-XXXX_"], ["A9-__O"])

    def testAIPlayerDoesNotWantOtherToWin(self):
        self.aiMoveForPatternShouldBeIn(["A9-XXXX_", "A3-_OOO_"], ["A9-____O"])
        self.aiMoveForPatternShouldBeIn(["A9-X_XXX", "A3-_OOO_"], ["A9-_O"])
        self.aiMoveForPatternShouldBeIn(["A9-XX_XX", "A3-_OOO_"], ["A9-__O"])

    def testAIPlayerShouldForm4InARowWhenPossible(self):
        self.aiMoveForPatternShouldBeIn(["A9-_OOO__$", "A3-_XXX__$"], ["A9-____O"])
        self.aiMoveForPatternShouldBeIn(["A9-_O_OO_$", "A3-_XXX__$"], ["A9-__O"])
        self.aiMoveForPatternShouldBeIn(["A9-_OO_O_$", "A3-_XXX__$"], ["A9-___O"])

    def testAIPlayerShouldStopOppose3InARow(self):
        self.aiMoveForPatternShouldBeIn(["A9-_XXX__$"], ["A9-____O"])
        self.aiMoveForPatternShouldBeIn(["A9-_X_XX_$"], ["A9-__O"])
        self.aiMoveForPatternShouldBeIn(["A9-_XX_X_$"], ["A9-___O"])

    def testTwoStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__OO__$", "A0|__XX__$"], ["A0-_O", "A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-_O_O__$", "A0|__XX__$"], ["A0-__O"])

    def testOpposeTwoStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__XX__$", "A0|__O___$"], ["A0-_O", "A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-_X_X__$", "A0|__O___$"], ["A0-__O"])

    def testOneStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__O___$", "A0|_O____$"], ["A0-___O"])
        self.aiMoveForPatternShouldBeIn(["A0|_O____$", "B0-__X___$"], ["A0|__O"])

    def testOpposeWithOneStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__X___$", "A0|_X____$"], ["A0-___O"])
        self.aiMoveForPatternShouldBeIn(["A0|_X____$"], ["A0|__O"])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
