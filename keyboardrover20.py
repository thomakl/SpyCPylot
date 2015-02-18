import pygame
from pygame.locals import *
from rover import Rover20

class keyboardrover20(Rover20):
	def __init__(self):
		Rover20.__init__(self)
		
		self.quit = False
		
		# WASD movement controls
		
		def self.movements = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
		
		self.windowSize = [640, 480]
		
		pygame.init()
		pygame.display.set_caption("Keyboard Rover")
		self.screen = pygame.display.set_mode(self.windowSize)
		print "YES"
		try:
			self.keyListen()
		except KeyboardInterrupt:
			self.quit = True
	
	def keyListen():
		listening = True
		while listening:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key in self.movements:
						
				elif event.type == KEYUP:
					if event.key in self.movements:
						self.halt()
				elif event.type == QUIT:
					listening = False
		self.quit = True	
		
	def moveForward():
		setTreads(1,1)
	
	def moveBackward():
		setTreads(-1,-1)
		
	def turnRight():
		setTreads(1,0)
		
	def turnLeft():
		setTreads(0,1)
	
	def halt():
		setTreads(0,0)
	
def main():	
	rover = keyboardrover20()
	
	while not rover.quit:
		pass
	rover.close()
	print "DONE"
			
if __name__ == '__main__':
	main()	
		
