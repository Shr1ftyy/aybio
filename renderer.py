from OpenGL.raw.GL.VERSION.GL_1_0 import GL_QUADS
from PyQt5 import QtCore # core Qt functionality, QtWidgets
from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
from PyQt5 import QtOpenGL # provides QGLWidget, QtWidgets,a special OpenGL QWidget)
from PyQt5 import QtWidgets
import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
import sys # we'll need this later to run our Qt application
import random as r
from datetime import datetime

from world import World
from creatures import Creature
from config import *

from OpenGL.arrays import vbo
import numpy as np

class GLWidget(QtOpenGL.QGLWidget):
  def __init__(self, parent=None):
    self.parent = parent
    QtOpenGL.QGLWidget.__init__(self, parent)
    self.world = World()
    self.FPS = 0
    self.parent = parent

  def initializeGL(self):
    self.qglClearColor(QtGui.QColor(1, 100, 128)) # initialize the screen to blue
    gl.glEnable(gl.GL_DEPTH_TEST) # enable depth testing

    self.world.initWorld()
    self.initCreatures()

    self.rotX = INIT_ROT_X 
    self.rotY = INIT_ROT_Y
    self.rotZ = INIT_ROT_Z
    self.zoom = ZOOM_SCALE
    self.t = 0 
    self.nb_frames = 0

  def resizeGL(self, width, height):
    gl.glViewport(0, 0, width, height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    aspect = width / float(height)

    GLU.gluPerspective(90.0, aspect, 1.0, 500.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)

  def paintGL(self):
    self.start_time = datetime.now()
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    gl.glPushMatrix() # push the current matrix to the current stack

    gl.glTranslate(0.0, 0.0, -50.0) # third, translate cube to specified depth
    gl.glScale(self.zoom, self.zoom, self.zoom) # second, scale cube
    gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
    gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
    gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
    # gl.glTranslate(-0.5, -0.5, -0.5) # first, translate cube center to origin

    self.world.update()
    self.updateLife()
    self.t += 1
    time_passed = datetime.now() - self.start_time
    # print(time_passed.microseconds/1000)
    self.FPS = 1000.0/(time_passed.microseconds/1000)
    self.parent.fps_counter.setText(str(int(self.FPS)) + ' FPS')
    self.parent.fps_counter.resize(int(self.parent.width()/5), int(self.parent.height()/5))
    self.parent.repaint()

    gl.glPopMatrix() # restore the previous modelview matrix

  def initCreatures(self):
    minSize = 3
    maxSize = 15
    self.creatures = []
    for i in range(NUM_CREATURES):
      # moves = np.array([[r.randint(-1,1), r.randint(-1,1), r.randint(-1,1)] for i in range(1000)])
      init_pos = np.array([r.randint(-150, 150), r.randint(-150, 150), r.randint(-150, 150)])
      size = 3 + r.random()*(maxSize - minSize)
      # c = Creature(init_pos, moves, size)
      c = Creature(pos=init_pos, size=size)
      self.creatures.append(c)

  def updateLife(self):
    for creature in self.creatures:
      creature.move(np.array([r.randint(-1,1), r.randint(-1,1), r.randint(-1,1)]))
      # creature.move(np.array([1,0,0]))
      creature.rotate(pitch=np.pi/160, yaw=0, roll=np.pi/160)
      gl.glColor3d(1,0,1)
      gl.glBegin(gl.GL_LINES)
      for conn in creature.hitbox_edges:
        for point in conn:
          gl.glVertex3fv(creature.hitbox[point])
      gl.glEnd()

      gl.glColor3d(150/255, 0, 30/255)
      gl.glEnable(gl.GL_POINT_SMOOTH)
      gl.glPointSize(creature.size/2)
      gl.glBegin(gl.GL_POINTS)
      gl.glVertex3fv(creature.eye)
      gl.glEnd()



  def setRotX(self, val):
    self.rotX = val

  def setRotY(self, val):
    self.rotY = val

  def setRotZ(self, val):
    self.rotZ = val

  def setZoom(self, val):
    self.zoom = val * 0.01

class MainWindow(QtWidgets.QMainWindow):

  def __init__(self):
    QtWidgets.QMainWindow.__init__(self) # call the init for the parent class

    self.resize(500, 500)
    self.setWindowTitle('aybio')

    self.glWidget = GLWidget(self)
    self.initGUI()

    timer = QtCore.QTimer(self)
    timer.setInterval(5) # period, in milliseconds
    timer.timeout.connect(self.glWidget.updateGL)
    timer.start()

  def initGUI(self):
    central_widget = QtWidgets.QWidget()
    gui_layout = QtWidgets.QVBoxLayout()
    central_widget.setLayout(gui_layout)

    self.setCentralWidget(central_widget)

    gui_layout.addWidget(self.glWidget)

    self.fps_counter = QtWidgets.QLabel(self)
    self.fps_counter.setText(str(self.glWidget.FPS) + ' FPS')
    self.fps_counter.resize(int(self.width()/5), int(self.height()/5))

    sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    sliderX.setMinimum(0)
    sliderX.setMaximum(360)
    sliderX.setValue(INIT_ROT_X)
    sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

    sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    sliderY.setMinimum(0)
    sliderY.setMaximum(360)
    sliderY.setValue(INIT_ROT_Y)
    sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

    sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    sliderZ.setMinimum(0)
    sliderZ.setMaximum(360)
    sliderZ.setValue(INIT_ROT_Z)
    sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))

    sliderW = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    sliderW.setMinimum(1)
    sliderW.setMaximum(100)
    sliderW.setValue(ZOOM_SCALE)
    sliderW.valueChanged.connect(lambda val: self.glWidget.setZoom(val))

    gui_layout.addWidget(sliderX)
    gui_layout.addWidget(sliderY)
    gui_layout.addWidget(sliderZ)
    gui_layout.addWidget(sliderW)
    gui_layout.addWidget(self.fps_counter)

  # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
  #   if event.buttons() == QtCore.Qt.RightButton:

  #     return
  #   if event.buttons() == QtCore.Qt.MiddleButton:
  #     # Drag event
  #     event.accept()
  #     self.moveStartX = event.x()
  #     self.moveStartY = event.y()
  #     return
    # if event.modifiers() == QtCore.Qt.ShiftModifier:
    #   self.draggedMarker = self.getNearestMarker(event.x(), event.y())
    # elif event.modifiers() == QtCore.Qt.ControlModifier:
    #   event.accept()
    #   self.draggedBox = True
    #   self.draggedBoxStart = (event.x(), event.y())
    #   return
    # self.mouseMoveEvent(event) 


if __name__ == '__main__':

  app = QtWidgets.QApplication(sys.argv)

  win = MainWindow()
  win.show()

  sys.exit(app.exec_())
