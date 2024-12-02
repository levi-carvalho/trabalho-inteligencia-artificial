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

class FogOfWar(Sprite):
    def __init__(self, position, surface, groups, layer):
        super().__init__(position, surface, groups, layer)
        fog_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        fog_surface.fill('black')
        fog_surface.set_alpha(230)
        self.image = fog_surface
        self.disapearing = False
        self.disapear_speed = 200
        self.time_accumulator = 0
        self.pulse_speed = uniform(0.3, 1.8)
    
    def update(self, delta_time):
        if self.disapearing:
            alpha = self.image.get_alpha() - self.disapear_speed * delta_time
            if alpha <= 0:
                self.kill()
                return
            self.image.set_alpha(max(0, int(alpha)))
        else:
            self.time_accumulator += delta_time
            base_alpha = 210
            amplitude = 10
            
            alpha = base_alpha + amplitude * math.sin(self.pulse_speed * self.time_accumulator)
            self.image.set_alpha(int(alpha))