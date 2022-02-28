import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.upper = QCheckBox("test1", self)
        self.upper.move(100, 30)
        self.upper.stateChanged.connect(self.uppercase)

        self.lower = QCheckBox("test2", self)
        self.lower.move(180, 30)

        self.group = QButtonGroup()
        self.group.addButton(self.upper, 1)
        self.group.addButton(self.lower, 2)

        self.horizon = QHBoxLayout()
        self.vertical = QVBoxLayout()
        self.horizon.addLayout(self.vertical)
        self.setLayout(self.horizon)

        self.button = QPushButton("excute", self)
        self.button.clicked.connect(self.output)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle("QCheckBox")

    def uppercase(self):
        if self.upper.isChecked():
            self.upper_a = QCheckBox("A", self)
            self.vertical.addWidget(self.upper_a)

            self.upper_b = QCheckBox("B", self)
            self.vertical.addWidget(self.upper_b)
        else:
            self.vertical.removeWidget(self.upper_a)
            self.vertical.removeWidget(self.upper_b)
    
    def output(self):
        outputs = []
        if self.upper_a.isChecked():
            outputs.append("A")
        if self.upper_b.isChecked():
            outputs.append("B")
        for output in outputs:
            print(output)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())