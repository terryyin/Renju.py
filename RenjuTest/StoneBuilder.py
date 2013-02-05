from Renju import black, white
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
            self.stones.append((self.who, (self.origin[0] + self.dx * i, self.origin[1] + self.dy * i)))
        self.currentIndex += n
        return self
    
    def get(self):
        stones = self.stones
        self.stones = []
        return stones
    def getLastPosition(self):
        return self.get()[0][1]
    
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
                   'O' : lambda:builder.stone(white).count(1),
                   'X' : lambda:builder.stone(black).count(1),
                   '$' : lambda:builder.stone("wall").count(1)
                   }
        map(lambda c: toStone[c](), patternString[3:])
        self.stones = builder.get()
    def getOnePosition(self):
        return self.stones[0][1]
    
def stos(patternString):
    return OneRowPattern(patternString).stones

def stop(patternString):
    return OneRowPattern(patternString).getOnePosition()
