import sys
import pygame
from pygame.locals import *

pygame.init()

BG_COLOR = (0, 89, 150)

SCREEN_DIMENSIONS = (640, 480)

screen = pygame.display.set_mode(SCREEN_DIMENSIONS, 0, 32)

# fill background
bg = pygame.Surface(SCREEN_DIMENSIONS)
bg.fill( BG_COLOR )
screen.blit( bg, (0, 0) )
pygame.display.flip()

def handle_input():
  for event in pygame.event.get():
    if event.type in (QUIT, KEYDOWN):
      sys.exit()

class Player:
  def __init__( self ):

  def setHP( self, hp ):
    self.hp = hp

  def setPos( self, x, y ):
    self.x = x
    self.y = y

  def draw( self, surface ):


while 1:
  handle_input()

  # draw stuff
  bg = pygame.Surface(SCREEN_DIMENSIONS)
  bg.fill( BG_COLOR )
  screen.blit( bg, (0, 0) )
