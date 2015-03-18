'''
CHANGES:

1. Toggle feature detector with 'O'
2. cv2 operations done in rover thread instead
	of its own thread.
3. Infrared does not work, but it may be a problem
	with my rover. It doesn't work in KeyboardRover.py
	either.

CONTROLS:

WASD - Drive
SPACE - Take Picture

J - Camera Up
K - Camera Down

U - Toggle Infrared (not working)
I - Toggle Lights
O - Toggle Feature Detector
'''
import pygame
from pygame.locals import *
from time import sleep
from datetime import date
from random import choice
from string import ascii_lowercase, ascii_uppercase
import threading 
import cStringIO
import cv2
import numpy as np
from rover import Rover20


class roverShell(Rover20):
	def __init__(self):
		Rover20.__init__(self)
		self.quit = False
		self.orb = cv2.ORB()
		self.lock = threading.Lock()
		
		self.treads = [0,0]
		self.currentImage = None
		self.peripherals = {'lights': False, 'stealth': False, \
							'detect': True, 'camera': 0}
		
			
	# called by Rover20, acts as a main loop
	def processVideo(self, jpegbytes, timestamp_10msec):
		# update video						
		self.lock.acquire()		
		if self.peripherals['detect']:		
			self.currentImage = self.processImage(jpegbytes)
		else:
			self.currentImage = jpegbytes				
		self.lock.release()		
		
		# update movement
		self.setTreads(self.treads[0], self.treads[1])		
		
		# update lights/infrared/camera	
		self.setPeripherals()						
		if self.quit:
			self.close()


	def processImage(self, jpegbytes):
		img = np.asarray(bytearray(jpegbytes), dtype=np.uint8)
		img = cv2.imdecode(img, 0)
		keypoints = self.orb.detect(img,None)
		keypoints, des = self.orb.compute(img, keypoints)		
		img = cv2.drawKeypoints(img, keypoints, color=(0,255,0))			
		return cv2.imencode('.jpg', img)[1].tostring()


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
		self.quit = False
		self.rover = roverShell()		
		
		self.fps = 24
		self.windowSize = [640, 480]
		self.imageRect = (160,120,320,240)						
		self.displayCaption = "Keyboard Rover 2.0"
		
		pygame.init()
		pygame.display.init()
		pygame.display.set_caption(self.displayCaption)
		self.screen = pygame.display.set_mode(self.windowSize)
		self.clock = pygame.time.Clock()		
		self.run()
	
			
	def run(self):
		sleep(1.5)
		while not self.quit:			
			self.parseControls()
			self.refreshVideo()	
		self.rover.quit = True
		pygame.quit()
	
	
	def refreshVideo(self):	
		# prepare image
		self.rover.lock.acquire()
		image = self.rover.currentImage
		self.rover.lock.release()							
		image = cStringIO.StringIO(image)		
		image = pygame.image.load(image, 'tmp.jpg').convert()
		
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
				if event.key in (K_j, K_k, K_SPACE, K_u, K_i, K_o):
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
			self.rover.peripherals['stealth'] = not \
			self.rover.peripherals['stealth']
		elif key is K_i:
			self.rover.peripherals['lights'] = not \
			self.rover.peripherals['lights']
		elif key is K_o:
			self.rover.peripherals['detect'] = not \
			self.rover.peripherals['detect']
		elif key is K_SPACE:
			self.takePicture()
		else:
			pass
	
	
	def takePicture(self):
		with open(self.newPictureName(), 'w') as pic:
			self.rover.lock.acquire()
			pic.write(self.rover.currentImage)			
			self.rover.lock.release()
	
			
	def newPictureName(self):
		todaysDate = str(date.today())
		uniqueKey = ''.join(choice(ascii_lowercase + ascii_uppercase) \
							for _ in range(4))
		return todaysDate+'_'+uniqueKey+'.jpg'	



if __name__ == '__main__':
	brain = roverBrain()
