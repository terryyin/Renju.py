import unittest
from Renju import *
from Renju.AIRenjuPlayer import WIN
from StoneBuilder import StoneBuilder, stop, parseStonePatternString, aiMaxmin

'''
"B8\\__XO_$" means:
    B: column B (column 1).
    8: row 8.
    \\: to direction south east. Other directions: -:to east |: to south /:to south west 
    _: empty
    X: black stone
    O: white stone
    $: wall. It's not a stone but something else prevent AI to match a pattern.
'''
class TestAIPlayerPattern(unittest.TestCase):
    def setUp(self):
        self.FourInARowPattern = {
            '_|****': 100,
            }

        self.ThreeInARowPattern = {
            '|***__': 60,
            }
        self.OneStonePattern = {
            '|*____': 60,
            }

    def testAIPlayerShouldGiveThePatternRank(self):
        player = AIRenjuPlayer(white,  RenjuBoard(), self.FourInARowPattern)
        player.placeStones(parseStonePatternString('A0|XXXX_')[0])
        move = player.getMyMove()
        self.assertEqual(move, stop('A0|____O'))

    def testAIPlayerShouldWorkWithBlackStoneAsWell(self):
        player = AIRenjuPlayer(black, RenjuBoard(), self.FourInARowPattern)
        player.placeStones(parseStonePatternString('A0|OOOO_')[0])
        move = player.getMyMove()
        self.assertEqual(move, stop('A0|____O'))

    def testAIPlayerShouldChooseTheMoveWithHighestRank(self):
        player = AIRenjuPlayer(white,  RenjuBoard(), dict(self.FourInARowPattern.items() + self.ThreeInARowPattern.items()))
        player.placeStones(parseStonePatternString('C0|XXXX_')[0])
        player.placeStones(parseStonePatternString('G0|_XXX_')[0])
        move = player.getMyMove()
        self.assertEqual(move, stop('C0|____O'))

class TestAIPlayer(unittest.TestCase):

    def setUp(self):
        self.player = AIRenjuPlayer(white, RenjuBoard())
        self.stoneBuilder = StoneBuilder()

    def testNewMoveShouldTakeEmptyPlace(self):
        game = RenjuBoard(2).place(black, (0, 0)).place(black, (0, 1)).place(black, (1, 0))
        self.player = AIRenjuPlayer(white, game)
        move = self.player.getMyMove()
        self.assertEquals((1, 1), move)
        
    def testNewMoveShouldTakeEmptyPlace2(self):
        game = RenjuBoard(2).place(black, (0, 0)).place(black, (0, 1)).place(black, (1, 1))
        self.player = AIRenjuPlayer(white, game)
        move = self.player.getMyMove()
        self.assertEquals((1, 0), move)

    def aiMoveForPatternShouldBeIn(self, stones, expects):
        self.player = AIRenjuPlayer(white, RenjuBoard())
        for s in stones:
            self.player.placeStones(parseStonePatternString(s)[0])
        move = self.player.getMyMove()
        self.assertIn(move, [stop(e) for e in expects])

    def aiPattern(self, stonesPattern, level = 0):
        self.player = AIRenjuPlayer(white, RenjuBoard())
        stones, expects = parseStonePatternString(stonesPattern)
        self.player.placeStones(stones)
        move = self.player.getMyMove(level)
        self.assertIn(move, expects)

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

    def testThreatingShouldHavePriority(self):
        self.aiMoveForPatternShouldBeIn(["A0-OOO___$", "A0|__OO__$"], ["A0-___O", "A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-OOO___OO"], ["A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-OOO__$__OO"], ["A0-___O", "A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-OOO__O___OO"], ["A0-___O", "A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-OOO__X___OO"], ["A0-___O", "A0-____O"])

    def testTwoStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__OO__$", "A0|__XX__$"], ["A0-_O", "A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-__O_O__$", "A0|__XX__$"], ["A0-___O"])

    def testOpposeTwoStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__XX__$", "A0|__O___$"], ["A0-_O", "A0-____O"])
        self.aiMoveForPatternShouldBeIn(["A0-_X_X__$", "A0|__O___$"], ["A0-__O"])

    def testOneStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__O___$", "A0|_O____$"], ["A0-___O"])
        self.aiMoveForPatternShouldBeIn(["A0|_O____$", "B0-__X___$"], ["A0|__O"])

    def testOpposeWithOneStoneWith6Slots(self):
        self.aiMoveForPatternShouldBeIn(["A0-__X___$", "A0|_X____$"], ["A0-___O"])
        self.aiMoveForPatternShouldBeIn(["A0|_X____$"], ["A0|__O"])

    def testWinningWithADouble3(self):
        self.aiPattern('''    0123456789
                             |
                             |
                             |     OO?
                             |       O
                             |       O
                             |
                             |
                        ''')

    def testShouldAvoidFurtherLose(self):
        self.aiPattern('''    0123456789
                             |
                             |
                             |     XX?
                             |       X
                             |       X
                             |
                             |
                        ''')

    def testTwo3IsTheSameAs3OpenOnBothEndOppose(self):
        self.aiPattern('''    0123456789
                             |
                             |
                             |   $XXX?
                             |       X
                             |       X
                             |       X
                             |       $
                        ''')

    def testTryToBlockOpposeOneStone1(self):
        self.aiPattern('''    ABCDEFGHIJKL
                             0
                             1
                             2
                             3__X?__$
                             4   ?X
                             5    
                             6 
                             7
                             8    $
                        ''')

    def testFourStoneIsHigherThanBlocking3s(self):
        self.aiPattern('''    0123456789
                             0
                             1       O
                             2        ?
                             3         O
                             4       X  O
                             5       X
                             6      XXX
                             7         
                        ''')

    def test2LevelsStopAtLosing(self):
        self.aiPattern('''    0123456789
                             0XXXX?
                             0   OOO
                        ''', 1)

    def test2LevelsStopAtWinning(self):
        self.aiPattern('''    0123456789
                             0OOOO?
                             0XXXX
                        ''', 1)

    def test2LevelsTake3inARow(self):
        self.aiPattern('''    0123456789
                             0     ?OOO?
                             0      XXX
                        ''', 1)

    def test2LevelsSave3inARow(self):
        self.aiPattern('''    0123456789
                             0     ?XXX?
                        ''', 1)

    def test3Levels(self):
        self.aiPattern('''    0123456789
                             0     ?XX?
                        ''', 2)

