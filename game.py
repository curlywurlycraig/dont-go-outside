import sys
import pygame
import math
import code
import joystick
from pygame.locals import *

pygame.init()

BG_COLOR = (21, 35, 150)

SCREEN_DIMENSIONS = (640, 480)
PLAYER_COLOR = ( 51, 73, 160 )
BULLET_COLOR = ( 100, 100, 255, 0 )
DENSITY = 0.25

screen = pygame.display.set_mode(SCREEN_DIMENSIONS, 0, 32)

# fill background
bg = pygame.Surface(SCREEN_DIMENSIONS)
bg.fill( BG_COLOR )
screen.blit( bg, (0, 0) )
pygame.display.flip()

bullets = []

updaterects = []

friction = 1.01

def handle_input():
  keys = pygame.key.get_pressed()
  if keys[K_DOWN]:
    player1.force( (math.pi / 2, 10 ), 3 )
  if keys[K_UP]:
    player1.force( (math.pi / -2, 10 ), 3 )
  if keys[K_LEFT]:
    player1.force( (math.pi, 10 ), 3 )
  if keys[K_RIGHT]:
    player1.force( (0, 10 ), 3 )
  if keys[K_z]:
    player1.fire( 0 )

  player1.force((joystick.get_stick_direction(0,0),joystick.get_stick_magnitude(0,0)),5)

  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()
    elif event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        sys.exit()

def cart_from_polar( theta, distance, offset = (0,0) ):
  x = distance * math.cos( theta )
  y = distance * math.sin( theta )
  result = (x + offset[0], y + offset[1])
  return result

def polar_from_cart( x, y ):
  return ( direction_from_cart( x, y ), magnitude_from_cart( x, y ) )

def direction_from_cart( x, y ):
  return math.atan2( y, x )

def magnitude_from_cart( x, y ):
  return math.sqrt( x * x + y * y )

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

  def move( self, x, y ):
    self.x += x
    self.y += y

  def getX( self ):
    return self.x

  def getY( self ):
    return self.y

  def getRadius( self ):
    return self.radius

  def draw( self ):
    diameter = 2 * self.radius
    player_surface = pygame.Surface( ( diameter, diameter ) )
    player_surface.set_colorkey( (0,0,0) )
    pygame.draw.circle( player_surface, PLAYER_COLOR, ( self.radius, self.radius ), self.radius )
    screen.blit( player_surface, (int(self.x - self.radius), int(self.y - self.radius) ) )

    updaterects.append( player_surface.get_rect())

  # dir is measured in radians as taken from "right"
  def force( self, polar, mass ):
    direction = polar[0]
    magnitude = polar[1]
    self.vy += mass * magnitude * math.sin( direction ) / self.radius
    self.vx += mass * magnitude * math.cos( direction ) / self.radius

  def update( self ):
    self.x += self.vx
    self.y += self.vy

    self.vx = self.vx / friction
    self.vy = self.vy / friction

  def fire( self, direction ):
    fire_speed = 30
    mass = 1
    bullet_start_pos = cart_from_polar( direction, fire_speed, ( self.x, self.y ))
    bullets.append( Bullet( bullet_start_pos, direction, fire_speed, mass ) )






class Bullet:
  def __init__( self, start_pos, direction, speed, mass ):
    self.x = start_pos[0]
    self.y = start_pos[1]
    velocity = cart_from_polar( direction, speed )
    self.vx = velocity[0]
    self.vy = velocity[1]
    self.mass = mass

  def update( self ):
    self.x += self.vx
    self.y += self.vy

  def getX( self ):
    return self.x

  def getY( self ):
    return self.y

  def getVX( self ):
    return self.vx

  def getVY( self ):
    return self.vy

  def getMass( self ):
    return self.mass

  def draw( self ):
    length_scale = 0.5
    size = self.mass / DENSITY
    bullet_surface = pygame.Surface ( ( size, size ) )
    bullet_surface.set_colorkey( (0,0,0) )
    pygame.draw.circle( bullet_surface, BULLET_COLOR, ( int( size / 2 ), int( size / 2 ) ), int( size / 2 ) )
    #pygame.draw.line( bullet_surface, BULLET_COLOR, (self.x, self.y ), (-1 * length_scale * self.vx, -1 * length_scale * self.vy), 3 )

    drawPos = ( self.x, self.y )
    screen.blit( bullet_surface, drawPos )
    updaterects.append( bullet_surface.get_rect())




joystick.init()
clock = pygame.time.Clock()

# create the players
player1 = Player( 20, 100, 20 )
player2 = Player( 400, 100, 20 )

while 1:
  handle_input()

  player1.update()
  player2.update()

  for bullet in bullets:
    bullet.update()

  # check for collisions
  for bullet in bullets:
    if ( math.fabs( bullet.getX() - player1.getX() ) < player1.getRadius() and
       math.fabs( bullet.getY() - player1.getY() ) < player1.getRadius() ):
      player1.force( polar_from_cart( bullet.getVX(), bullet.getVY() ), bullet.getMass() )
      bullets.remove( bullet )

    if ( math.fabs( bullet.getX() - player2.getX() ) < player2.getRadius() and
       math.fabs( bullet.getY() - player2.getY() ) < player2.getRadius() ):
      player2.force( polar_from_cart( bullet.getVX(), bullet.getVY() ), bullet.getMass() )
      bullets.remove( bullet )

  # draw stuff
  screen.blit( bg, (0, 0) )
  player1.draw()
  player2.draw()

  for bullet in bullets:
    bullet.draw()

  pygame.display.flip()
  clock.tick_busy_loop(60)
