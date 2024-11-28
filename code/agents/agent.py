from settings import *

class Agent(pygame.sprite.Sprite):
    def __init__(self, size, position, game, *agrs):
        super().__init__(game.all_sprites)
        self.game = game
        self.size = size
        self.spritesheet = self.game.surfaces['state_based']
        self.collision_sprites = game.collision_sprites
        self.base_pos = position
        self.frames = {'down': [], 'left': [], 'right': [], 'up': []}
        
        self.load_images()
        self.image = self.frames['down'][0]
        self.rect = self.image.get_frect(topleft = position)
        self.direction = pygame.Vector2((0,0))
        
        self.hitbox = self.rect
        
        self.speed = 100
        self.state, self.frame_index = 'down', 0
        
        self.layer_order = 3
        
        self.moves = []
        self.moving = False
        self.moved = 0
        
    def input(self):
        if pygame.mouse.get_pressed()[0]:
            offset_x =  - self.game.camera.position[0] + WINDOW_WIDTH / 2
            offset_y =  - self.game.camera.position[1] + WINDOW_HEIGHT / 2
            offset = pygame.Vector2((offset_x, offset_y))
            
            mouse_position = pygame.Vector2(pygame.mouse.get_pos())
            self_center = pygame.Vector2(self.rect.center)
            
            # print(mouse_position - offset, self_center)
            distance = (mouse_position - offset - self_center) /TILE_SIZE
            
            print(round(distance[0]), round(distance[1]))
            
        if len(self.moves) > 0:
            return
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        
        if self.direction.x > 0:
            self.moves.append(pygame.Vector2(1,0))
            self.moves.append(pygame.Vector2(-1,0))
            self.moves.append(pygame.Vector2(0,1))
            self.moves.append(pygame.Vector2(0,-1))
            self.moves.append(pygame.Vector2(-1,0))
            self.moves.append(pygame.Vector2(0,1))
            self.moves.append(pygame.Vector2(0,-1))
            self.moves.append(pygame.Vector2(-1,0))
            self.moves.append(pygame.Vector2(0,1))
            self.moves.append(pygame.Vector2(0,-1))
            self.moves.append(pygame.Vector2(-1,0))
            self.moves.append(pygame.Vector2(0,1))
            self.moves.append(pygame.Vector2(0,-1))
            self.moves.append(pygame.Vector2(-1,0))
            self.moves.append(pygame.Vector2(0,1))
            self.moves.append(pygame.Vector2(0,-1))
        elif self.direction.x < 0:
            self.moves.append(pygame.Vector2(-1,0))
        elif self.direction.y > 0:
            self.moves.append(pygame.Vector2(0,1))
        elif self.direction.y < 0:
            self.moves.append(pygame.Vector2(0,-1))
            
        self.direction = self.direction.normalize() if self.direction else self.direction
        
    def move(self, delta_time):
        
        if not self.moving:
            if len(self.moves) > 0:
                print(self.moves)
                self.direction = self.moves[0]
                self.moving = True
        else:
            self.hitbox.x += self.direction.x * self.speed * delta_time
            self.collission('horizontal')
            self.hitbox.y += self.direction.y * self.speed * delta_time
            self.collission('vertical')
            
            self.moved += self.speed * delta_time
            
            if self.moved >= 64:
                self.moves.remove(self.moves[0])
                self.moving = False
                self.moved = 0
        
        self.rect.center = self.hitbox.center
    
    def collission(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox) and sprite.value <= self.limit:
                # self.carry(sprite)
                pass
                        
        self.rect.center = self.hitbox.center
                    
                        
        pass
    
    def update(self, delta_time):
        self.input()
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