class TestAIPlayerMaxmin(unittest.TestCase):
    def aiMaxmin(self, stonesPattern, who, asWho, level, expectedRank):
        (rank, move), expects = aiMaxmin(stonesPattern, who, asWho, level)
        self.assertIn(move, expects)
        self.assertEqual(expectedRank, rank)
        
    def test0LevelsShouldSeeTheDirectWinning(self):
        self.aiMaxmin('''     0123456789
                             |OOOO?
                             |XXXX
                        ''', white, white, 0, WIN)

    def test0LevelsShouldSeeTheIndirectWinning(self):
        self.aiMaxmin('''     0123456789
                             |   ?OOO?
                        ''', white, white, 0, WIN)

    def test0LevelsShouldSeeTheIndirectWinningButNotFalsePositive(self):
        self.aiMaxmin('''     0123456789
                             |   OOO
                             |XXXX?
                        ''', white, white, 0, 0)

    def test0LevelTooManyLosingPoints(self):
        self.aiMaxmin('''     0123456789
                             |?XXXX?
                        ''', white, white, 0, -WIN)


    def test0LevelsShouldPostponeTheLosing(self):
        self.aiMaxmin('''     0123456789
                             |
                             |       ?OOO$
                             |     XXX
                             |       X
                             |       X
                             |       
                             |
                        ''', white, white, 0, 0)

    def test0LevelsShouldSeeTheLosing2(self):
        self.aiMaxmin('''     0123456789
                             |
                             |       ?
                             |   $XXXX?
                             |       X
                             |       X
                             |       ?
                             |
                        ''', white, white, 1, -WIN)

    def test0LevelsShouldSeeTheLosing(self):
        self.aiMaxmin('''     0123456789
                             |
                             |       ?
                             |    ?XXX?
                             |       X
                             |       X
                             |       ?
                             |
                        ''', white, white, 1, -WIN)

    def test0LevelsShouldSeeTwo3IsTheSameAs3OpenOnBothEnd(self):
        self.aiMaxmin('''     0123456789
                             |
                             |       
                             |   $OOO?
                             |       O
                             |       O
                             |       O
                             |       $
                        ''', white, white, 0, WIN)

    def testMinusLevelsShouldSeeTwo3IsTheSameAs3OpenOnBothEnd(self):
        self.aiMaxmin('''     0123456789
                             |
                             |       
                             |   $OOO?
                             |       O
                             |       O
                             |       O
                             |       $
                        ''', white, white, -.5, WIN)

    def testLosingWillExtendTheSearchLevel(self):
        self.aiMaxmin('''     0123456789
                             |     
                             |
                             |
                             |      O
                             |   O O
                             |    XOO  
                             |    OXXX?X
                             |      X
                             |     XXXO
                             |    O X O 
                             |      O
                             |
                        ''', white, white, 0, -WIN)

    def testThreatWillExtendTheThreating(self):
        self.aiMaxmin('''     0123456789
                             |     
                             |
                             |
                             |      O
                             |   O O
                             |    XOO  
                             |    OXXX??
                             |      X
                             |     XXXO
                             |    O X O 
                             |      O
                             |
                        ''', white, black, 0, WIN)

    def testThreatWillExtendTheThreating1(self):
        self.aiMaxmin('''     0123456789
                             |     
                             |
                             |       
                             |      O
                             |   O O
                             |    XOO  
                             |    OXXX 
                             |      X 
                             |     XXXO
                             |    ? X O 
                             |      O
                             |
                        ''', white, white, 1, -WIN)
        
    def testThreatWillExtendTheThreating2(self):
        self.aiMaxmin('''     0123456789
                             |     
                             |
                             |       
                             |      O
                             |   O O
                             |    XOO  
                             |    OXX? 
                             |      X ?
                             |     ?XX
                             |      X O 
                             |      O
                             |
                        ''', white, black, 4, WIN)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
