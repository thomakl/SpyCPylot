'''
This version of the rover separates the rover (roverShell) from 
the pygame controller (roverBrain). With this design, we can create 
new controllers without needing to redesign the basic rover functions.

CONTROLS:

WASD - Drive
SPACE - Take Picture

J - Camera Up
K - Camera Down

U - Toggle Infrared
I - Toggle Lights
'''
import pygame
from pygame.locals import *

from time import sleep
from datetime import date
from random import choice
from threading import Lock
from string import ascii_lowercase, ascii_uppercase
import StringIO
from rover import Rover20
'''
 The Lock() is used to prevent two processes from trying to access 
 a resource at the same time, which would cause errors.
'''
lock = Lock()
	
class roverShell(Rover20):
	def __init__(self):
		Rover20.__init__(self)

		self.quit = False
		self.peripherals = {'lights': False, 'stealth': False, 'camera': 0}
		self.treads = [0,0]
		self.currentImage = None
		
	# called by Rover20, acts as a main loop
	def processVideo(self, jpegbytes, timestamp_10msec):
		
		# safely write image
		lock.acquire()		
		self.currentImage = jpegbytes		
		lock.release()
		
		# update movement
		self.setTreads(self.treads[0], self.treads[1])
		
		#update lights/infrared/camera	
		self.setPeripherals()				
		
		if self.quit:
			self.close()


	def setPeripherals(self):		
		if self.peripherals['lights']:
			self.turnLightsOn()
		else:
			self.turnLightsOff()
		if self.peripherals['stealth']:
			self.turnStealthOn()
		else:
			self.turnStealthOff()
		if self.peripherals['camera'] in (-1,0,1):
			self.moveCameraVertical(self.peripherals['camera'])
		else:
			self.peripherals['camera'] = 0
			
	

class roverBrain():
	def __init__(self):
		
		self.rover = roverShell()
		self.quit = False
		
		# [width, height]
		self.windowSize = [640, 480]

		# [x, y, width, height]
		self.imageRect = (160,120,320,240)

		self.fps = 60
		
		self.displayCaption = "Keyboard Rover 2.0"

		pygame.init()
		pygame.display.init()
		pygame.display.set_caption(self.displayCaption)

		self.screen = pygame.display.set_mode(self.windowSize)
		self.clock = pygame.time.Clock()
		
		self.run()
	
			
	def run(self):
		sleep(2) # allows roverShell to first write 'jpegbytes'
		
		while not self.quit:			
			self.parseControls()
			self.refreshVideo()
		
		self.rover.quit = True
		pygame.quit()
	
	
	def refreshVideo(self):	
		# safely load image
		lock.acquire()		
		currentImage = StringIO.StringIO(self.rover.currentImage)	
		lock.release()			
		
		currentImage.seek(0)
		image = pygame.image.load(currentImage, 'tmp.jpg').convert()
		currentImage.close()
		
		# render image		
		self.screen.blit(image, (160, 120))
		pygame.display.update(self.imageRect)
		self.clock.tick(self.fps)
	
		
	def parseControls(self):
		for event in pygame.event.get():

			if event.type == QUIT:
				self.quit = True

			elif event.type == KEYDOWN:
				# camera
				if event.key in (K_j, K_k, K_SPACE, K_u, K_i):
					self.updatePeripherals(event.key)
				# drive
				elif event.key in (K_w, K_a, K_s, K_d):
					self.updateTreads(event.key)
				else:
					pass
					
			elif event.type == KEYUP:
				# drive
				if event.key in (K_w, K_a, K_s, K_d):
					self.updateTreads()
				# camera
				elif event.key in (K_j, K_k):
					self.updatePeripherals()
				else:
					pass
			else:
				pass
	
	
	def updateTreads(self, key=None):		
		if key is None:
			self.rover.treads = [0,0]
		elif key is K_w:
			self.rover.treads = [1,1]
		elif key is K_s:
			self.rover.treads = [-1,-1]
		elif key is K_a:
			self.rover.treads = [-0.5,0.5]
		elif key is K_d:
			self.rover.treads = [0.5,-0.5]
		else:
			pass
		
		
	def updatePeripherals(self, key=None):		
		if key is None:
			self.rover.peripherals['camera'] = 0
		elif key is K_j:
			self.rover.peripherals['camera'] = 1
		elif key is K_k:
			self.rover.peripherals['camera'] = -1
		elif key is K_u:
			self.rover.peripherals['stealth'] = \
			not self.rover.peripherals['stealth']
		elif key is K_i:
			self.rover.peripherals['lights'] = \
			not self.rover.peripherals['lights']
		elif key is K_SPACE:
			lock.acquire()
			self.takePicture()
			lock.release()
		else:
			pass
	
	
	def takePicture(self):
		with open(self.newPictureName(), 'w') as pic:
			pic.write(self.rover.currentImage)			
	
			
	# today's date plus a random string of letters
	def newPictureName(self):
		todaysDate = str(date.today())
		uniqueKey = ''.join(choice(ascii_lowercase + ascii_uppercase) \
							for _ in range(4))
		return todaysDate+'_'+uniqueKey+'.jpg'	



if __name__ == '__main__':
	brain = roverBrain()
