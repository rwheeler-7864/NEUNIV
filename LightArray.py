from interface import Interface, implements
import pygame

class LightArray(Interface):

    def turnOn(self, x, y):
        pass

    def turnOff(self, x, y):
        pass

    def cleanup(self):
	pass

    def getWidth(self):
	pass

    def getHeight(self):
	pass

class SimulatedTrafficArray(implements(LightArray)):
    
    def __init__(self, width, height, size):
        self.w = width
        self.h = height
        self.size = size
        self.colors = [(45,201,55), (231,180,22), (204,50,50)]
        pygame.init()
        self.screen = pygame.display.set_mode((self.w * self.size, self.h * self.size))
        self.screen.fill((0, 0, 0))
        for i in range(0, self.w):
            for j in range(0, self.h):
               self.turnOff(i, j) 
        pygame.display.update()

    def turnOn(self, x, y):
        color = self.colors[y % 3]
        pygame.draw.ellipse(self.screen, color, [x * self.size, y * self.size, self.size, self.size])
        pygame.display.update()
        return

    def turnOff(self, x, y):
        pygame.draw.ellipse(self.screen, (25, 25, 25), [x * self.size, y * self.size, self.size, self.size])
        pygame.display.update()
        return

    def getWidth(self):
	return self.w

    def getHeight(self):
	return self.h

    def cleanup(self):
	pygame.quit()
