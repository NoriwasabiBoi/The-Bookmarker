import nuke
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
from nukescripts import panels

class Bookmarker(QtWidgets.QWidget):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QGridLayout(self)

        width = 200
        height = 100
        self.selection_sets = {
            '1':"",
            '2':"",
            '3':"",
            '4':"",
            '5':"",
            '6':""
        }        

        # Create buttons with unique names
        self.button1 = QtWidgets.QPushButton('Selection Set 1')
        self.button2 = QtWidgets.QPushButton('Selection Set 2')
        self.button3 = QtWidgets.QPushButton('Selection Set 3')
        self.button4 = QtWidgets.QPushButton('Selection Set 4')
        self.button5 = QtWidgets.QPushButton('Selection Set 5')
        self.button6 = QtWidgets.QPushButton('Selection Set 6')

        # Connect buttons to actions
        self.button1.clicked.connect(self.button_action)
        self.button2.clicked.connect(self.button_action)
        self.button3.clicked.connect(self.button_action)
        self.button4.clicked.connect(self.button_action)
        self.button5.clicked.connect(self.button_action)
        self.button6.clicked.connect(self.button_action)

        # Add buttons to the layout in a grid
        self.layout.addWidget(self.button1, 0, 0)
        self.layout.addWidget(self.button2, 0, 1)
        self.layout.addWidget(self.button3, 1, 0)
        self.layout.addWidget(self.button4, 1, 1)
        self.layout.addWidget(self.button5, 2, 0)
        self.layout.addWidget(self.button6, 2, 1)

        # Set uniform size for all buttons
        self.button1.setFixedSize(width, height)
        self.button2.setFixedSize(width, height)
        self.button3.setFixedSize(width, height)
        self.button4.setFixedSize(width, height)
        self.button5.setFixedSize(width, height)
        self.button6.setFixedSize(width, height)

    def button_action(self):
        sender = self.sender()
        modifiers = QtWidgets.QApplication.keyboardModifiers()  # Get the current keyboard modifiers
        shift_pressed = modifiers & QtCore.Qt.ShiftModifier  # Check if Shift is pressed
        
        button = f'{sender.text()}'.split()[-1]
        
        if shift_pressed:
            selection = nuke.selectedNodes()
            print(f'Added to Selection {button}')
            button = f'{sender.text()}'.split()[-1]
            self.selection_sets[button] = selection
        else:
            print(f'Zooming On Selection')
            selection_list = self.selection_sets[button]
            for node in selection_list:
                node.setSelected(True)
            nuke.zoomToFitSelected()
            for node in selection_list:
                node.setSelected(False)
            

panels.registerWidgetAsPanel('Bookmarker', 'The Bookmarker', 'uk.co.thefoundry.NukeTestWindow')

QtWidgets.QPushButton()