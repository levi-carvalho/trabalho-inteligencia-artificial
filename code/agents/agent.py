from settings import *

class Agent(pygame.sprite.Sprite):
    def __init__(self, size, position, spritsheet, groups, collision_sprites, *agrs):
        super().__init__(groups)
        self.size = size
        self.base_pos = position - pygame.Vector2(32,32)
        self.spritesheet = spritsheet
        self.frames = {'down': [], 'left': [], 'right': [], 'up': []}
        
        self.load_images()
        self.image = self.frames['down'][0]
        self.rect = self.image.get_frect(center = position)
        self.hitbox_rect = self.rect
        
        self.speed = 100
        self.direction = pygame.Vector2((0,0))
        self.state, self.frame_index = 'down', 0
        
        self.busy = False
        self.returning = False
        self.resource = None
        
        self.target = self.base_pos
        self.collision_sprites = collision_sprites
        self.layer_order = 3
        self.limit = 20
        
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        
    def move(self, delta_time):
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collission('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collission('vertical')
        
        self.rect.center = self.hitbox_rect.center
        
    def carry(self, sprite): #nome deveria ser deliver, parece que s´o executa quando chega na base
        if not self.busy and not sprite.holder:
            sprite.holder = self
            self.busy = True
            self.returning = True
            self.resource = sprite
            self.target = self.base_pos
            self.target_rect.center = self.base_pos
    
    def collission(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect) and sprite.value <= self.limit:
                self.carry(sprite)
                        
        self.rect.center = self.hitbox_rect.center
                    
                        
        pass
    
    def update(self, delta_time):
        # self
        # .input()
        self.move(delta_time)
        self.animate(delta_time)
    
    def load_images(self):
        
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