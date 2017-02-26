#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

This is a Tetris game clone.

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QPushButton, QAction, qApp, QGridLayout, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QIcon


class GamePiece:
    detectRange = 0  # by default things don't detect
    speed = 0  # by default things don't move
    """"This is a thing class. It represents an object or coll"""
    def __init__(self, position):
        assert isinstance(position, tuple)
        assert len(position) == 2
        assert all(isinstance(n, int) for n in position)
        self.position = position


class GameState:
    """This is a dummy class containing the entire game state"""
    def __init__(self):
        self.pieceList = []
        self.set_demo()

    def set_demo(self):
        demo_posns = [(1, 2), (4, 5), (3, -1)]
        self.pieceList = [GamePiece(posn) for posn in demo_posns]


class OpenAurora(QMainWindow):
    def __init__(self):
        super().__init__()

        self.state = GameState()

        self.maintab = MapTab(self)
        self.setCentralWidget(self.maintab)

        #self.statusbar = self.statusBar()
        #self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.resize(300, 380)
        self.center()
        self.setWindowTitle('OpenAurora')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def end_turn(self):
        """This method ends the turn"""
        pass


class MapTab(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.mapFrame = TacView(parent.state)

        turnBtn = QPushButton('Next turn', self)
        turnBtn.setToolTip('This ends the turn')
        turnBtn.resize(turnBtn.sizeHint())
        turnBtn.clicked.connect(parent.end_turn)

        hbox = QHBoxLayout()

        hbox.addWidget(turnBtn)
        hbox.addWidget(self.mapFrame, stretch=1)

        self.setLayout(hbox)


class TacView(QFrame):
    """This class is for rendering the positions of things on a tactical view"""
    def __init__(self, state):
        super().__init__()

        self.curX = 0
        self.curY = 0
        self.curScale = 100.0

        self.state = state

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        painter.fillRect(0, 0, rect.right(), rect.bottom(), QColor(0x000000))

        for piece in self.state.pieceList:
            self.draw_ship(painter, piece.position[0] * self.curScale, piece.position[1] * self.curScale)
            pass

    def draw_ship(self, painter, x, y):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(0x6666CC)
        width = 10
        painter.fillRect(x, y, width, width, color)

        #painter.setPen(color.lighter())
        #painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        #painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        #painter.setPen(color.darker())
        #painter.drawLine(x + 1, y + self.squareHeight() - 1,
        #                 x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        #painter.drawLine(x + self.squareWidth() - 1,
        #                 y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


class Tetrominoe(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    def __init__(self):

        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.setShape(Tetrominoe.NoShape)

    def shape(self):
        return self.pieceShape

    def setShape(self, shape):

        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def setX(self, index, x):
        self.coords[index][0] = x

    def setY(self, index, y):
        self.coords[index][1] = y

    def minX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):

        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):

        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):

        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotateLeft(self):

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotateRight(self):

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


if __name__ == '__main__':
    app = QApplication([])
    OA = OpenAurora()
    sys.exit(app.exec_())