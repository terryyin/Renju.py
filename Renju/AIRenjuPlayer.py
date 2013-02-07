from itertools import product

from RenjuGame import black, white, empty

MIN_RANK = 2  
TWO23 = 100
THREAT = TWO23 * 2 - 10
URGENT = THREAT * 2
WINNING = URGENT * 2
LOSS = 4000
WIN = 10000
stonePatterns = {
            '__|_*_': MIN_RANK, 
            '_*|___': MIN_RANK + 1, 
            '__|*__': MIN_RANK + 2, 
            '_@|___': MIN_RANK + 3, 
            '__|@__': MIN_RANK + 4, 
            
            '_|_**_': TWO23, 
            '_|**__': TWO23 + 1, 
            '_*|*__': TWO23/2 + 1, 
            '_|_@@_': TWO23 + 2, 
            '_|@@__': TWO23 + 3, 
            '_@|@__': TWO23/2 + 3, 

            '_|***@': THREAT+1, 
            '_|***W': THREAT+1, 
            '|_***@': THREAT+1, 
            '|_***W': THREAT+1, 
            '_*|**@': THREAT+1, 
            '_*|**W': THREAT+1, 
            '*_|**@': THREAT+1, 
            '*_|**W': THREAT+1, 
            'W*|**_': THREAT+1, 
            '@*|**_': THREAT+1, 
            'W*|*_*': THREAT+1, 
            '@*|*_*': THREAT+1, 
            'W*|_**': THREAT+1, 
            '@*|_**': THREAT+1, 

            '_|@@@*': THREAT+10, 
            '_|@@@W': THREAT+10, 
            '|_@@@*': THREAT+10, 
            '|_@@@W': THREAT+10, 
            '_@|@@*': THREAT+10, 
            '_@|@@W': THREAT+10, 
            '@_|@@*': THREAT+10, 
            '@_|@@W': THREAT+10, 
            'W@|@@_': THREAT+10, 
            '*@|@@_': THREAT+10, 
            'W@|@_@': THREAT+10, 
            '*@|@_@': THREAT+10, 
            'W@|_@@': THREAT+10, 
            '*@|_@@': THREAT+10, 

            '_|***_': URGENT, 
            '_*|**_': URGENT, 
            '_|@@@_': WINNING, 
            '_@|@@_': WINNING, 
            
            '_*|***': LOSS,
            '@*|***': LOSS,
            'W*|***': LOSS,
            '*|***@': LOSS,
            '*|***_': LOSS,
            '*|***W': LOSS,
            '*|****': LOSS,
            '**|***': LOSS,
            '**|**@': LOSS,
            '**|**_': LOSS,
            '**|**W': LOSS,
            '*|****': LOSS,
            '@|****': LOSS,
            '_|****': LOSS,
            'W|****': LOSS,
            '@|@@@@': WIN,
            '_@|@@@': WIN,
            '*@|@@@': WIN,
            'W@|@@@': WIN,
            '@|@@@*': WIN,
            '@|@@@_': WIN,
            '@|@@@W': WIN,
            '@|@@@@': WIN,
            '@@|@@@': WIN,
            '@@|@@*': WIN,
            '@@|@@_': WIN,
            '@@|@@@': WIN,
            '@@|@@W': WIN,
            '*|@@@@': WIN,
            '_|@@@@': WIN,
            'W|@@@@': WIN,
            '|@@@@*': WIN,
            '|@@@@_': WIN,
            '|@@@@W': WIN,
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
        self.rank_ = [0, 0]
        self.ripples_ = []
        
    def getRippleSlices(self):
        for cross, aslice in self.ripples_:
            yield cross, ''.join([x.stone_ for x in aslice])
            
    def placeStone(self, stone):
        self.stone_ = toAI[stone]

origin = AICross()
origin.stone_ = '|'
border = AICross()
border.stone_ = 'W'
        
class AIBoard:
    dirs = ((-1, 0), (0, -1), (-1, -1), (1, -1), (1, 0), (0, 1), (1, 1), (-1, 1))
    
    def __init__(self, boardSize, patterns, blackPatterns):
        self.patterns = [patterns, blackPatterns]
        self.crosses = {}
        for pos in product(range(-1, boardSize+1), repeat=2):
            if (boardSize>pos[0]>=0 and boardSize>pos[1]>=0):
                self.crosses[pos] = AICross()
            else:
                self.crosses[pos] = border

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
            c.rank_[0] -= self.patterns[0].get(aslice, 0)
            c.rank_[1] -= self.patterns[1].get(aslice, 0)
        self.crosses[pos].placeStone(stone)
        for c, aslice in cross.getRippleSlices():
            c.rank_[0] += self.patterns[0].get(aslice, 0)
            c.rank_[1] += self.patterns[1].get(aslice, 0)

def blackCopyOfPattern(pattern):
    op = {}
    for key, v in pattern.viewitems():
        op[key.replace('*', '#').replace('@', '*').replace('#', '@')] = v
    return op

class AIRenjuPlayer(object):
    
    def __init__(self, who, board, patternsForWhite = stonePatterns):
        self.who = who
        self.aiBoard = AIBoard(board.groundSize, patternsForWhite, blackCopyOfPattern(patternsForWhite))
        self.aiBoard.placeStones(board.stones.items())
            
    def placeStone(self, pos, stone):
        self.aiBoard.placeStone(pos, stone)
        
    def placeStones(self, stones):
        self.aiBoard.placeStones(stones)
        
    def getMyMove(self, level = 0):
        return self.getMyMove_(level, self.who).getPosition()
    def getMyMove_(self, level, who):
        evaluateMove = lambda x:Move(x, self.aiBoard.crosses[x].rank_[who == black])
        unsortedMoves = map(evaluateMove, self._possibleMoves())
        alpha = max(unsortedMoves)
        if LOSS > alpha.rank_ >= WINNING or alpha.rank_ >= WIN:
            alpha.rank_ = WIN
        else:
            if alpha.rank_ >= LOSS:
                lossingMoves = filter(lambda x:x.rank_ >=LOSS, unsortedMoves)
                if len(lossingMoves) > 1:
                    alpha.rank_ = -WIN
                    return alpha
                else:
                    if len(filter(lambda x:x.rank_ >=WINNING, unsortedMoves)) > 1:
                        alpha.rank_ = WIN
                        return alpha
            if URGENT+THREAT >alpha.rank_ >= URGENT:
                if len(filter(lambda x:URGENT+THREAT>x.rank_ >=URGENT, unsortedMoves)) > 2:
                    alpha.rank_ = -WIN
                    return alpha
            if alpha.rank_ >= LOSS:
                unsortedMoves = lossingMoves
            alpha.rank_ = 0
            if level > 0:
                possibleMoves = sorted(unsortedMoves, reverse = True)[:10]
                alpha.rank_ = -WIN * 10
                for move in possibleMoves:
                    pos = move.pos
                    self.aiBoard.placeStone(pos, who)
                    beta = self.getMyMove_(level - 1, who.oppose)
                    if alpha.rank_ < - beta.rank_:
                        alpha.rank_ = - beta.rank_
                        alpha.pos = pos
                    self.aiBoard.placeStone(pos, '_')
        return alpha
    
    def _possibleMoves(self):
        for pos, cross in self.aiBoard.crosses.items():
            if cross.stone_ == '_':
                yield pos
    
