import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
import sys # we'll need this later to run our Qt application
import pickle

from OpenGL.arrays import vbo
import numpy as np

#TODO: Figure out how to capture multiple viewports


# This is just a dummy class to play around with random position updates in OpenGL for
# creatures' hitboxes. It will be renamed or completely removed once the final version
# has been completed
# class Creature(object):
#   def __init__(self, pos, size):
#     self.pos = pos
#     self.size = size

# The actual creature class that will be used in a later version of the simulation
class Creature(object):
  def __init__(self, size, pos, pitch=None, yaw=None, genomes=None):
    self.genomes = genomes
    self.pos = pos
    self.size = size
    self.pitch = 0
    self.yaw = 0
    self.roll = 0
    # self.age = age
    # self.hitbox = np.array([
    #   [self.pos[0] - (self.size/2), self.pos[1] - (self.size/2), self.pos[2] - (self.size/2)], # 0,0
    #   [self.pos[0] + (self.size/2), self.pos[1] - (self.size/2), self.pos[2] - (self.size/2)], # 0,1
    #   [self.pos[0] + (self.size/2), self.pos[1] - (self.size/2), self.pos[2] + (self.size/2)], # 0,2
    #   [self.pos[0] - (self.size/2), self.pos[1] - (self.size/2), self.pos[2] + (self.size/2)], # 0,3
    #   [self.pos[0] - (self.size/2), self.pos[1] + (self.size/2), self.pos[2] - (self.size/2)], # 1,0
    #   [self.pos[0] + (self.size/2), self.pos[1] + (self.size/2), self.pos[2] - (self.size/2)], # 1,1
    #   [self.pos[0] + (self.size/2), self.pos[1] + (self.size/2), self.pos[2] + (self.size/2)], # 1,2
    #   [self.pos[0] - (self.size/2), self.pos[1] + (self.size/2), self.pos[2] + (self.size/2)], # 1,3
    # ])

    self.hitbox = np.array([
      [-(self.size/2), -(self.size/2),-(self.size/2)], # 0,0
      [(self.size/2), -(self.size/2),-(self.size/2)], # 0,1
      [(self.size/2), -(self.size/2),(self.size/2)], # 0,2
      [-(self.size/2), -(self.size/2),(self.size/2)], # 0,3
      [-(self.size/2), (self.size/2),-(self.size/2)], # 1,0
      [(self.size/2), (self.size/2),-(self.size/2)], # 1,1
      [(self.size/2), (self.size/2),(self.size/2)], # 1,2
      [-(self.size/2),(self.size/2),(self.size/2)] # 1,3
    ]) + self.pos

    self.hitboxVBO = vbo.VBO(np.reshape(self.hitbox,
    (1, -1)).astype(np.float32)) 

    self.hitbox_edges = np.array([
      [0,1], [0,3], [0,4],
      [1,5], [1,2],
      [2, 3], [2, 6],
      [3, 7],
      [4, 5], [4, 7],
      [5, 6],
      [6, 7]
    ])

    self.faces = (
      0,1,2,3,
      0,1,5,4,
      1,2,6,5,
      3,0,4,7,
      2,3,6,7,
      4,5,6,7,
    )

    self.t_faces = (
      0,1,2,
      1,2,3, # bottom
      0,1,4,
      1,5,4, # front 
      1,2,5,
      2,6,5, # right 
      0,3,7,
      0,4,7, # left
      4,5,7,
      5,6,7, # top
      3,2,7,
      2,6,7,
    )

    self.look_vec= np.array([
      [0, 0 ,-(self.size)/2],
      [0, 0,-1.5*(self.size)]
      ]) + self.pos# 0,0

    self.lookVBO = vbo.VBO(np.reshape(self.look_vec,
    (1, -1)).astype(np.float32))


  def move(self, vec):
    # self.unbind_vbos()
    self.pos += vec
    self.hitbox += self.pos
    self.look_vec += self.pos
    self.hitboxVBO = vbo.VBO(np.reshape(self.hitbox,
    (1, -1)).astype(np.float32))
    self.hitboxVBO.bind()

    self.lookVBO = vbo.VBO(np.reshape(self.look_vec,
    (1, -1)).astype(np.float32))

  def forward_thrust(self, mag):
    self.pos += self.pitch

  def rotate(self, pitch, yaw, roll):
    # self.unbind_vbos()
    # We translate the creature to the origin, and rotate it about the base coordinate axes
    self.hitbox = np.array([
      [-(self.size/2), -(self.size/2),-(self.size/2)], # 0,0
      [(self.size/2), -(self.size/2),-(self.size/2)], # 0,1
      [(self.size/2), -(self.size/2),(self.size/2)], # 0,2
      [-(self.size/2), -(self.size/2),(self.size/2)], # 0,3
      [-(self.size/2), (self.size/2),-(self.size/2)], # 1,0
      [(self.size/2), (self.size/2),-(self.size/2)], # 1,1
      [(self.size/2), (self.size/2),(self.size/2)], # 1,2
      [-(self.size/2),(self.size/2),(self.size/2)] # 1,3
    ])

    self.look_vec= np.array([
      [0, 0 ,-(self.size)/2],
      [0, 0,-1.5*(self.size)]
      ]) 

    # pitch rotation matrix
    self.pitch += pitch
    self.yaw += yaw
    self.roll += roll
    R_x = np.array([
      [1, 0, 0],
      [0, np.cos(self.pitch), -np.sin(self.pitch)],
      [0, np.sin(self.pitch), np.cos(self.pitch)]
    ])

    # yaw rotation matrix
    R_y = np.array([
      [np.cos(self.yaw), 0, np.sin(self.yaw)],
      [0, 1, 0],
      [-np.sin(self.yaw), 0, np.cos(self.yaw)]
    ])

    # roll rotation matrix
    R_z = np.array([
      [np.cos(self.roll), -np.sin(self.roll), 0],
      [np.sin(self.roll), np.cos(self.roll), 0],
      [0, 0, 1]
    ])

    # Apply rotation matrices and translate them back their original position
    self.hitbox = np.array([np.dot(np.dot(np.dot(R_x, vert), R_y), R_z) for vert in self.hitbox])
    self.hitbox = self.hitbox + self.pos 
    self.look_vec = np.array([np.dot(np.dot(np.dot(R_x, vert), R_y), R_z) for vert in self.look_vec])
    self.look_vec = self.look_vec + self.pos 
  
    self.hitboxVBO = vbo.VBO(np.reshape(self.hitbox,
    (1, -1)).astype(np.float32))
    self.hitboxVBO.bind()

    self.lookVBO = vbo.VBO(np.reshape(self.look_vec,
    (1, -1)).astype(np.float32))

    

def give_birth(c1:Creature, c2:Creature) -> Creature:
  pass
    

# def spawn_creature():



# genomes = {size:, m_rate:, }
