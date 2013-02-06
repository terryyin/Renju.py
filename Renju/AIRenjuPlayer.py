from itertools import product

from RenjuGame import black, white, empty

MIN_RANK = 2  
URGENT = 300
LOSS = 1000
WIN = 2000
stonePatterns = {
            '_*_|__': MIN_RANK, 
            '_*|___': MIN_RANK + 1, 
            '__|*__': MIN_RANK + 2, 
            '_@|___': MIN_RANK + 3, 
            '__|@__': MIN_RANK + 4, 
            
            '_|**__': MIN_RANK + 5, 
            '_*|*__': MIN_RANK + 5, 
            '_|@@__': MIN_RANK + 6, 
            '_@|@__': MIN_RANK + 6, 

            '_|***_': URGENT - 100, 
            '_*|**_': URGENT - 100, 
            '_|@@@_': URGENT, 
            '_@|@@_': URGENT, 
            '*|****': LOSS,
            '_*|***': LOSS,
            '@*|***': LOSS,
            '*|***@': LOSS,
            '*|***_': LOSS,
            '**|***': LOSS,
            '**|**@': LOSS,
            '**|**_': LOSS,
            '@|****': LOSS,
            '_|****': LOSS,
            '|****@': LOSS,
            '|****_': LOSS,
            '@|@@@@': WIN,
            '_@|@@@': WIN,
            '*@|@@@': WIN,
            '@|@@@*': WIN,
            '@|@@@_': WIN,
            '@@|@@@': WIN,
            '@@|@@*': WIN,
            '@@|@@_': WIN,
            '*|@@@@': WIN,
            '_|@@@@': WIN,
            '|@@@@*': WIN,
            '|@@@@_': WIN,
            }

class Move:
    def __init__(self, pos, rank):
        self.pos = pos
        self.rank_ = rank
    
    def getPosition(self):
        return self.pos
    
    def __cmp__(self, other):
        return self.rank_ - other.rank_

toAI = {black:'*', white:'@', empty:'_', '_':'_', 'wall':'W', '|':'|'}
class AICross:
    def __init__(self):
        self.stone_ = '_'
        self.rank_ = 0
        self.ripples_ = []
        
    def getRippleSlices(self):
        for cross, aslice in self.ripples_:
            yield cross, ''.join([x.stone_ for x in aslice])
            
    def placeStone(self, stone):
        self.stone_ = toAI[stone]

origin = AICross()
origin.stone_ = '|'
        
class AIBoard:
    dirs = ((-1, 0), (0, -1), (-1, -1), (1, -1), (1, 0), (0, 1), (1, 1), (-1, 1))
    
    def __init__(self, boardSize, patterns):
        self.patterns = patterns
        self.crosses = {}
        for pos in product(range(boardSize), repeat=2):
            self.crosses[pos] = AICross()
        for pos, cross in self.crosses.items():
            for s in list(self.slices_(pos)):
                for c in s:
                    if c is not origin:
                        c.ripples_.append((cross, s))
                    
    def placeStones(self, stones):
        for pos, stone in stones:
            self.placeStone(pos, stone)
        
    def slices_(self, pos):
        for start in range(-2, 1):
            for (dx, dy) in self.dirs:
                for length in range(6, 7):
                    try:
                        s = [self.crosses[(pos[0] + i * dx, pos[1] + i * dy)] for i in range(start, start + length)]
                        for i in range(len(s)):
                            if s[i] is self.crosses[(pos)]:
                                s[i] = origin
                        yield s
                    except:
                        pass

    def getSlice(self, move):
        for s in self.crosses[move].getSlices():
            yield s
                    
    def placeStone(self, pos, stone):
        cross = self.crosses[pos]
        for c, aslice in cross.getRippleSlices():
            c.rank_ -= self.patterns.get(aslice, 0)
        self.crosses[pos].placeStone(stone)
        for c, aslice in cross.getRippleSlices():
            c.rank_ += self.patterns.get(aslice, 0)

def blackCopyOfPattern(pattern):
    op = {}
    for key, v in pattern.viewitems():
        op[key.replace('*', '#').replace('@', '*').replace('#', '@')] = v
    return op

class AIRenjuPlayer(object):
    
    def __init__(self, who, board, patternsForWhite = stonePatterns):
        self.who = who
        if who == white:
            patterns = patternsForWhite
        else:
            patterns = blackCopyOfPattern(patternsForWhite)
        self.aiBoard = AIBoard(board.groundSize, patterns)
        self.aiBoard.placeStones(board.stones.items())
            
    def placeStone(self, pos, stone):
        self.aiBoard.placeStone(pos, stone)
        
    def placeStones(self, stones):
        self.aiBoard.placeStones(stones)
        
    def getMyMove(self):
        evaluateMove = lambda x:Move(x, self.aiBoard.crosses[x].rank_)
        return max(map(evaluateMove, self._possibleMoves())).getPosition()
    
    def _possibleMoves(self):
        for pos, cross in self.aiBoard.crosses.items():
            if cross.stone_ == '_':
                yield pos
    
