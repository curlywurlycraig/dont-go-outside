import sys
import pygame
import math
import code
import joystick
from pygame.locals import *

pygame.init()
#joystick.init()

BG_COLOR = (21, 35, 150)

SCREEN_DIMENSIONS = (1024, 768)
PLAYER_COLOR = ( 51, 73, 160 )
PLAY_AREA_COLOR = ( 0, 0, 50 )
BULLET_COLOR = ( 100, 100, 255, 0 )
DENSITY = 1

screen = pygame.display.set_mode(SCREEN_DIMENSIONS, pygame.HWSURFACE, 16)

# fill background
bg = pygame.Surface(SCREEN_DIMENSIONS)
bg.fill( BG_COLOR )
screen.blit( bg, (0, 0) )
pygame.display.flip()

# Define play area
play_area = pygame.Surface(SCREEN_DIMENSIONS)
play_area.set_colorkey( (0, 0, 0) )
circlepos = (play_area.get_rect().centerx, play_area.get_rect().centery)
pygame.draw.circle(play_area, PLAY_AREA_COLOR, circlepos, 350)


bullets = []

updaterects = []

friction = 1

def handle_input( t ):
  keys = pygame.key.get_pressed()
  if keys[K_DOWN]:
    player1.force( (math.pi / 2, 10000 * t ), 1 )
  if keys[K_UP]:
    player1.force( (math.pi / -2, 10000 * t ), 1 )
  if keys[K_LEFT]:
    player1.force( (math.pi, 10000 * t ), 1 )
  if keys[K_RIGHT]:
    player1.force( (0, 10000 * t ), 1 )
  if keys[K_z]:
    player1.fire( 0 )

  #player1.force((joystick.get_stick_direction(0,0),joystick.get_stick_magnitude(0,0)),5)

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

  def update( self, t ):
    self.x += self.vx * t
    self.y += self.vy * t


    self.vx = self.vx / ( 1 + friction * t )
    self.vy = self.vy / ( 1 + friction * t )

  def fire( self, direction ):
    fire_speed = 500
    mass = 2
    bullet_start_pos = cart_from_polar( direction, self.radius, ( self.x, self.y ))
    bullets.append( Bullet( bullet_start_pos, direction, fire_speed, mass ) )






class Bullet:
  def __init__( self, start_pos, direction, speed, mass ):
    self.x = start_pos[0]
    self.y = start_pos[1]
    velocity = cart_from_polar( direction, speed )
    self.vx = velocity[0]
    self.vy = velocity[1]
    self.mass = mass

  def update( self, t ):
    self.x += self.vx * t
    self.y += self.vy * t

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



clock = pygame.time.Clock()

# create the players
player1 = Player( 20, 100, 20 )
player2 = Player( 400, 100, 20 )

while 1:
  t = clock.tick_busy_loop( 60 ) / 1000.0 # measure in seconds

  handle_input( t )

  player1.update( t )
  player2.update( t )

  for bullet in bullets:
    bullet.update( t )

    # check for collisions
    if ( math.fabs( bullet.getX() - player1.getX() ) < player1.getRadius() and
       math.fabs( bullet.getY() - player1.getY() ) < player1.getRadius() ):
      player1.force( polar_from_cart( bullet.getVX(), bullet.getVY() ), bullet.getMass() )
      bullets.remove( bullet )
      break

    if ( math.fabs( bullet.getX() - player2.getX() ) < player2.getRadius() and
       math.fabs( bullet.getY() - player2.getY() ) < player2.getRadius() ):
      player2.force( polar_from_cart( bullet.getVX(), bullet.getVY() ), bullet.getMass() )
      bullets.remove( bullet )
      break

    # Kill bullets out of bounds
    if ( bullet.getX() > SCREEN_DIMENSIONS[0] or bullet.getX() < 0
      or bullet.getY() > SCREEN_DIMENSIONS[1] or bullet.getY() < 0 ):
      bullets.remove( bullet )
      break

  # draw stuff
  screen.blit( bg, (0, 0) )
  screen.blit( play_area, (0, 0) )
  player1.draw()
  player2.draw()

  for bullet in bullets:
    bullet.draw()

  pygame.display.flip()
