import sys
import pygame
import math
import code
import menu

import joystick
from maths import *
from pygame.locals import *

pygame.init()
joystick.init()

BG_COLOR = (0, 0, 50)
SCREEN_DIMENSIONS = (800, 600)
PLAYER1_COLOR = ( 51, 100, 255 )
PLAYER2_COLOR = ( 160, 73, 51 )
TEXT_COLOR = ( 255, 255, 255 )
RETICULE_DISTANCE = 10
PLAY_AREA_COLOR = ( 21, 35, 150 )
PLAY_AREA_RADIUS = 275
BULLET_COLOR = ( 100, 100, 255, 0 )
JOYPAD_CALIBRATION = 10000
MAX_SHOT_SIZE = 30
DEFAULT_SHOT_SIZE = 5
DENSITY = 1
BLOCK_TIME_LIMIT = 500
BLOCK_WINDOW = 200
ARC_DISTANCE = 10


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
pygame.draw.circle(play_area, PLAY_AREA_COLOR, circlepos, PLAY_AREA_RADIUS)

# Define winner screens
font128 = pygame.font.Font("res/Jawbreaker.ttf", 128)
font16 = pygame.font.Font(None, 16)

p1_win = pygame.Surface(SCREEN_DIMENSIONS)
p1_win.set_colorkey( (0,0,0) )
p1_text = font128.render("P1 Wins!", True , TEXT_COLOR)

p2_win = pygame.Surface(SCREEN_DIMENSIONS)
p2_win.set_colorkey( (0,0,0) )
p2_text = font128.render("P2 Wins!", True, TEXT_COLOR)

start_text = font16.render("Press start to continue.", True, TEXT_COLOR)

textpos1 = p1_text.get_rect()
textpos2 = p2_text.get_rect()
startpos = start_text.get_rect()

textpos1.centerx = screen.get_rect().centerx
textpos2.centerx = screen.get_rect().centerx
startpos.centerx = screen.get_rect().centerx

textpos1.centery = 300
textpos2.centery = 300
startpos.centery = 425

p1_win.blit(p1_text, textpos1)
p2_win.blit(p2_text, textpos2)
p1_win.blit(start_text, startpos)
p2_win.blit(start_text, startpos)

# GUI Elements
special_text = font16.render("Blink:", True, TEXT_COLOR)
special_bar_back_1 = pygame.Surface((210, 34))
special_bar_back_1.fill(PLAYER1_COLOR)
special_bar_back_2 = pygame.Surface((210, 34))
special_bar_back_2.fill(PLAYER2_COLOR)
special_bar_empty = pygame.Surface((200, 26))
special_bar_empty.fill((0,84,60))

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
    player1.fire( )

  if joystick.get_joypad_count() > 1:
    if winner==None: player1.force((joystick.get_stick_direction(0,0),joystick.get_stick_magnitude(0,0) * JOYPAD_CALIBRATION * t),1)
    if winner==None: player2.force((joystick.get_stick_direction(1,0),joystick.get_stick_magnitude(1,0) * JOYPAD_CALIBRATION * t),1)

    if (joystick.get_stick_magnitude(0,1) > 0.5):
      if player1.isAlive(): player1.setDirection((joystick.get_stick_direction(0,1)))
    if (joystick.get_stick_magnitude(1,1) > 0.5):
      if player2.isAlive(): player2.setDirection((joystick.get_stick_direction(1,1)))

  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()
    elif event.type == KEYDOWN:
      if event.key == K_ESCAPE:
        sys.exit()
      elif event.key == K_RETURN:
        next_round()
      elif event.key == K_x:
        player2.block()
    elif event.type == JOYBUTTONDOWN:
      if event.button == 7: # Start
        if not (winner == None):
          next_round()
      if event.button == 5: # R1/RB
        if event.joy == 0:
          if player1.isAlive(): player1.startCharging()
        elif event.joy == 1:
          if player2.isAlive(): player2.startCharging()
      elif event.button == 4:
          if event.joy == 0:
            player1.block()
          elif event.joy == 1:
            player2.block()
      elif event.button == 0:
        if event.joy == 0:
          player1.blink(joystick.get_stick_direction(0,0))
        elif event.joy == 1:
          player2.blink(joystick.get_stick_direction(1,0))
    elif event.type == JOYBUTTONUP:
      if event.button == 5: # R1/RB
        if event.joy == 0:
          if player1.isAlive(): player1.fire()
        elif event.joy == 1:
          if player2.isAlive(): player2.fire()




