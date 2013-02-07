NameOfTheGame = "Renju"

from Tkinter import *
import Tkinter
from AIRenjuPlayer import AIRenjuPlayer
from RenjuGame import RenjuBoard, black, white

class RenjuGameTkWindow():
    PADDING = 2
    BORDER = 10
    LINE_THICKNESS = 1
    def __init__(self, root, game):
        self.board = game
        root.title(NameOfTheGame)
        Label(root, text='Welcome To The Renju Game!').pack(pady=10)
        self.canvas = Tkinter.Canvas(root, height=600, width=600)
        self.canvas.pack()
        width = int(self.canvas["width"])
        height = int(self.canvas["height"])
        self.GRID_SIZE = ([width, height][width > height] - self.BORDER * 2) / (game.groundSize)
        self._drawGround()
        def handler(event, self=self):
            return self.__onClick(event)
        self.canvas.bind('<Button-1>', handler)
        self.aiMove()
        
    def _drawGround(self):
        for i in range(0, self.board.groundSize):
            self.canvas.create_line(
                               self.GRID_SIZE/2 + self.BORDER,
                               self.GRID_SIZE/2 + self.BORDER + self.GRID_SIZE * i,
                               self.GRID_SIZE/2 + self.BORDER + self.GRID_SIZE * (self.board.groundSize-1),
                               self.GRID_SIZE/2 + self.BORDER + self.GRID_SIZE * i,
                               width=self.LINE_THICKNESS)
            self.canvas.create_line(
                               self.GRID_SIZE/2 + self.BORDER + self.GRID_SIZE * i,
                               self.GRID_SIZE/2 + self.BORDER,
                               self.GRID_SIZE/2 + self.BORDER + self.GRID_SIZE * i,
                               self.GRID_SIZE/2 + self.BORDER + self.GRID_SIZE * (self.board.groundSize - 1),
                               width=self.LINE_THICKNESS)
        
    def aiMove(self):
        self.aiPlayer = AIRenjuPlayer(black, self.board)
        move = self.aiPlayer.getMyMove(3)
        self._placeStone(move, black)
    
    def __onClick(self, event):
        pos = self._getPosition(event.x, event.y)
        self._placeStone(pos, white)
        self.aiMove()
    
    def _placeStone(self, position, who):
        self.board.place(who, position)
        if who:
            self.__drawStone(position, who)
        
    def __drawStone(self, position, who):
        xy = self._getCoordination(position)
        self.canvas.create_oval(xy[0], xy[1], xy[0] + self.GRID_SIZE, xy[1] + self.GRID_SIZE, fill=who.color)
    
    def _getPosition(self, x, y):
        toGround = lambda x: (x - self.BORDER) / self.GRID_SIZE
        return (toGround(x), toGround(y))
    
    def _getCoordination(self, position):
        toAxis = lambda x: self.GRID_SIZE * x + self.BORDER
        return (toAxis(position[0]), toAxis(position[1]))

if __name__ == "__main__":
    root = Tk()
    window = RenjuGameTkWindow(root, RenjuBoard())
    root.mainloop()
