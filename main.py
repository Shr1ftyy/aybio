from PyQt5 import QtCore # core Qt functionality, QtWidgets
from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
from PyQt5 import QtOpenGL # provides QGLWidget, QtWidgets,a special OpenGL QWidget)
from PyQt5 import QtWidgets
import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
import sys # we'll need this later to run our Qt application

from OpenGL.arrays import vbo
import numpy as np

from renderer import *

if __name__ == '__main__':

  app = QtWidgets.QApplication(sys.argv)

  win = MainWindow()
  win.show()

  sys.exit(app.exec_())

