from settings import *
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
        self.image = pygame.image.load(path.join('..','base.png')).convert_alpha()
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
       
        self.collision_sprites = pygame.sprite.Group()
        self.utility_agents = pygame.sprite.Group()
        self.objetives = pygame.sprite.Group()
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
        
        for x, y, image in map.get_layer_by_name('layer_1').tiles():
            image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            position = (x * TILE_SIZE, y * TILE_SIZE)
            self.place_random_resource(position)
            Sprite(position, image, self.all_sprites, layer=0)    
            
            
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
        surface_path = path.join('..','dreamland','48x48',f'Char_00{number}.png')
        surface = pygame.image.load(surface_path).convert_alpha()
        
        return surface
    
    def test_agent(self, agent_type, duration):
        self.surfaces_setup()
        agent_classes = {
            'state_based': StateBased,
            'simple_reactive': SimpleReactive,
            'objective_based': ObjectiveBased,
            'utility_based': UtilityBased,
            'bdi_agent': BDIAgent
        }
        
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.objetives.empty()
        self.setup()
        
        AgentClass = agent_classes[agent_type]
        if agent_type in ['state_based', 'simple_reactive']:
            AgentClass(72, self.map_center, self.surfaces[agent_type], self.all_sprites, self.collision_sprites)
        elif agent_type in ['objective_based', 'utility_based', 'bdi_agent']:
            AgentClass(72, self.map_center, self.surfaces[agent_type], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration * 1000:
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
                    return
                
    def test_agent_group(self, agent_type, count, duration):
        self.surfaces_setup()
        agent_classes = {
            'utility_based': UtilityBased,
            'bdi_agent': BDIAgent
        }
        
        if agent_type not in agent_classes:
            print(f"Agent type {agent_type} not supported for group tests.")
            return

        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.objetives.empty()
        self.setup()
        
        AgentClass = agent_classes[agent_type]
        for _ in range(count):
            random_offset = pygame.Vector2(randint(-100, 100), randint(-100, 100))
            AgentClass(72, self.map_center + random_offset, self.surfaces[agent_type], 
                    (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration * 1000:
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
                    return
    
    def run_individual_tests(self):
        self.surfaces_setup()
        
        while self.running:
            agent_types = ['state_based', 'simple_reactive', 'objective_based', 'utility_based', 'bdi_agent']
            for agent_type in agent_types:
                print(f"Testing agent type: {agent_type}")
                self.test_agent(agent_type, 60)
    
    def run_group_tests(self):
        agent_types = ['utility_based', 'bdi_agent']
        for agent_type in agent_types:
            print(f"Testing agent type: {agent_type}")
            if agent_type in ['utility_based', 'bdi_agent']:
                self.test_agent_group(agent_type, 3, 30)  # Test groups of 3 for 30 seconds
            else:
                self.test_agent(agent_type, 30) 
                    
    def run(self):
        self.surfaces_setup()
        
        StateBased(72, self.map_center, self.surfaces['state_based'], self.all_sprites, self.collision_sprites)
        SimpleReactive(72, self.map_center, self.surfaces['simple_reactive'], self.all_sprites, self.collision_sprites)
        ObjectiveBased(72, self.map_center, self.surfaces['objective_based'], self.all_sprites, self.collision_sprites, self.objetives)
        
        UtilityBased(72, self.map_center, self.surfaces['utility_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        UtilityBased(72, self.map_center, self.surfaces['utility_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        UtilityBased(72, self.map_center, self.surfaces['utility_based'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        BDIAgent(72, self.map_center, self.surfaces['bdi_agent'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        BDIAgent(72, self.map_center, self.surfaces['bdi_agent'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        BDIAgent(72, self.map_center, self.surfaces['bdi_agent'], (self.all_sprites, self.utility_agents), self.collision_sprites, self.objetives, self.utility_agents)
        
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