from itertools import product

class AIRenjuPlayer(object):
    
    def __init__(self, who):
        self.who = who
        
    def getMyMove(self, game):
        for move in self._possibleMoves(game):
            if game.willWinWith(move, self.who):
                return move
            if game.willWinWith(move, self.who.oppose):
                return move
        return move
    
    def _possibleMoves(self, game):
        for pos in product(range(game.groundSize), repeat = 2):
            if pos not in game.stones:
                yield pos
    
