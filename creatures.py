import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
import sys # we'll need this later to run our Qt application
import pickle

from OpenGL.arrays import vbo
import numpy as np


# This is just a dummy class to play around with random position updates in OpenGL for
# creatures' hitboxes. It will be renamed or completely removed once the final version
# has been completed
class Creature(object):
  def __init__(self, pos, moves, size):
    self.pos = pos
    self.moves = moves
    self.size = size

# The actual creature class that will be used in the simulation
class Creaturev2(object):
  def __init__(self, moves, size, spawn_pos=(0,0), genomes=None):
    self.genomes = genomes
    self.spawn_pos = spawn_pos
    self.moves
    self.size = size

def give_birth(c1:Creature, c2:Creature) -> Creature:
  pass
    

# def spawn_creature():



# genomes = {size:, m_rate:, }
