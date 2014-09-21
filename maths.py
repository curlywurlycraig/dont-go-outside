import pygame
import math

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
