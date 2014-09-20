import sys
import pygame
import math
import code
from pygame.locals import *

pygame.init()

BG_COLOR = (21, 35, 150)

SCREEN_DIMENSIONS = (640, 480)
PLAYER_COLOR = ( 51, 73, 160 )
BULLET_COLOR = ( 100, 100, 255, 0 )

screen = pygame.display.set_mode(SCREEN_DIMENSIONS, 0, 32)

# fill background
bg = pygame.Surface(SCREEN_DIMENSIONS)
bg.fill( BG_COLOR )
screen.blit( bg, (0, 0) )
pygame.display.flip()

bullets = []


def handle_input():
  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()
    elif event.type == KEYDOWN:
      sys.exit()

def cart_from_polar( theta, distance, offset = (0,0) ):
  x = distance * math.cos( theta )
  y = distance * math.sin( theta )
  result = (x + offset[0], y + offset[0])
  return result

def filled_aacircle( surface, color, pos, radius ):
  aacircle( surface, color, pos, radius - 1)
  aacircle( surface, color, pos, radius )
  aacircle( surface, color, pos, radius + 1)

  pygame.draw.circle( surface, color, pos, radius + 1 )

# use aalines to draw a nice antialiased circle
def aacircle( surface, color, pos, radius, filled=True ):
  points = []
  resolution = 50
  for i in range( resolution ):
    theta = i * ( 2 * math.pi ) / ( resolution )
    point = cart_from_polar( theta, radius, pos )
    points.append( point )

  pygame.draw.aalines( surface, color, True, points, False )

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

  def getX( self ):
    return self.x

  def getY( self ):
    return self.y

  def draw( self ):
    diameter = 2 * self.radius
    player_surface = pygame.Surface( ( diameter, diameter ) )
    player_surface.set_colorkey( (0,0,0) )
    pygame.draw.circle( player_surface, PLAYER_COLOR, ( self.radius, self.radius ), self.radius )
    screen.blit( player_surface, (int(self.x + self.radius), int(self.y + self.radius) ) )

  # dir is measured in radians as taken from "right"
  def force( self, direction, magnitude ):
    self.vy = magnitude * math.sin( direction )
    self.vx = magnitude * math.cos( direction )

  def update( self ):
    self.x += self.vx
    self.y += self.vy

    self.vx = self.vx / 2
    self.vy = self.vy / 2

  def fire( self, direction ):
    fire_speed = 50
    bullet_start_pos = cart_from_polar( direction, fire_speed )
    bullets.append( Bullet( bullet_start_pos, direction, fire_speed ) )


class Bullet:
  def __init__( self, start_pos, direction, magnitude ):
    self.x = start_pos[0]
    self.y = start_pos[1]
    velocity = cart_from_polar( direction, magnitude )
    self.vx = velocity[0]
    self.vy = velocity[1]

  def update( self ):
    self.x += self.vx
    self.y += self.vy

  def draw( self ):
    length_scale = 0.5
    bullet_surface = pygame.Surface ( ( int( self.vx + 3 ), int( self.vy + 3 ) ) )
    bullet_surface.set_colorkey( (0,0,0) )
    pygame.draw.line( bullet_surface, BULLET_COLOR, (self.x, self.y ), (-1 * length_scale * self.vx, -1 * length_scale * self.vy), 3 )
    

    drawPos = ( self.x - self.vx, self.y - self.vy )
    screen.blit( bullet_surface, drawPos )

# create the players
player1 = Player( 10, 10, 20 )
player2 = Player( 100, 10, 20 )

player1.fire( math.pi / 4.0 )


while 1:
  handle_input()

  player1.update()
  player2.update()

  for bullet in bullets:
    bullet.update()

  # draw stuff
  bg = pygame.Surface(SCREEN_DIMENSIONS)
  bg.fill( BG_COLOR )
  screen.blit( bg, (0, 0) )
  player1.draw()
  player2.draw()

  for bullet in bullets:
    bullet.draw()

  pygame.display.flip()
