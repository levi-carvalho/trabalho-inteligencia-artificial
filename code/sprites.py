from settings import *

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = position)
        self.layer_order = 3
        
class Sprite(CollisionSprite):
    def __init__(self, position, surface, groups, layer):
        super().__init__(position, surface, groups)
        self.ground = True
        self.layer_order = layer