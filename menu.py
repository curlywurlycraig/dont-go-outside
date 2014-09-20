import sys
import pygame
from pygame.locals import *

# Colour Definitions
bgCol = (20,20,20)
buttonCol = (100,100,100)
fontCol = (255,255,255)
highlightCol = (200,200,200)
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
    if event.type == KEYDOWN:
      if event.key == K_DOWN:
        menuLocation += 1
        if menuLocation > (len(buttonPositions)-1):
          menuLocation = (len(buttonPositions)-1)
      elif event.key == K_UP:
        menuLocation -= 1
        if menuLocation < 0:
          menuLocation = 0
      elif event.key == K_RETURN:
        return True
  return False

# Returns the button id that is selected by the user.
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

  # Make everything but the buttons transparent
  buttons = pygame.Surface(screen.get_size())
  buttons = buttons.convert()
  buttons.fill((0,255,0))
  buttons.set_colorkey((0,255,0))

  # Draw the buttons
  b1 = drawButton(buttons, "Singleplayer", 200)
  b2 = drawButton(buttons, "Multiplayer", 250)
  b3 = drawButton(buttons, "Scores", 300)
  global buttonPositions
  buttonPositions = [b1,b2,b3]

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