class Player:

  def __init__( self, color, x, y, radius, direction ):
    self.color = color
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.isCharging = False
    self.shotSize = DEFAULT_SHOT_SIZE
    self.radius = radius
    self.direction = direction
    self.alive = True
    self.blocking = False
    self.lastBlock = 0
    self.blockSize = math.pi
    self.boostAmount = 0
    self.hasBlocked = False

  def getBoostAmount(self):
    return self.boostAmount

  def blink( self , angle ):
    if (self.boostAmount >= 25):
      self.boostAmount -= 25
      self.force((angle, 5000),1)

  def block( self ):
    time = pygame.time.get_ticks()

    if time - self.lastBlock > BLOCK_TIME_LIMIT:
      self.blocking = True
      self.lastBlock = pygame.time.get_ticks()

  def kill( self ):
    self.alive = False

  def isAlive( self ):
    return self.alive

  def isBlocking( self ):
    return self.blocking

  def setDirection( self, direction ):
    self.direction = direction

  def getColor( self ):
    return self.color

  def getDirection( self ):
    return self.direction

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
    pygame.draw.circle( player_surface, self.color, ( int(self.radius), int(self.radius) ), int(self.radius) )
    screen.blit( player_surface, (int(self.x - self.radius), int(self.y - self.radius) ) )

    # draw the reticule
    if self.alive:
      reticule_size = self.shotSize
      reticule_surface = pygame.Surface( ( reticule_size, reticule_size ) )
      reticule_surface.set_colorkey( (0,0,0) )
      reticule_pos = cart_from_polar( self.direction, self.radius + RETICULE_DISTANCE + self.shotSize/2, ( self.x, self.y ) )
      reticule_pos = ( int( reticule_pos[0] - reticule_size / 2.0), int( reticule_pos[1] - reticule_size / 2.0 ) )
      pygame.draw.circle( reticule_surface, self.color, ( int( reticule_size / 2 ), int( reticule_size / 2 ) ), int(reticule_size/2) )
      pygame.transform.rotate( reticule_surface, degrees_from_radians( self.direction ) )
      screen.blit( reticule_surface, reticule_pos )

    # blocking
    if self.blocking:
      block_surface = pygame.Surface( ( diameter + ARC_DISTANCE * 2, diameter + ARC_DISTANCE * 2 ) )
      block_surface.set_colorkey( ( 0,0,0) )
      top_left = ( self.x - self.radius - ARC_DISTANCE, self.y - self.radius - ARC_DISTANCE )
      width_height = diameter + ARC_DISTANCE * 2

      # get opacity between 0 and 255
      opacity = 1 - float( pygame.time.get_ticks() - self.lastBlock ) / BLOCK_WINDOW
      opacity = int( opacity * 255 )
      block_surface.set_alpha( opacity )


      arc_start = -1 * self.direction - self.blockSize / 2
      arc_end = -1 * self.direction + self.blockSize / 2
      pygame.draw.arc( block_surface, self.color, pygame.Rect( (0, 0), ( width_height, width_height ) ), arc_start, arc_end, 2 )
      screen.blit( block_surface, top_left )

  # dir is measured in radians as taken from "right"
  def force( self, polar, mass ):
    direction = polar[0]
    magnitude = polar[1]
    self.vy += mass * magnitude * math.sin( direction ) / self.radius
    self.vx += mass * magnitude * math.cos( direction ) / self.radius

  def update( self, t ):
    if not self.alive:
      self.radius -= .2
      if self.radius < 0:
        self.radius = 0
    else:
      self.x += self.vx * t
      self.y += self.vy * t

      self.vx = self.vx / ( 1 + friction * t )
      self.vy = self.vy / ( 1 + friction * t )

      # Grow bullets
      if self.isCharging:
        self.shotSize += 0.1
        if self.shotSize > MAX_SHOT_SIZE:
          self.shotSize = MAX_SHOT_SIZE

      if self.blocking:
        if pygame.time.get_ticks() - self.lastBlock > BLOCK_WINDOW:
          if not self.hasBlocked:
            self.boostAmount -= 10
            if self.boostAmount < 0: self.boostAmount = 0
          self.blocking = False
          self.hasBlocked = False

  def startCharging( self ):
    self.isCharging = True

  def has_blocked( self, mass ):
    self.hasBlocked = True
    self.boostAmount += mass*2
    if self.boostAmount > 100: self.boostAmount = 100

  def fire( self ):
    fire_speed = 500
    mass = self.shotSize

    # play the sound
    sound_strength = int( math.ceil( 4 * ( ( self.shotSize - 5 ) / ( MAX_SHOT_SIZE - 5 ) ) ) )
    if sound_strength == 0:
      sound_strength = 1
    filename = "res/pew" + str( sound_strength ) + ".wav"
    sound = pygame.mixer.Sound( filename )
    sound.play()


    bullet_start_pos = cart_from_polar( self.direction, self.radius + self.shotSize, ( self.x, self.y ))
    bullets.append( Bullet( self, bullet_start_pos, self.direction, fire_speed, mass ) )

    # Reset charging status
    self.shotSize = DEFAULT_SHOT_SIZE
    self.isCharging = False


