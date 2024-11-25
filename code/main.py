from settings import *
from agents.simple_reactive import SimpleReactive
from agents.state_based import StateBased
from agents.objective_based import ObjectiveBased
from sprites import *
from groups import AllSprites
from resources import *
from random import random
from random import randint
from pytmx.util_pygame import load_pygame


class Base(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load(path.join('..','base.png'))
        self.rect = self.image.get_rect(bottomright=position)
        print(self.rect)
        self.layer_order = 2
        

class Camera():
    def __init__(self, position):
        self.position = position
        self.direction = pygame.Vector2((0,0))
        self.speed = 300
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, delta_time):
        self.position.x += self.direction.x * self.speed * delta_time
        self.position.y += self.direction.y * self.speed * delta_time
    
    def update(self, delta_time):
        self.input()
        self.move(delta_time)

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ablu bla blé")
        
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.objetives = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.running = True
        self.create_agent = pygame.event.custom_type()
        pygame.time.set_timer(self.create_agent, 2000)
        
        self.setup()
        
    
    def setup(self):
        self.map_center = pygame.Vector2(21 * TILE_SIZE // 2, 21 * TILE_SIZE // 2)
        self.base_position = self.map_center
        self.base = Base(self.base_position, self.all_sprites)
        
        self.camera = Camera(self.base_position)
        
        map = load_pygame(path.join('..','map.tmx'))
        
        for x, y, image in map.get_layer_by_name('layer_1').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            position = (x * TILE_SIZE, y * TILE_SIZE)
            
            if random() < 0.1:
                Crystal(position, (self.all_sprites, self.collision_sprites, self.objetives))
            elif random() < 0.1:
                Metal(position, (self.all_sprites, self.collision_sprites, self.objetives))
            elif random() < 0.05:
                AncientBuilding(position, (self.all_sprites, self.collision_sprites, self.objetives))
            Sprite(position, image, self.all_sprites, layer=0)
                
            
        for x, y, image in map.get_layer_by_name('layer_2').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites, layer=1)

    
    def surfaces_setup(self):
        self.surfaces = {}
        self.surfaces['state_based'] = self.load_agent_sprite_sheet(1)
        self.surfaces['objective_based'] = self.load_agent_sprite_sheet(2)
        self.surfaces['simple_reactive'] = self.load_agent_sprite_sheet(3)
    
    def load_agent_sprite_sheet(self, number):
        surface_path = path.join('..','dreamland','48x48',f'Char_00{number}.png')
        surface = pygame.image.load(surface_path).convert_alpha()
        
        return surface
    
    def run(self):
        self.surfaces_setup()
        
        SimpleReactive(72, self.map_center, self.surfaces['simple_reactive'], self.all_sprites, self.collision_sprites)
        StateBased(72, self.map_center, self.surfaces['state_based'], self.all_sprites, self.collision_sprites)
        ObjectiveBased(72, self.map_center, self.surfaces['objective_based'], self.all_sprites, self.collision_sprites, self.objetives)
        
        while self.running:
            self.delta_time = self.clock.tick() / 1000
            
            self.display_surface.fill('black')
                    
            self.all_sprites.update(self.delta_time)
            self.collision_sprites.update(self.delta_time)
            
            self.camera.update(self.delta_time)
            self.all_sprites.draw(self.camera.position)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()