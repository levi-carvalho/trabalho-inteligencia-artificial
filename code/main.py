from settings import *
from agents.agent import Agent
# from agents.simple_reactive import SimpleReactive
# from agents.state_based import StateBased
# from agents.objective_based import ObjectiveBased
# from agents.utility_based import UtilityBased
# from agents.bdi_agent import BDIAgent
from sprites import *
from groups import AllSprites
from resources import *
from random import random
from random import randint
from pytmx.util_pygame import load_pygame


class Base(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        position -= pygame.Vector2((TILE_SIZE,TILE_SIZE))
        self.image = pygame.image.load(path.join('..','base.png')).convert_alpha()
        self.rect = self.image.get_frect(topleft=position)
        self.rect.center -= pygame.Vector2(((self.rect.width - TILE_SIZE)/2, (self.rect.height - TILE_SIZE)/2))
        print(self.rect)
        self.layer_order = 2
        

class Camera():
    def __init__(self, position):
        self.position = position
        self.direction = pygame.Vector2((0,0))
        self.speed = 0
        
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
       
        # self.utility_agents = pygame.sprite.Group()
        # self.objetives = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.all_sprites = AllSprites()
       
        self.clock = pygame.time.Clock()
        self.running = True
        self.create_agent = pygame.event.custom_type()
        
        self.setup()
        
    
    def place_random_resource(self, position):
        if random() < 0.15:
            Crystal(position, (self.all_sprites, self.collision_sprites, self.objetives))
        elif random() < 0.15:
            Metal(position, (self.all_sprites, self.collision_sprites, self.objetives))
        elif random() < 0.1:
            AncientBuilding(position, (self.all_sprites, self.collision_sprites, self.objetives))
    
    def setup(self):
        self.map_center = pygame.Vector2(21 * TILE_SIZE // 2, 21 * TILE_SIZE // 2)
        self.base_position = self.map_center
        self.base = Base(self.base_position, self.all_sprites)
        
        self.camera = Camera(self.base_position)
        
        map = load_pygame(path.join('..','map.tmx'))
        
        fog_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        for x, y, image in map.get_layer_by_name('layer_1').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            position = (x * TILE_SIZE, y * TILE_SIZE)
            # self.place_random_resource(position)
            Sprite(position, image, self.all_sprites, layer=0)    
            FogOfWar((x * TILE_SIZE, y * TILE_SIZE), fog_surface, (self.all_sprites, self.collision_sprites), layer=5)
            
        for x, y, image in map.get_layer_by_name('layer_2').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites, layer=1)
            
    def surfaces_setup(self):
        self.surfaces = {}
        self.surfaces['state_based'] = self.load_agent_sprite_sheet(1)
        self.surfaces['objective_based'] = self.load_agent_sprite_sheet(2)
        self.surfaces['simple_reactive'] = self.load_agent_sprite_sheet(3)
        self.surfaces['utility_based'] = self.load_agent_sprite_sheet(6)
    
    def load_agent_sprite_sheet(self, number):
        surface_path = path.join('..','dreamland','48x48',f'Char_00{number}.png')
        surface = pygame.image.load(surface_path).convert_alpha()
        
        return surface
    
    def run(self):
        self.surfaces_setup()
        
        Agent(72, self.map_center, self)
        # StateBased(72, self.map_center, self.surfaces['state_based'], self.all_sprites, self.collision_sprites)
        # SimpleReactive(72, self.map_center, self.surfaces['simple_reactive'], self.all_sprites, self.collision_sprites)
        # ObjectiveBased(72, self.map_center, self.surfaces['objective_based'], self.all_sprites, self.collision_sprites, self.objetives)
        
        # UtilityBased(72, self.map_center, self.surfaces['utility_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        # UtilityBased(72, self.map_center, self.surfaces['utility_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        # UtilityBased(72, self.map_center, self.surfaces['utility_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        # BDIAgent(72, self.map_center, self.surfaces['objective_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        # BDIAgent(72, self.map_center, self.surfaces['objective_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        # BDIAgent(72, self.map_center, self.surfaces['objective_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        
        while self.running:
            self.delta_time = self.clock.tick(120) / 1000
            
            self.display_surface.fill('black')
                    
            self.all_sprites.update(self.delta_time)
            # self.collision_sprites.update(self.delta_time)
            
            self.camera.update(self.delta_time)
            self.all_sprites.draw(self.camera.position)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()


class FogOfWar(Sprite):
    def __init__(self, position, surface, groups, layer):
        super().__init__(position, surface, groups, layer)
        fog_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        fog_surface.fill('black')
        fog_surface.set_alpha(255)
        self.image = fog_surface
        self.disapearing = False
        self.disapear_speed = 200
    
    def update(self, delta_time):
        if self.disapearing:
            alpha = self.image.get_alpha() - self.disapear_speed * delta_time
            if alpha <= 0:
                self.kill()
                return
            self.image.set_alpha(alpha)
            
if __name__ == '__main__':
    game = Game()
    game.run()