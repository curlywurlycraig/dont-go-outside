import sys
import pygame
from pygame.locals import *

# Colour Definitions
bgCol = (20,20,20)
buttonCol = (100,100,100)
fontCol = (255,255,255)

def drawButton ( surface, string, y ):
  # Create and position the button
  button = pygame.Surface((200, 40))
  button.convert()
  button.fill(buttonCol)
  buttonpos = button.get_rect()
  buttonpos.centerx = surface.get_rect().centerx
  buttonpos.centery = y

  # Create and position the text
  font = pygame.font.Font(None, 18)
  text = font.render(string, True, fontCol)
  textpos = text.get_rect()
  textpos.centerx = buttonpos.centerx
  textpos.centery = buttonpos.centery

  # Draw button and text to surface
  surface.blit(button,buttonpos)
  surface.blit(text,textpos)

def handle_input( ):
  for event in pygame.event.get():
    if event.type in (QUIT, KEYDOWN):
      return True
  return False

def draw( screen ):
  # Initialize background and fill with bgCol
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill(bgCol)

  # Initialize and draw title to background
  font = pygame.font.Font(None, 64)
  text = font.render("Don't go Outside!", True , fontCol)
  textpos = text.get_rect()
  textpos.centerx = background.get_rect().centerx
  textpos.top = 100
  background.blit(text,textpos)

  # Draw a button
  drawButton(background, "Singleplayer", 200)
  drawButton(background, "Multiplayer", 250)
  drawButton(background, "Scores", 300)

  while 42:
    if handle_input():
      break

    screen.blit(background,(0,0))
    pygame.display.flip()
