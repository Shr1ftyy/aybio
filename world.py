import numpy as np
import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
from config import *
import random as r

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
    self.energy_sources = []

  def update(self):
    gl.glLineWidth(1.0)
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

    self.growFood()

    if len(self.energy_sources) != 0:
      gl.glColor3d(0, 117/255, 14/255)
      gl.glBegin(gl.GL_QUADS)
      for e in self.energy_sources:
        for vert in e.faces:
          gl.glVertex3fv(e.hitbox[vert])
      gl.glEnd()


  def growFood(self):
    if len(self.energy_sources)<=100 and r.random() <= 0.1:
      pos = np.array([r.randint(-150, 150), -200, r.randint(-150, 150)])
      size = r.randrange(2, 8, 1)
      f = EnergySource(pos, size, size)
      self.energy_sources.append(f)

class EnergySource(object):
  def __init__(self, pos, size, energy) -> None:
    self.pos = pos
    self.size = size
    self.energy = energy # need to change -> energy should be based on min, max and more spawning conditions
    self.hitbox = np.array([
      [self.pos[0] - (self.size/2), self.pos[1] - (self.size/2), self.pos[2] - (self.size/2)], # 0,0
      [self.pos[0] + (self.size/2), self.pos[1] - (self.size/2), self.pos[2] - (self.size/2)], # 0,1
      [self.pos[0] + (self.size/2), self.pos[1] - (self.size/2), self.pos[2] + (self.size/2)], # 0,2
      [self.pos[0] - (self.size/2), self.pos[1] - (self.size/2), self.pos[2] + (self.size/2)], # 0,3
      [self.pos[0] - (self.size/2), self.pos[1] + (self.size/2), self.pos[2] - (self.size/2)], # 1,0
      [self.pos[0] + (self.size/2), self.pos[1] + (self.size/2), self.pos[2] - (self.size/2)], # 1,1
      [self.pos[0] + (self.size/2), self.pos[1] + (self.size/2), self.pos[2] + (self.size/2)], # 1,2
      [self.pos[0] - (self.size/2), self.pos[1] + (self.size/2), self.pos[2] + (self.size/2)], # 1,3
    ]) + [0, (self.size)/2, 0]

    self.faces = (
      0,1,2,3,
      0,1,5,4,
      1,2,6,5,
      3,0,4,7,
      2,3,6,7,
      4,5,6,7,
    )