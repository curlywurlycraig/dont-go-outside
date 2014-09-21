import sys
import pygame
import time
import math

joypads = []

def init():
  global joypads
  joypads = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
  for pad in joypads:
    pad.init()

def get_joypad_count():
  return len( joypads )

def get_stick_direction( pad_number, stick ):
  if stick == 0:
    axis0 = joypads[pad_number].get_axis(0)
    axis1 = joypads[pad_number].get_axis(1)
  elif stick == 1:
    axis0 = joypads[pad_number].get_axis(4)
    axis1 = joypads[pad_number].get_axis(3)

  # Quick fix for divide by 0
  if axis0 == 0: axis0 += 0.01
  if axis1 == 0: axis1 += 0.01

  return math.atan2(axis1, axis0)

def get_stick_magnitude( pad_number, stick ):
  if stick == 0:
    axis0 = joypads[pad_number].get_axis(0)
    axis1 = -joypads[pad_number].get_axis(1)
  elif stick == 1:
    axis0 = joypads[pad_number].get_axis(4)
    axis1 = -joypads[pad_number].get_axis(3)

  result = math.hypot(axis0,axis1)
  if result > 1: result = 1.0

  return result
