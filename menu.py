import sys
import pygame
import joystick
from pygame.locals import *

# Colour Definitions
bgCol = (0,0,40)
buttonCol = (0,0,150)
fontCol = (255,255,255)
highlightCol = (0,0,200)
buttonPositions = []
menuLocation = 0

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

  return buttonpos

def handle_input( ):
  global menuLocation
  for event in pygame.event.get():
    if event.type == QUIT:
      sys.exit()
    if event.type == KEYDOWN:
      if event.key == K_DOWN:
        menuLocation += 1
      elif event.key == K_UP:
        menuLocation -= 1
      elif event.key == K_RETURN:
        return True
    elif event.type == JOYBUTTONDOWN:
      if event.button == 0:
        return True
    elif event.type == JOYHATMOTION:
      if event.value == (0,1):
        menuLocation -= 1
      if event.value == (0,-1):
        menuLocation += 1

    if menuLocation < 0:
      menuLocation = 0
    if menuLocation > (len(buttonPositions)-1):
      menuLocation = (len(buttonPositions)-1)
  return False

# Returns the button id that is selected by the user.
def draw( screen ):
  # Initialize background and fill with bgCol
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill(bgCol)

  # Initialize and draw title to background
  font = pygame.font.Font("res/Jawbreaker.ttf", 128)
  text = font.render("Don't go Outside!", True , fontCol)
  textpos = text.get_rect()
  textpos.centerx = background.get_rect().centerx
  textpos.top = 200
  background.blit(text,textpos)

  # Make everything but the buttons transparent
  buttons = pygame.Surface(screen.get_size())
  buttons = buttons.convert()
  buttons.fill((0,255,0))
  buttons.set_colorkey((0,255,0))

  # Draw the buttons
  b1 = drawButton(buttons, "Press X to start!", 350)
  global buttonPositions
  buttonPositions = [b1]

  # Draw menu highlight and initalize to first item
  highlight = pygame.Surface((220,40))
  highlight.fill(highlightCol)
  highlightpos = highlight.get_rect()

  while 42:
    if handle_input():
      return menuLocation

    highlightpos.centerx = buttonPositions[menuLocation].centerx
    highlightpos.centery = buttonPositions[menuLocation].centery

    screen.blit(background,(0,0))
    screen.blit(highlight,highlightpos)
    screen.blit(buttons, (0,0))
    pygame.display.flip()
