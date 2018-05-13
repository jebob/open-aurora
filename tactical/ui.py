import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import *
from tab import Tab


class MapTab(Tab):
    def __init__(self, tactical):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.tactical = tactical

        self.cur_posn = 0+0j  # Define some initial view
        self.cur_scal = 100.0

        self.mapFrame = TacView(self, tactical)

        # todo: readd a end turn button
        #turn_btn = QPushButton('Next turn', self)
        #turn_btn.setToolTip('This ends the turn')
        #turn_btn.resize(turn_btn.sizeHint())
        #turn_btn.clicked.connect(None)

        self.x_label = QLabel('x_label')
        self.y_label = QLabel('y_label')
        self.s_label = QLabel('s_label')
        self.t_label = QLabel('t_label')  # Todo: ensure this is initialized properly
        self.map_instructions = QLabel('Welcome to the game!\nUse the arrow keys to move around\nand +/- to scroll.')

        ctrl_panel = QVBoxLayout()
        ctrl_panel.addWidget(self.x_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.y_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.s_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.t_label, alignment=Qt.AlignHCenter)
        ctrl_panel.addWidget(self.map_instructions, alignment=Qt.AlignHCenter)
        # ctrl_panel.addWidget(turn_btn, alignment=Qt.AlignHCenter)

        hbox = QHBoxLayout()

        hbox.addLayout(ctrl_panel)
        hbox.addWidget(self.mapFrame, stretch=1)

        self.setLayout(hbox)
        self.update_ui()  # Finalise initialisation

    def keyPressEvent(self, event):
        # Todo: implement movement adjustments relative to the screen size e.g. up means 1/3 height upwards.
        key = event.key()
        if key == Qt.Key_Left:
            self.move_view(posn=1)

        elif key == Qt.Key_Right:
            self.move_view(posn=-1)

        elif key == Qt.Key_Up:
            self.move_view(posn=1j)

        elif key == Qt.Key_Down:
            self.move_view(posn=-1j)

        elif key == Qt.Key_Minus:
            self.move_view(scal=1/math.sqrt(2))

        elif key in [Qt.Key_Plus, Qt.Key_Equal]:
            self.move_view(scal=math.sqrt(2))

        else:
            super(MapTab, self).keyPressEvent(event)

    def update_ui(self):
        """This function updates this tab"""
        # Write to the labels in the control panel.
        self.x_label.setText('x={:4f}'.format(self.cur_posn.real))
        self.y_label.setText('y={:4f}'.format(self.cur_posn.imag))
        self.s_label.setText('scale={:4f}'.format(self.cur_scal))
        self.t_label.setText('time={:4f}'.format(self.tactical.state.time))

        # No need to trigger a paint event, the above should cause QT to trigger one.

    def move_view(self, posn=None, scal=None):
        """This function modifies the existing view by adding a new position and/or multiplying the scale."""
        self.cur_posn = self.cur_posn if posn is None else self.cur_posn + posn
        self.cur_scal = self.cur_scal if scal is None else self.cur_scal * scal
        self.update_ui()


class TacView(QFrame):
    """This class is for rendering the positions of things on a tactical view"""
    def __init__(self, parent, state):
        super().__init__()

        self.par = parent
        self.state = state

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        painter.fillRect(0, 0, rect.right(), rect.bottom(), QColor(0x000000))

        for piece in self.state.pieceList:
            self.draw_ship(painter, (piece.start_position + self.par.cur_posn) * self.par.cur_scal)

    @staticmethod
    def draw_ship(painter, posn):
        color = QColor(0x6666CC)
        width = 10
        painter.fillRect(posn.real, posn.imag, width, width, color)