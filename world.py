import numpy as np
import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
from config import *

class World(object):
  def initWorld(self):
    self.cubeVtxArray = np.array([
      [-1.0, -1.0, -1.0],
      [1.0, -1.0, -1.0],
      [1.0, -1.0, 1.0],
      [-1.0, -1.0, 1.0]]) * WORLD_SCALER

    self.cubeIdxArray = np.array( [0,1,2, 2,3,0 ])
    self.outlineVtx = np.array((
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )) * WORLD_SCALER

    self.outlineEdges =(
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

  def update(self):
    gl.glBegin(gl.GL_LINES)
    for edge in self.outlineEdges:
      for point in edge:
        gl.glColor3d(0,1,0)
        gl.glVertex3fv(self.outlineVtx[point])
    gl.glEnd()

    gl.glBegin(gl.GL_QUADS)
    gl.glColor3d(200/255, 207/255, 0)
    for vert in self.cubeVtxArray:
      gl.glVertex3fv(vert)
    gl.glEnd()

