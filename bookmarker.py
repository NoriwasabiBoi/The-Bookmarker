import nuke
from nukescripts import panels

from contextlib import contextmanager
import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets


@contextmanager
def selected(selection_list):
    orig_selection = nuke.selectedNodes()
    nukescripts.clear_selection_recursive()
    for node in selection_list or []:
        node.setSelected(True)
    try:
        yield
    finally:
        for node in nuke.selectedNodes() or []:
            node.setSelected(False)
        for node in orig_selection or []:
            node.setSelected(True)


class Bookmarker(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QtWidgets.QGridLayout(self)
        self.selection_sets = {}
        self.buttons = []

        button_size = (200, 100)
        position_grid = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]

        for index in range(1, 7):
            button = QtWidgets.QPushButton(f'Selection Set {index}')
            button.clicked.connect(self.button_action)
            self.buttons.append(button)

        for button, pos in zip(self.buttons, position_grid):
            self.layout.addWidget(button, *pos)

        for button in self.buttons:
            button.setFixedSize(*button_size)

    def button_action(self):
        sender = self.sender()
        modifiers = QtWidgets.QApplication.keyboardModifiers()  # Get the current keyboard modifiers
        shift_pressed = modifiers & QtCore.Qt.ShiftModifier  # Check if Shift is pressed

        button = f'{sender.text()}'.split()[-1]

        if shift_pressed:
            selection = nuke.selectedNodes()
            print(f'Added to Selection {button}')
            self.selection_sets[button] = selection
            return

        print(f'Zooming On Selection')
        selection_list = self.selection_sets.get(button)

        with selected(selection_list):
            nuke.zoomToFitSelected()


if __name__ == '__main__':
    panels.registerWidgetAsPanel(
        'Bookmarker',
        'The Bookmarker',
        'uk.co.thefoundry.NukeTestWindow'
    )
    QtWidgets.QPushButton()