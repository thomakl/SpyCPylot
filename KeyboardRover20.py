'''
CONTROLS:

WASD - Drive
SPACE - Take Picture

J - Camera Up
K - Camera Down

U - Toggle Infrared
I - Toggle Lights

'''
from datetime import date
from random import choice
from string import ascii_lowercase, ascii_uppercase
import StringIO

import pygame
from pygame.locals import *

from rover import Rover20



class KeyboardRover20(Rover20):
	def __init__(self):
		Rover20.__init__(self)

		self.quit = False

		self.lightsAreOn = False
		self.stealthIsOn = False

		# each integer may be -1, 0, or 1
		self.treads = [0,0]

		# window must be open and in focus for pygame to take input
		self.windowSize = [640, 480]

		# used to only refresh the video and not the unused pixels
		self.imageRect = (160,120,320,240)

		# Live video frames per second
		self.fps = 48

		# stores what the camera currently sees
		self.currentImage = None

		self.displayCaption = "Keyboard Rover 2.0"

		pygame.init()
		pygame.display.init()
		pygame.display.set_caption(self.displayCaption)

		self.screen = pygame.display.set_mode(self.windowSize)
		self.clock = pygame.time.Clock()


	# automagically called by Rover20, acts as main loop
	def processVideo(self, jpegbytes, timestamp_10msec):
			if not self.quit:
				self.currentImage = StringIO.StringIO(jpegbytes)
				self.refreshVideo()
				self.parseControls()
				self.setTreads(self.treads[0], self.treads[1])
			
				
	def parseControls(self):
		for event in pygame.event.get():

			if event.type == QUIT:
				self.quit = True

			elif event.type == KEYDOWN:
				# camera
				if event.key in (K_j, K_k, K_SPACE):
					self.updateCameraState(event.key)

				# drive
				elif event.key in (K_w, K_a, K_s, K_d):
					self.updateTreadState(event.key)

				# infrared
				elif event.key is K_u:
					self.stealthIsOn = not self.stealthIsOn
					if self.stealthIsOn:
						self.turnStealthOn()
					else:
						self.turnStealthOff()

				# lights
				elif event.key is K_i:
					self.lightsAreOn = not self.lightsAreOn
					if self.lightsAreOn:
						self.turnLightsOn()
					else:
						self.turnLightsOff()

			elif event.type == KEYUP:
				# drive
				if event.key in (K_w, K_a, K_s, K_d):
					self.updateTreadState()
				# camera
				elif event.key in (K_j, K_k):
					self.updateCameraState()
				else:
					pass
			else:
				pass


	# live video feed
	def refreshVideo(self):
		

		#load image, update display
		image = pygame.image.load(self.currentImage).convert()
		self.currentImage.close()
		self.screen.blit(image, (160, 120))
		pygame.display.update(self.imageRect)

		#limit fps
		self.clock.tick(self.fps)


	# move rover
	def updateTreadState(self, key=None):

		if key is None:
			self.treads = [0,0]
		elif key is K_w:
			self.treads = [1,1]
		elif key is K_s:
			self.treads = [-1,-1]
		elif key is K_a:
			self.treads = [-1,1]
		elif key is K_d:
			self.treads = [1,-1]
		else:
			pass


	# move camera and take pictures
	def updateCameraState(self, key=None):
		# stationary
		if key is None:
			self.moveCameraVertical(0)
		# up
		elif key is pygame.K_j:
			self.moveCameraVertical(1)
		# down
		elif key is pygame.K_k:
			self.moveCameraVertical(-1)
		# take picture
		elif key is pygame.K_SPACE:
			# FIX THIS
			pass
			#self.takePicture(self.newPictureName())
		else:
			pass


	# save jpegbytes to file
	def takePicture(self, fname):
		with open(fname, 'w') as fd:
			fd.write(self.currentImage.getvalue())


	# today's date plus a random string of letters
	def newPictureName(self):
		todaysDate = str(date.today())
		uniqueKey = ''.join(choice(ascii_lowercase + ascii_uppercase) \
							for _ in range(4))
		return todaysDate+'_'+uniqueKey+'.jpg'



def main():

	rover = KeyboardRover20()

	while not rover.quit:
		pass

	rover.close()


if __name__ == '__main__':
	main()

