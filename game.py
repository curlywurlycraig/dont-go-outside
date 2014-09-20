import sys
import pygame
import math
import code
from pygame.locals import *

pygame.init()

BG_COLOR = (0, 89, 150)

SCREEN_DIMENSIONS = (640, 480)
PLAYER_COLOR = ( 71, 99, 209 )

screen = pygame.display.set_mode(SCREEN_DIMENSIONS, 0, 32)

# fill background
bg = pygame.Surface(SCREEN_DIMENSIONS)
bg.fill( BG_COLOR )
screen.blit( bg, (0, 0) )
pygame.display.flip()

def handle_input():
  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()
    elif event.type == KEYDOWN:
      sys.exit()

def cart_from_polar( theta, distance, offset ):
  x = distance * math.cos( theta )
  y = distance * math.sin( theta )
  result = [x + offset[0], y + offset[0]]
  return result

# use aalines to draw a nice antialiased circle
def aacircle( surface, color, pos, radius ):
  points = []
  resolution = 50
  for i in range( resolution ):
    theta = i * ( 2 * math.pi ) / ( resolution )
    point = cart_from_polar( theta, radius, pos )
    points.append( point )

  pygame.draw.aalines( surface, color, True, points, 1 )
  pygame.draw.circle( surface, color, pos, radius - 1 )

class Player:
  def __init__( self, x, y, radius ):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.radius = radius

  def setPos( self, x, y ):
    self.x = x
    self.y = y

  def draw( self ):
    diameter = 2 * self.radius
    player_surface = pygame.Surface( ( diameter, diameter ) )
    aacircle( player_surface, PLAYER_COLOR, ( self.x, self.y ), self.radius )
    screen.blit( player_surface, (int(self.x), int(self.y) ) )

  # dir is measured in radians as taken from "right"
  def force( self, direction, magnitude ):
    self.vy = magnitude * math.sin( direction )
    self.vx = magnitude * math.cos( direction )

  def update( self ):
    self.x += self.vx
    self.y += self.vy

    self.vx = self.vx / 2
    self.vy = self.vy / 2

# create the players
player1 = Player( 10, 10, 20 )
player2 = Player( 50, 10, 20 )

while 1:
  handle_input()

  player1.update()
  player2.update()

  # draw stuff
  bg = pygame.Surface(SCREEN_DIMENSIONS)
  bg.fill( BG_COLOR )
  screen.blit( bg, (0, 0) )
  player1.draw()
  player2.draw()
  pygame.display.flip()
