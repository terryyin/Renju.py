import unittest
from Renju.AIRenjuPlayer import AIBoard, stonePatterns, blackCopyOfPattern
from StoneBuilder import parseStonePatternString

Urgent = 380
class AIBoardTest(unittest.TestCase):

    def boardWithStones(self, stoneString):
        aiBoard = AIBoard(15, stonePatterns, blackCopyOfPattern(stonePatterns))
        stones, expects = parseStonePatternString(stoneString)
        aiBoard.placeStones(stones)
        return aiBoard
    def testName(self):
        stoneString = '''     0123456789
                             |
                             |
                             |     OO?
                             |       O
                             |       O
                             |
                             |
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertGreater(aiBoard.crosses[(7,2)].rank_[0], aiBoard.crosses[(6,3)].rank_[0])
        
    def testTwo3IsTheSameAs3OpenOnBothEnd(self):
        stoneString = '''     0123456789
                             |
                             |
                             |   $XXX?
                             |       X
                             |       X
                             |       X
                             |       $
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertEqual(Urgent, aiBoard.crosses[(7,2)].rank_[0])

    def testTwo3IsTheSameAs3OpenOnBothEnd2(self):
        stoneString = '''     0123456789
                             |
                             |
                             |  $XXX ?
                             |       X
                             |       X
                             |       X
                             |       $
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertEqual(Urgent, aiBoard.crosses[(7,2)].rank_[0])

    def testTwo3IsTheSameAs3OpenOnBothEnd3(self):
        stoneString = '''     0123456789
                             |
                             |
                             |    $XX?X
                             |       X
                             |       X
                             |       X
                             |       $
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertEqual(Urgent, aiBoard.crosses[(7,2)].rank_[0])

    def testTwo3IsTheSameAs3OpenOnBothEnd4(self):
        stoneString = '''     0123456789
                             |
                             |
                             |    $XX? X
                             |       X
                             |       X
                             |       X
                             |       $
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertEqual(Urgent, aiBoard.crosses[(7,2)].rank_[0])

    def testTwo3IsTheSameAs3OpenOnBothEnd5(self):
        stoneString = '''     0123456789
                             |
                             |
                             |     $X?XX
                             |       X
                             |       X
                             |       X
                             |       $
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertEqual(Urgent, aiBoard.crosses[(7,2)].rank_[0])

    def testTwo3IsTheSameAs3OpenOnBothEnd6(self):
        stoneString = '''     0123456789
                             |
                             |
                             |     $X?X X
                             |       X
                             |       X
                             |       X
                             |       $
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertEqual(Urgent, aiBoard.crosses[(7,2)].rank_[0])

    def testTwo3IsTheSameAs3OpenOnBothEnd7(self):
        stoneString = '''     0123456789
                             | X
                             | X
                             | X
                             |X?_XX
                        '''
        aiBoard = self.boardWithStones(stoneString)
        self.assertEqual(Urgent, aiBoard.crosses[(1,3)].rank_[0])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()