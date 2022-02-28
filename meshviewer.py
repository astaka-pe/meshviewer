import sys
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np
import pymeshlab as ml

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.meshset = ml.MeshSet()
        self.items = []
        self.setGeometry(300, 300, 960, 720)
        self.initUI()
        self.smooth()
    
    def initUI(self):
        centerWidget = QWidget()
        self.setCentralWidget(centerWidget)
        layout = QVBoxLayout()
        centerWidget.setLayout(layout)
        self.viewer = gl.GLViewWidget()
        layout.addWidget(self.viewer, 1)
        self.viewer.setWindowTitle("Mesh Viewer")
        self.viewer.setCameraPosition(distance=40)

        openFile = QAction("&Open", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip("Open new File")
        openFile.triggered.connect(self.openfile)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openFile)

        # g = gl.GLGridItem()
        # g.setSize(200, 200)
        # g.setSpacing(5, 5)
        # self.viewer.addItem(g)

        sm_bt = QPushButton("smooth", self)
        sm_bt.move(10, 10)
        sm_bt.clicked.connect(self.smooth)

    def openfile(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "/Users/shota/Downloads")
        vertices, faces = self.loadOBJ(fname[0])
        meshdata = gl.MeshData(vertexes=vertices, faces=faces)
        mesh = gl.GLMeshItem(meshdata=meshdata, drawEdges=True, color=(0, 0.6, 0.3, 1), edgeColor=(0, 0, 0, 1))
        self.items.append(mesh)
        self.viewer.addItem(mesh)
    
    def loadOBJ(self, fname):
        self.meshset.load_new_mesh(fname)
        vertices = self.meshset.current_mesh().vertex_matrix()
        faces = self.meshset.current_mesh().face_matrix()
        return vertices, faces
    
    def smooth(self):
        if len(self.items) > 0:
            #self.meshset.apply_filter("laplacian_smooth", stepsmoothnum=3)
            self.meshset.apply_filter("laplacian_smooth", stepsmoothnum=3, cotangentweight=False)
            vertices = self.meshset.current_mesh().vertex_matrix()
            faces = self.meshset.current_mesh().face_matrix()
            sm_meshdata = gl.MeshData(vertexes=vertices, faces=faces)
            sm_mesh = gl.GLMeshItem(meshdata=sm_meshdata, drawEdges=True, color=(0, 0.6, 0.3, 1), edgeColor=(0, 0, 0, 1))
            self.viewer.removeItem(self.items[0])
            self.viewer.addItem(sm_mesh)
            self.items.append(sm_mesh)
            self.items = self.items[1:]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())