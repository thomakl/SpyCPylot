'''
CURRENT CONTROLS:

0 - Quit
WASD - Drive/Turn
J - Camera Up
K - Camera Down
SPACE - Take a Picture


NOTES:

There are a couple limits to mobility with the current algorithm:

1. It cannot turn while moving forward/backward. This is due to 
	pygame, and we should be able to incorporate better turning soon.
2. It stops moving after about 4 or 5 wheel rotations, so you have to 
    press the directional button again for longer movements. However, it
    will stop if you let go earlier.

'''
from datetime import date
from random import choice
from string import ascii_lowercase, ascii_uppercase

import pygame
from pygame.locals import *

from rover import Rover20


# must be in interval [-1,1] (vals < 1 yield slower speeds)
MAX_TREAD_SPEED = 1

class KeyboardRover20(Rover20):
	def __init__(self):
		Rover20.__init__(self)	
		
		self.quit = False
				
		# window must be open and in focus for pygame to take input
		self.windowSize = [640, 480]
		
		# used to only refresh the video and not the unused pixels
		self.imageRect = (0,0,320,240)
		
		# Live video frames per second
		self.fps = 24
		
		# stores what the camera currently sees
		self.currentImage = None
				
		pygame.init()
		pygame.display.init()
		
		self.displayCaption = "Keyboard Rover 2.0 | PRESS 0 to QUIT"
		pygame.display.set_caption(self.displayCaption)
		
		self.screen = pygame.display.set_mode(self.windowSize)
		self.clock = pygame.time.Clock()
	
		
	# automagically called by Rover20, overriden to add functionality
	def processVideo(self, jpegbytes, timestamp_10msec):						
			self.currentImage = jpegbytes
			self.parseControls()
			
			#prevents an inconsequential error on quit
			if not self.quit:													
				self.refreshVideo()
	
	
	def parseControls(self):
		for event in pygame.event.get():			
			
			if event.type == KEYDOWN:
				# movement
				if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
					self.updateTreadState(event.key)			
				# camera
				if event.key in (pygame.K_j, pygame.K_k, pygame.K_SPACE):
					self.updateCameraState(event.key)
				# quit								
				if event.key is pygame.K_0:	
					self.quit = True
			
			if event.type == KEYUP:
				# movement
				if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
					self.updateTreadState()
				# camera
				if event.key in (pygame.K_j, pygame.K_k):
					self.updateCameraState()
	
	
	# live video feed										
	def refreshVideo(self):
		self.takePicture('tmp.jpg')
		
		#load image, update display
		image = pygame.image.load('tmp.jpg').convert()		
		self.screen.blit(image, (0, 0))
		pygame.display.update(self.imageRect)
		
		#limit fps
		self.clock.tick(self.fps) 
	
	
	# move rover								
	def updateTreadState(self, key=None):
		if key is None:
			self.setTreads(0,0)
		if key is pygame.K_w:
			self.setTreads(MAX_TREAD_SPEED, MAX_TREAD_SPEED)
		if key is pygame.K_a:
			self.setTreads(-MAX_TREAD_SPEED, MAX_TREAD_SPEED)
		if key is pygame.K_s:
			self.setTreads(-MAX_TREAD_SPEED, -MAX_TREAD_SPEED)
		if key is pygame.K_d:
			self.setTreads(MAX_TREAD_SPEED, -MAX_TREAD_SPEED)
	
	
	# move camera and take pictures
	def updateCameraState(self, key=None):
		if key is None:
			self.moveCameraVertical(0)
		if key is pygame.K_j:
			self.moveCameraVertical(1)
		if key is pygame.K_k:
			self.moveCameraVertical(-1)
		if key is pygame.K_SPACE:
			self.takePicture(self.newPictureName())
	
	
	# save jpegbytes to file
	def takePicture(self, fname):
		fd = open(fname, 'w')
		fd.write(self.currentImage)
		fd.close()
		
				
	# returns today's date plus a random string of letters
	def newPictureName(self):
		todaysDate = str(date.today())
		uniqueKey = ''.join(choice(ascii_lowercase + ascii_uppercase) \
							for _ in range(7))
		return todaysDate+'_'+uniqueKey+'.jpg'
		
		
			
def main():	
	rover = KeyboardRover20()
	
	while not rover.quit:
		pass
	
	pygame.quit()
	rover.close()
	

			
if __name__ == '__main__':
	main()	
		
