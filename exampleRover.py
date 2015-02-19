from rover import Rover20
import time


def main():
	
	rover = Rover20() #create rover
		
	rover.setTreads(1,1) #forwards	
	time.sleep(1) #wait 1 second
	
	rover.setTreads(0,0) #stop	
	time.sleep(1)
	
	rover.setTreads(-1,-1) #backwards	
	time.sleep(1)
	
	rover.setTreads(0,0)
	time.sleep(1)
		
	rover.turnLightsOn() #turn on green lights	
	time.sleep(1)
	
	rover.turnLightsOff()	
	time.sleep(1)
	
	rover.close() #close rover
	
main()
