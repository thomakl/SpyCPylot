import time
import pygame
from pygame.locals import *
from rover import Rover20

MIN_BUTTON_LAG_SEC = 0.25

# vals < 1 yield slower speed
MAX_TREAD_SPEED = 0.5

class KeyboardRover20(Rover20):
	def __init__(self):
		Rover20.__init__(self)
		
		self.quit = False
		
		'''
		Trying to prevent repeated instructions that may be causing lag,
		but lag could be from another issue entirely (possibly batteries)
		'''
		self.lastbuttontime = 0
		self.lastmovement = None
		
		# WASD controls
		self.movements = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
		
		# window must be open and in focus for pygame to take input
		self.windowSize = [640, 480]
		
		pygame.init()
		pygame.display.set_caption("Keyboard Rover")
		self.screen = pygame.display.set_mode(self.windowSize)
		
		# Ctrl-C in Terminal (not game window) quits program for now
		try:
			self.keyListen()
		except KeyboardInterrupt:
			self.quit = True
	
	def keyListen(self):
		listening = True
		while listening:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key in self.movements and self.goodCommand(event.key):
						
						self.lastbuttontime = time.time()
						self.lastmovement = event.key
						
						if event.key == self.movements[0]:
							self.moveForward()
						elif event.key == self.movements[1]:
							self.turnLeft()
						elif event.key == self.movements[2]:
							self.moveBackward()
						elif event.key == self.movements[3]:
							self.turnRight()				
						else:
							#ignore other keys for now
							pass
																		
				if event.type == KEYUP:
					# letting go of WASD stops movement	
					if event.key in self.movements:
						self.halt()
				
				if event.type == QUIT:
					listening = False
		self.quit = True	

	def moveForward(self):
		self.setTreads(MAX_TREAD_SPEED, MAX_TREAD_SPEED)
	
	def moveBackward(self):
		self.setTreads(-MAX_TREAD_SPEED, -MAX_TREAD_SPEED)
		
	def turnRight(self):
		self.setTreads(MAX_TREAD_SPEED,0)
		
	def turnLeft(self):
		self.setTreads(0,MAX_TREAD_SPEED)
	
	def halt(self):
		self.setTreads(0,0)
	
	'''
	goodCommand() needs better function name	
	prevents 'button jump'
	'''
	def goodCommand(self, key):
		return ((time.time() - self.lastbuttontime) > MIN_BUTTON_LAG_SEC) and (key is not self.lastmovement)
	
def main():	
	rover = KeyboardRover20()
	
	while not rover.quit:
		pass
	
	rover.close()
	pygame.quit()

			
if __name__ == '__main__':
	main()	
		
