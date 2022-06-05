from PyQt5 import QtCore # core Qt functionality, QtWidgets
# from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
# from PyQt5 import QtOpenGL # provides QGLWidget, QtWidgets,a special OpenGL QWidget)
from PyQt5 import QtWidgets
import OpenGL.GL as gl # python wrapping of OpenGL
import OpenGL.GLUT as glut # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
import sys # we'll need this later to run our Qt application
import random as r
from datetime import datetime

from world import World
from creatures import Creature
from config import *

from OpenGL.arrays import vbo
import numpy as np

class GLWidget(QtWidgets.QOpenGLWidget):
  def __init__(self, parent=None):
    QtWidgets.QOpenGLWidget.__init__(self, parent)
    self.world = World()
    self.FPS = 0
    self.parent = parent

  def initializeGL(self):
    gl.glClearColor(1/255, 100/255, 128/255, 1) # initialize the screen to blue
    gl.glEnable(gl.GL_DEPTH_TEST) # enable depth testing

    self.world.initWorld()
    self.initCreatures()

    self.rotX = INIT_ROT_X 
    self.rotY = INIT_ROT_Y
    self.rotZ = INIT_ROT_Z
    self.zoom = ZOOM_SCALE
    self.t = 0 

  def resizeGL(self, width, height):
    gl.glViewport(0, 0, width, height)
    # gl.glMatrixMode(gl.GL_PROJECTION)
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

    self.world.update()
    self.updateLife()
    # width, height = gl.glGetIntegerv(gl.GL_VIEWPORT)[-2], gl.glGetIntegerv(gl.GL_VIEWPORT)[-1]
    # frame = gl.glReadPixels(0, 0, height, width, gl.GL_BGR, gl.GL_FLOAT)
    # cv2.imshow('frame', frame)
    self.t += 1
    time_passed = datetime.now() - self.start_time
    # print(time_passed.microseconds/1000)
    self.FPS = 1000.0/(time_passed.microseconds/1000)
    self.parent.fps_counter.setText(str(int(self.FPS)) + ' FPS')
    gl.glPopMatrix() # restore the previous modelview matrix

  def updateLife(self):
    for creature in self.creatures:
      gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
      creature.move(np.array([r.randint(-1,1), r.randint(-1,1), r.randint(-1,1)]))
      # # creature.move(np.array([1,0,0]))
      creature.rotate(pitch=np.pi/160, yaw=0, roll=np.pi/160)
      gl.glLineWidth(2.0)
      gl.glColor3d(1,0,1)
      creature.hitboxVBO.bind()
      gl.glVertexPointer(3, gl.GL_FLOAT, 0, creature.hitboxVBO)
      gl.glDrawElements(gl.GL_LINES, 24, gl.GL_UNSIGNED_INT, creature.hitbox_edges)

      gl.glColor3d(0.75,0,0)
      gl.glDrawElements(gl.GL_QUADS, 24, gl.GL_UNSIGNED_INT, creature.faces)
      creature.hitboxVBO.unbind()

      gl.glLineWidth(1.0)
      gl.glColor3d(0, 0, 0)
      creature.lookVBO.bind()
      gl.glVertexPointer(3, gl.GL_FLOAT, 0, creature.lookVBO)
      gl.glDrawElements(gl.GL_LINES, 2, gl.GL_UNSIGNED_INT, np.array([0,1]))
      gl.glDisableClientState(gl.GL_VERTEX_ARRAY)  
      creature.lookVBO.unbind()


  def initCreatures(self):
    minSize = 1
    maxSize = 15
    self.creatures = []
    for i in range(NUM_CREATURES):
      # moves = np.array([[r.randint(-1,1), r.randint(-1,1), r.randint(-1,1)] for i in range(1000)])
      init_pos = np.array([r.randint(-150, 150), r.randint(-150, 150), r.randint(-150, 150)])
      size = 3 + r.random()*(maxSize - minSize)
      # c = Creature(init_pos, moves, size)
      c = Creature(pos=init_pos, size=size)
      self.creatures.append(c)

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
    timer.timeout.connect(self.glWidget.update)
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
