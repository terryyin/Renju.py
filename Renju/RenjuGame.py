class Player:
    def __init__(self, color):
        self.color = color
        self.oppose = None

black = Player("black")
white = Player("white")
empty = Player("empty")

black.oppose = white
white.oppose = black

class RenjuBoard:
    
    dirs = ((-1,0), (0,-1), (-1,-1), (1,-1))
    
    def __init__(self, groundSize = 15):
        self.groundSize = groundSize
        self.whoseTurn = white
        self.stones = {}
    
    def place(self, who, position):
        self.stones[position] = who
        return self
    
    def places(self, stones):
        for (pos, who) in stones:
            self.place(who, pos)
    
    def willWinWith(self, move, who):
        for (dx, dy) in self.dirs:
            for i in range(1, 5):
                pos = (move[0] + i * dx, move[1] + i * dy)
                if self.stones.get(pos) != who:
                    break
            else:
                return True
            for j in range(1, 6 - i):
                pos = (move[0] - j * dx, move[1] - j * dy)
                if self.stones.get(pos) != who:
                    break
            else:
                return True
        return False
