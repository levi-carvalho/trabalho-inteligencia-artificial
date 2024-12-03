from settings import *
from resources import Resource
from sprites import *

class Agent(pygame.sprite.Sprite):
    def __init__(self, size, position, spritesheet, game, *agrs):
        super().__init__(game.all_sprites)
        self.game = game
        self.size = size
        self.spritesheet = spritesheet
        self.collision_sprites = game.collision_sprites
        self.base_pos = position
        self.frames = {'down': [], 'left': [], 'right': [], 'up': []}
        
        self.load_images()
        self.image = self.frames['down'][0]
        self.state, self.frame_index = 'down', 0
        self.rect = self.image.get_frect(topleft = position)
        self.direction = pygame.Vector2((0,0))
        self.speed = self.game.agent_speed
        self.points = 0
        
        self.hitbox = self.rect
        
        
        self.layer_order = 3
        
        self.moves = []
        self.moving = False
        self.moved = 0
        
        self.set_perception(3)
        
        self.busy = False
        self.found_resources = []
        self.limit = 20
    
    def define_path_to(self, position):
        grid = Grid(matrix=self.game.matrix)
        
        offset_x =  - self.game.camera.position[0] + WINDOW_WIDTH / 2
        offset_y =  - self.game.camera.position[1] + WINDOW_HEIGHT / 2
        offset = pygame.Vector2((offset_x, offset_y))
        
        start = grid.node(round(self.rect.center[0]/TILE_SIZE), round(self.rect.center[1]/TILE_SIZE)) 
        end = grid.node(round(position[0]), round(position[1]))
        
        finder = AStarFinder()
        
        path, runs = finder.find_path(start, end, grid)
        
        moves = []
        for move in path:
            moves.append(pygame.Vector2((move.x, move.y)))
        
        directions = []
        for i in range(len(moves) - 1):
            direction = moves[i + 1] - moves[i]
            direction = direction.normalize()
            directions.append(direction)
        
        self.moves = directions

    def fuck_around(self):
            
        if pygame.mouse.get_pressed()[0]:
            offset_x =  - self.game.camera.position[0] + WINDOW_WIDTH / 2
            offset_y =  - self.game.camera.position[1] + WINDOW_HEIGHT / 2
            offset = pygame.Vector2((offset_x, offset_y))
            mouse_position = pygame.Vector2(pygame.mouse.get_pos())
            mouse_position = (mouse_position - offset)/TILE_SIZE
    
            self.define_path_to(mouse_position)
    
    def set_perception(self, size):
        self.perception_size = size
        self.perception = pygame.Rect(0,0,self.perception_size*TILE_SIZE, self.perception_size*TILE_SIZE)
        self.perception = self.perception.scale_by(0.9)
        self.perception.center = self.rect.center
        pass
    
    def define_target(self):
        pass
    
    def move(self, delta_time):
        if not self.moving:
            if len(self.moves) > 0:
                self.direction = self.moves[0]
                self.moving = True
            else:
                if len([resource for resource in self.found_resources if (pygame.time.get_ticks() - resource.last_tried) > resource.cooldown_duration]) > 0:
                    self.define_target()
                else:
                    self.fuck_around()
        else:
            self.rect.x += self.direction.x * self.speed * delta_time
            self.rect.y += self.direction.y * self.speed * delta_time
            
            self.moved += self.speed * delta_time
            
            if self.moved >= 64:
                overshoot = self.moved - 64
                self.rect.x -= self.direction.x * overshoot
                self.rect.y -= self.direction.y * overshoot
                
                self.moves.remove(self.moves[0])
                self.direction = pygame.Vector2((0,0))
                self.moving = False
                self.moved = 0

        self.collission('horizontal')
        self.perception.center = self.rect.center
    
    
    def found_resource(self, resource):
        if not resource in self.found_resources:
            self.found_resources.append(resource)
    
    def collission(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.perception): ## diferenciar de recurso depois
                if isinstance(sprite, FogOfWar):
                    sprite.disapearing = True
                if isinstance(sprite, Resource):
                    if sprite.value <= self.limit:
                        self.found_resource(sprite)
                        
        pass
    
        
    def update(self, delta_time):
        m_pos_x = int(self.rect.topright[0]/TILE_SIZE)
        m_pos_y = int(self.rect.bottomright[1]/TILE_SIZE)
        self.m_position = (m_pos_x, m_pos_y)
        self.move(delta_time)
        self.animate(delta_time)
        self.speed = self.game.agent_speed
        # self.game.camera.position = pygame.Vector2((self.rect.center))
    
    def load_images(self):
        self.display_surface = pygame.display.get_surface()
        sheet_width, sheet_height = self.spritesheet.get_size()
        frames_per_row = sheet_width // self.size

        states = self.frames.keys()

        for i, state in enumerate(states):
            self.frames[state] = []
            for frame in range(frames_per_row):
                x = frame * self.size
                y = i * self.size
                frame_surface = self.spritesheet.subsurface(pygame.Rect(x, y, self.size, self.size))
                frame_surface = pygame.transform.scale(frame_surface, (TILE_SIZE, TILE_SIZE))
                self.frames[state].append(frame_surface)

    def animate(self, delta_time):
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'
            
        self.frame_index += 8 * delta_time
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])] 
        
        if not self.direction:
            self.frame_index = 1