class Bullet:
  def __init__( self, owner, start_pos, direction, speed, mass ):
    self.owner = owner
    self.x = start_pos[0]
    self.y = start_pos[1]
    velocity = cart_from_polar( direction, speed )
    self.vx = velocity[0]
    self.vy = velocity[1]
    self.mass = mass

  def update( self, t ):
    self.x += self.vx * t
    self.y += self.vy * t

  def getOwner(self):
    return self.owner

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

  def getRadius( self ):
    return self.mass / DENSITY

  def deflect( self, deflector ):
    self.owner = deflector
    direction = deflector.getDirection()
    speed = magnitude_from_cart( self.vx, self.vy )
    velocity = cart_from_polar( direction, speed )
    self.vx = velocity[0]
    self.vy = velocity[1]

  def draw( self ):
    length_scale = 0.5
    size = self.mass / DENSITY
    bullet_surface = pygame.Surface ( ( size, size ) )
    bullet_surface.set_colorkey( (0,0,0) )
    pygame.draw.circle( bullet_surface, self.owner.getColor(), ( int( size / 2 ), int( size / 2 ) ), int( size / 2 ) )

    drawPos = ( self.x - size/2, self.y - size/2 )
    screen.blit( bullet_surface, drawPos )
    updaterects.append( bullet_surface.get_rect())

def next_round():
  global player1
  global player2
  global winner
  global bullets
  screen_pos = screen.get_rect()
  p1x = screen_pos.centerx - 100
  p2x = screen_pos.centerx + 100
  py = screen_pos.centery
  player1 = Player( PLAYER1_COLOR, p1x, py, 20, 0 )
  player2 = Player( PLAYER2_COLOR, p2x, py, 20, math.pi )
  winner = None
  bullets = []

number_of_rounds = 2*menu.draw(screen) + 1
round_count = 1

clock = pygame.time.Clock()

# create the players
screen_pos = screen.get_rect()
p1x = screen_pos.centerx - 100
p2x = screen_pos.centerx + 100
py = screen_pos.centery
player1 = Player( PLAYER1_COLOR, p1x, py, 20, 0 )
player2 = Player( PLAYER2_COLOR, p2x, py, 20, math.pi )
winner = None

