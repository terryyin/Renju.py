from Renju import *
class StoneBuilder:
    dirs = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
    def __init__(self):
        self.origin = (0, 0)
        self.stones = []
        self.expects = []
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
    
    def toSouth(self):
        self.dx = 0
        self.dy = 1
        return self
    
    def toSouthEast(self):
        self.dx = 1
        self.dy = 1
        return self
    
    def toSouthWest(self):
        self.dx = -1
        self.dy = 1
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
            self.stones.append(((self.origin[0] + self.dx * i, self.origin[1] + self.dy * i), self.who))
        self.currentIndex += n
        return self
    def expectOne(self):
        self.expects.append((self.origin[0] + self.dx * self.currentIndex, self.origin[1] + self.dy * self.currentIndex))
        self.currentIndex += 1
    def get(self):
        stones = self.stones
        self.stones = []
        return stones
    def getLastPosition(self):
        return self.get()[0][0]
    
class OneRowPattern:
    def __init__(self, patternString):
        builder = StoneBuilder().From((ord(patternString[0]) - ord('A'), ord(patternString[1]) - ord('0')))
        {
         '-':StoneBuilder.toEast,
         '|':StoneBuilder.toSouth,
         '\\':StoneBuilder.toSouthEast,
         '/':StoneBuilder.toSouthWest,
         }[patternString[2]](builder)
         
        toStone = {
                   '_' : lambda:builder.skip(1),
                   ' ' : lambda:builder.skip(1),
                   'O' : lambda:builder.stone(white).count(1),
                   'X' : lambda:builder.stone(black).count(1),
                   '$' : lambda:builder.stone("wall").count(1),
                   '?' : lambda:builder.expectOne()
                   }
        map(lambda c: toStone[c](), patternString[3:])
        self.stones = builder.get()
        self.expects = builder.expects
    def getOnePosition(self):
        return self.stones[0][0]

class MultipleRowPattern:
    def __init__(self, patternString):
        self.stones =[]
        self.expects = []
        c = ord('0')
        for p in patternString.splitlines()[1:]:
            oneRow = OneRowPattern('A'+chr(c)+"-" + p.strip()[1:])
            self.stones.extend(oneRow.stones)
            self.expects.extend(oneRow.expects)
            c+=1
    
def parseStonePatternString(patternString):
    if patternString.startswith(' '):
        parsed = MultipleRowPattern(patternString)
    else:
        parsed = OneRowPattern(patternString)
    return parsed.stones, parsed.expects

def stop(patternString):
    return OneRowPattern(patternString).getOnePosition()

def aiMaxmin(stonesPattern, who, asWho, level):
    player = AIRenjuPlayer(who, RenjuBoard())
    stones, expects = parseStonePatternString(stonesPattern)
    player.placeStones(stones)
    return player.negamax_(level, asWho), expects


