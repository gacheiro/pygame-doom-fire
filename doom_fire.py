"""DOOM fire algorithm in Pygame.

This code is adapted from <https://github.com/filipedeschamps/doom-fire-algorithm>
"""


import pygame
from random import randint, random


# Color pallete
PALETTE = (
    (7, 7, 7), (31, 7, 7), (47, 15, 7), (71, 15, 7), (87, 23, 7), (103, 31, 7), 
    (119, 31, 7), (143, 39, 7), (159, 47, 7), (175, 63, 7), (191, 71, 7),
    (199, 71, 7), (223, 79, 7), (223, 87, 7), (223, 87, 7), (215, 95, 7),
    (215, 95, 7), (215, 103, 15), (207, 111, 15), (207, 119, 15),
    (207, 127, 15), (207, 135, 23), (199, 135, 23), (199, 143, 23),
    (199, 151, 31), (191, 159, 31), (191, 159, 31), (191, 167, 39),
    (191, 167, 39), (191, 175, 47), (183, 175, 47), (183, 183, 47),
    (183, 183, 55), (207, 207, 111), (223, 223, 159), (239, 239, 199),
    (255, 255, 255),
)


# Fire intensity
LOW = (0, 14)
MEDIUM = (14, 32)
HIGH = (32, 36)

UPDATE_RATE = 75
PIXEL_SIZE = 5


class Fire(object):
    """A DOOM-style fire animation.
    
    Attributes:
        width (int): The fire width.
        height (int): The fire height.
        pixels (list): The fire pixels.
        
    Examples:
        Instantiate a fire with width and height 20:
        
        >>> Fire(width=20, height=20, intensity=HIGH, pixel_size=5)
    """
    def __init__(self, width, height, intensity, pixel_size=5):
        """Creates a DOOM-style fire animation.
        
        
        Args:
            width (int): The fire width.
            height (int): The fire height.
            intensity (2-tuples): The intensity of the fire. Use one of the 
                top-level constants HIGH, MEDIUM, LOW.
            pixel_size (int, optional): The size of each rect used to draw 
                the fire. Defaults to 5.
        """
        self.width, self.height = width, height
        self._pixel_size = pixel_size
        
        self.pixels = self._create(width, height, intensity)
        
    def update(self):
        """Update the fire. Usually needs to be updated every 75ms."""
        for i in range(self.width * self.height):    
                             
                try:
                    pixel_below = self.pixels[i+self.width]
                    decay = int(random() * 2)
                    
                    if i - decay < 0:
                        continue
                        
                    self.pixels[i - decay] = max(pixel_below - decay, 0)
                    
                except IndexError:
                    pass
                              
    def draw(self, surface, offset=(0, 0)):
        """Draw the fire using a set of rects.
        
        Args:
            surface (pygame.Surface): The surface to draw the fire.
            offset (2-tuple, optional): The topleft offset. Defaults to (0, 0).
        """
        rects = self._rects(self.width, self.height, self._pixel_size, offset)
        for pixel, rect in zip(self.pixels, rects):
            pygame.draw.rect(surface, self.color(pixel), rect)
                    
    def increase(self):
        """Increase the intensity of the fire source."""
        for i in range(1, self.width + 1):
            self.pixels[-i] = min(self.pixels[-i] + randint(0, 14), 36)
            
    def decrease(self):
        """Decrease the intensity of the fire source."""
        for i in range(1, self.width + 1):
            self.pixels[-i] = max(self.pixels[-i] - randint(0, 14), 0)
            
    @staticmethod
    def color(value, pallete=PALETTE):
        """Returns a color represented by a pixel value.
        
        A pallete can be passed as a keyword argument. Note that
        a pallete must have atleast 36 length.
        
        Args:
            value (int): The pixel value that will be mapped to a color.
            pallete (list, optional): The color pallete. If None is passed,
                it will be set to the default pallete.
        """
        v = max(value, 0)
        try:
            return pallete[v]
        except IndexError:
            return pallete[-1]
    
    
    @staticmethod
    def _create(width, height, intensity=HIGH):
        """Creates a fire source."""
        fire = [0] * (width * height)
        for i in range(1, width+1):
            # sets the last row with random values in the intensity range
            fire[-i] = randint(*intensity)
        return fire
        
    @staticmethod
    def _rects(width, height, pixel_size=PIXEL_SIZE, offset=(0, 0)):
        '''Generates the rects used to draw the fire.'''
        x0, y0 = offset
        for i in range(height):
            for j in range(width):
                yield (x0 + j*pixel_size, 
                    y0 + i*pixel_size, pixel_size, pixel_size)                
               
           
def main():
    width, height = 640, 360
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Pygame Fire')
    
    # creates fire filling the whole screen
    fire = Fire(width//PIXEL_SIZE, height//PIXEL_SIZE, intensity=HIGH)
    
    # load pygame logo
    pygame_img = pygame.image.load('assets/pygame_logo.png').convert_alpha()
    pygame_img = pygame.transform.scale(pygame_img, (540, 151))
    
    clock = pygame.time.Clock()
    elapsed = 0
    
    print('\nUse the arrow keys up and down to increase/decrease the fire.')
    
    while True:
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:  
                fire.decrease()
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:  
                fire.increase() 
        
        # check that the fire will only be updated every 75ms,
        # otherwise the animation will be too fast.
        if elapsed >= UPDATE_RATE:
            fire.update()
            elapsed = 0
        
        # clear the screen
        screen.fill((7, 7, 7))
        
        # draw the fire and pygame logo
        fire.draw(screen)
        screen.blit(pygame_img, (50, 100))
        
        # update the screen
        pygame.display.update()
        
        elapsed += clock.tick(60)

        
if __name__ == '__main__':
    main()
