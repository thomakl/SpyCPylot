import time
import pygame
from pygame.locals import *
from rover import Rover20

MIN_BUTTON_LAG_SEC = 0.25

class keyboardrover20(Rover20):
	def __init__(self):
		Rover20.__init__(self)
		
		self.quit = False
		self.lastbuttontime = 0
		self.lastmovement = None
		
		self.movements = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
		
		self.windowSize = [640, 480]
		
		pygame.init()
		pygame.display.set_caption("Keyboard Rover")
		self.screen = pygame.display.set_mode(self.windowSize)
		print "YES"
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
						elif event.key == pygame.K_q:
							self.halt()
							listening = False					
						else:
							pass												
				if event.type == KEYUP:
					if event.key in self.movements:
						self.halt()
				if event.type == QUIT:
					listening = False
		self.quit = True	
		
	def moveForward(self):
		self.setTreads(0.5,0.5)
	
	def moveBackward(self):
		self.setTreads(-0.5,-0.5)
		
	def turnRight(self):
		self.setTreads(0.5,0)
		
	def turnLeft(self):
		self.setTreads(0,0.5)
	
	def halt(self):
		self.setTreads(0,0)
	
	def goodCommand(self, key):
		return ((time.time() - self.lastbuttontime) > MIN_BUTTON_LAG_SEC) and key is not self.lastmovement
	
def main():	
	rover = keyboardrover20()
	
	while not rover.quit:
		pass
	rover.close()
	pygame.quit()
	print "DONE"
			
if __name__ == '__main__':
	main()	
		
