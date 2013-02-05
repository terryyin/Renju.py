from itertools import product

from RenjuGame import black, white, empty

class Move:
    def __init__(self, pos):
        self.pos = pos
        self.rank_ = 0
    
    def getPosition(self):
        return self.pos
    
    def rank(self, number):
        self.rank_ = number
    
    def __cmp__(self, other):
        return self.rank_ - other.rank_

now = 8
toAI = {black:'*', white:'@', empty:'_', now:'|', 'wall':'W'}
class AIBoard:
    dirs = ((-1, 0), (0, -1), (-1, -1), (1, -1), (1, 0), (0, 1), (1, 1), (-1, 1))
    
    def __init__(self, board):
        self.size = board.groundSize
        self.board = board
        self.rows = []
        
    def getSlice(self, move):
        for start in range(-2, 1):
            for (dx, dy) in self.dirs:
                for length in range(5, 8):
                    s = [self.getStone_((move[0] + i * dx, move[1] + i * dy)) for i in range(start, start + length)]
                    s[-start] = '|'
                    yield ''.join(s)
    def getStone_(self, pos):
        if pos[0]<0 or pos[0] >= self.size or pos[1] < 0 or pos[1] > self.size:
            return '|'
        return toAI[self.board.stones.get(pos, empty)]

MIN_RANK = 1  
LOSS = 100
stonePatterns = {
            '_*|___': MIN_RANK, 
            '__|*__': MIN_RANK * 2, 
            '_@|___': MIN_RANK * 3, 
            '__|@__': MIN_RANK * 4, 
            
            '_|**__': MIN_RANK * 5, 
            '_*|*__': MIN_RANK * 5, 
            '_|@@__': MIN_RANK * 6, 
            '_@|@__': MIN_RANK * 6, 

            '_|***_': LOSS - 15, 
            '_*|**_': LOSS - 15, 
            '_|@@@_': LOSS - 10, 
            '_@|@@_': LOSS - 10, 
            '*|***': LOSS,
            '**|**': LOSS,
            '|****': LOSS,
            '@|@@@': LOSS + 10,
            '@@|@@': LOSS + 10,
            '|@@@@': LOSS + 10,
            }

def blackCopyOfPattern(pattern):
    op = {}
    for key, v in pattern.viewitems():
        op[key.replace('*', '#').replace('@', '*').replace('#', '@')] = v
    return op

class AIRenjuPlayer(object):
    
    def __init__(self, who, patternsForWhite = stonePatterns):
        self.who = who
        if who == white:
            self.patterns = patternsForWhite
        else:
            self.patterns = blackCopyOfPattern(patternsForWhite)
        
    def getMyMove(self, board):
        self.board = board
        self.aiBoard = AIBoard(board)
        def evaluateMove(move, self=self):
            return self._evaluateMove(move)
        return max(map(evaluateMove, self._possibleMoves(board))).getPosition()
    
    def _evaluateMove(self, move):
        m = Move(move)
        for aslice in self.aiBoard.getSlice(move):
            m.rank(self.patterns.get(aslice, m.rank_))
        return m
    
    def _possibleMoves(self, board):
        for pos in product(range(board.groundSize), repeat=2):
            if pos not in board.stones:
                yield pos
    
