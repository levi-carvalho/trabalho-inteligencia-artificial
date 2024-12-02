from settings import *
from agents.agent import Agent
from agents.simple_reactive import SimpleReactive
from agents.state_based import StateBased
from agents.objective_based import ObjectiveBased
from agents.utility_based import UtilityBased
from agents.bdi_agent import BDIAgent
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
        self.image = pygame.image.load(path.join('..','assets','base.png')).convert_alpha()
        self.rect = self.image.get_frect(topleft=position)
        self.rect.center -= pygame.Vector2(((self.rect.width - TILE_SIZE)/2, (self.rect.height - TILE_SIZE)/2))
        self.layer_order = 2
    
    def update(self, *agrs):
        m_pos_x = int(self.rect.centerx/TILE_SIZE)
        m_pos_y = int(self.rect.centery/TILE_SIZE)
        self.m_position = (m_pos_x, m_pos_y)

class Camera():
    def __init__(self, position):
        self.position = position
        self.direction = pygame.Vector2((0,0))
        self.speed = 400
        
    def fuck_around(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, delta_time):
        self.position.x += self.direction.x * self.speed * delta_time
        self.position.y += self.direction.y * self.speed * delta_time
    
    def update(self, delta_time):
        self.fuck_around()
        self.move(delta_time)

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ablu bla blé")
        
        self.display_surface = pygame.display.get_surface()
       
        self.utility_agents = pygame.sprite.Group()
        self.objetives = pygame.sprite.Group()
        
        self.resources = pygame.sprite.Group()
        
        self.collision_sprites = pygame.sprite.Group()
        self.all_sprites = AllSprites()
       
        self.clock = pygame.time.Clock()
        self.running = True
        self.create_agent = pygame.event.custom_type()
        
        self.map_size = 21
        
        self.setup()
        
    
    def place_random_resource(self, position):
        center = (self.map_size // 2, self.map_size // 2)
        distance = abs(position[0]/TILE_SIZE - center[0]) + abs(position[1]/TILE_SIZE - center[1])
        if distance < 4:
            return
        elif random() < 0.1:
            Crystal(position, (self.all_sprites, self.resources, self.collision_sprites))
        elif random() < 0.1:
            Metal(position, (self.all_sprites, self.resources, self.collision_sprites))
        elif random() < 0.1:
            AncientBuilding(position, (self.all_sprites, self.resources, self.collision_sprites))
    
    def setup(self):
        self.map_center = pygame.Vector2(21 * TILE_SIZE // 2, 21 * TILE_SIZE // 2)
        self.base_position = self.map_center
        self.base = Base(self.base_position, self.all_sprites)
        
        self.matrix = np.ones((self.map_size, self.map_size))
        self.camera = Camera(self.base_position)
        fog_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        map = load_pygame(path.join('..','assets','map.tmx'))
        
        for obj in map.get_layer_by_name('object'):
            CollisionSprite((obj.x * 2, obj.y * 2), pygame.Surface((obj.width * 2, obj.height * 2), pygame.SRCALPHA), (self.collision_sprites, self.all_sprites))
            self.matrix[math.floor((obj.y * 2 + 32)/TILE_SIZE)][math.floor((obj.x * 2 + 32)/TILE_SIZE)] = 0
        
        for x, y, image in map.get_layer_by_name('layer_1').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            position = (x * TILE_SIZE, y * TILE_SIZE)
            Sprite(position, image, self.all_sprites, layer=0)    
            FogOfWar((x * (TILE_SIZE), y * (TILE_SIZE)), fog_surface, (self.all_sprites, self.collision_sprites), layer=5)
            if self.matrix[y,x]:
                self.place_random_resource(position)
            
            # FogOfWar((x * TILE_SIZE, y * TILE_SIZE), fog_surface, (self.all_sprites, self.collision_sprites), layer=5)
            # FogOfWar((x * (TILE_SIZE/2), y * (TILE_SIZE/2) + (self.map_size * TILE_SIZE) / 2), fog_surface, (self.all_sprites, self.collision_sprites), layer=5)
            # FogOfWar((x * (TILE_SIZE/2) + (self.map_size * TILE_SIZE) / 2, y * (TILE_SIZE/2) ), fog_surface, (self.all_sprites, self.collision_sprites), layer=5)
            # FogOfWar((x * (TILE_SIZE/2) + (self.map_size * TILE_SIZE) / 2, y * (TILE_SIZE/2) + (self.map_size * TILE_SIZE) / 2), fog_surface, (self.all_sprites, self.collision_sprites), layer=5)
            
        for x, y, image in map.get_layer_by_name('layer_2').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites, layer=1)
            
    def surfaces_setup(self):
        self.surfaces = {}
        self.surfaces['state_based'] = self.load_agent_sprite_sheet(1)
        self.surfaces['objective_based'] = self.load_agent_sprite_sheet(2)
        self.surfaces['simple_reactive'] = self.load_agent_sprite_sheet(3)
        self.surfaces['utility_based'] = self.load_agent_sprite_sheet(6)
        self.surfaces['bdi_agent'] = self.load_agent_sprite_sheet(5)
    
    def load_agent_sprite_sheet(self, number):
        surface_path = path.join('..','assets','dreamland','48x48',f'Char_00{number}.png')
        surface = pygame.image.load(surface_path).convert_alpha()
        
        return surface
    
    def run(self):
        self.surfaces_setup()
        
        # Agent(72, self.map_center, self)
        SimpleReactive(72, self.map_center, self.surfaces['state_based'], self)
        StateBased(72, self.map_center, self.surfaces['simple_reactive'], self)
        ObjectiveBased(72, self.map_center, self.surfaces['objective_based'], self)
        
        # UtilityBased(72, self.map_center, self.surfaces['utility_based'], self.utility_agents, self)
        # UtilityBased(72, self.map_center, self.surfaces['utility_based'], self.utility_agents, self)
        UtilityBased(72, self.map_center, self.surfaces['utility_based'], self.utility_agents, self)
        
        BDIAgent(72, self.map_center, self.surfaces['bdi_agent'], self.utility_agents, self)
        # BDIAgent(72, self.map_center, self.surfaces['bdi_agent'], self.utility_agents, self)
        # BDIAgent(72, self.map_center, self.surfaces['bdi_agent'], self.utility_agents, self)
        
        while self.running:
            self.delta_time = self.clock.tick() / 1000
            
            self.display_surface.fill('black')
                    
            self.all_sprites.update(self.delta_time)
            
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