# Play Background Music
music_file = "res/music.wav"
music = pygame.mixer.Sound( music_file )
music.set_volume( 0.1 )
music.play(loops=-1)

# Create the GUI Overlay
gui_overlay = pygame.surface.Surface(SCREEN_DIMENSIONS)
gui_overlay.set_colorkey((0,0,0))
while 1:
  t = clock.tick_busy_loop( 60 ) / 1000.0 # measure in seconds

  handle_input( t )

  player1.update( t )
  player2.update( t )

  bullets_for_removal = []
  for bullet in bullets:
    bullet.update( t )

  for bullet in bullets:
    # check for collisions
    if ( math.fabs( bullet.getX() - player1.getX() ) < ( player1.getRadius() + bullet.getRadius() ) and
      math.fabs( bullet.getY() - player1.getY() ) < ( player1.getRadius() + bullet.getRadius() ) ):
      if bullet.getOwner() != player1:
        if player1.isBlocking():
          bullet.deflect( player1 )
          player1.has_blocked(bullet.getMass())
        else:
          player1.force( polar_from_cart( bullet.getVX(), bullet.getVY() ), bullet.getMass() )
          if bullet not in bullets_for_removal:
            bullets_for_removal.append( bullet )

    if ( math.fabs( bullet.getX() - player2.getX() ) < ( player2.getRadius() + bullet.getRadius() ) and
      math.fabs( bullet.getY() - player2.getY() ) < ( player2.getRadius() + bullet.getRadius() ) ):
      if bullet.getOwner() != player2:
        if player2.isBlocking():
          bullet.deflect( player2 )
          player2.has_blocked(bullet.getMass())
        else:
          player2.force( polar_from_cart( bullet.getVX(), bullet.getVY() ), bullet.getMass() )
          if bullet not in bullets_for_removal:
            bullets_for_removal.append( bullet )

    # Kill bullets out of bounds
    if ( bullet.getX() > SCREEN_DIMENSIONS[0] or bullet.getX() < 0
      or bullet.getY() > SCREEN_DIMENSIONS[1] or bullet.getY() < 0 ):
      if bullet not in bullets_for_removal:
        bullets_for_removal.append( bullet )

  for bullet in bullets_for_removal:
    bullets.remove( bullet )

  if winner == None:
    if ((player1.getX() - screen_pos.centerx)**2 + (player1.getY() - screen_pos.centery)**2 > PLAY_AREA_RADIUS**2):
      player1.kill()
      winner = player2
    elif ((player2.getX()-screen_pos.centerx)**2 + (player2.getY() - screen_pos.centery)**2 > PLAY_AREA_RADIUS**2):
      player2.kill()
      winner = player1

  # Generate GUI
  gui_overlay.blit(special_bar_back_1, (25, 540))
  gui_overlay.blit(special_bar_back_2, (565, 540))
  gui_overlay.blit(special_bar_empty, (30, 544))
  gui_overlay.blit(special_bar_empty, (570, 544))

  p1bar = pygame.surface.Surface((player1.getBoostAmount()*2, 26))
  p1bar.fill((0,255,183))
  p2bar = pygame.surface.Surface((player2.getBoostAmount()*2, 26))
  p2bar.fill((0,255,183))

  gui_overlay.blit(p1bar, (30,544))
  gui_overlay.blit(p2bar, (570,544))

  # draw stuff
  screen.blit( bg, (0, 0) )
  screen.blit( play_area, (0, 0) )
  screen.blit( gui_overlay, (0, 0) )
  player1.draw()
  player2.draw()

  for bullet in bullets:
    bullet.draw()

  if winner == player1:
    screen.blit( p1_win, (0, 0) )
  elif winner == player2:
    screen.blit( p2_win, (0, 0) )

  pygame.display.flip()
