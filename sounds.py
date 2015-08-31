import glob
import os
import pygame
import random

pygame.init()


def get_taunts(path='./sounds'):
	return glob.glob(os.path.join(path, '*.wav'))

class Taunter(object):

	def __init__(self, taunts=get_taunts()):
		self.taunts = taunts

	def taunt(self):
		taunt = random.choice(self.taunts)
		print 'playing %s' % taunt
		pygame.mixer.music.load(taunt)
		pygame.mixer.music.play()
