from settings import *
from agents.agent import Agent
import math
import random

class SimpleReactive(Agent):
    def __init__(self, size, position, sprite_sheet, groups, collision_sprites):
        super().__init__(size, position, sprite_sheet, groups, collision_sprites)
        
        self.last_position = self.rect.center
        self.waiting = False
        # self.moving = True
        
        self.target = pygame.Vector2(self.rect.centerx, self.rect.centery) + pygame.Vector2(TILE_SIZE, 0)
        self.target_surf = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.target_rect = self.target_surf.get_frect(center = self.target)
        self.directions = [
            pygame.Vector2(TILE_SIZE, 0),
            pygame.Vector2(-TILE_SIZE, 0),
            pygame.Vector2(0, TILE_SIZE),
            pygame.Vector2(0, -TILE_SIZE)
        ]
    
    def set_new_target(self):
        new_direction = random.choice(self.directions)
        self.target_rect = self.hitbox_rect.move(new_direction.x, new_direction.y)
    
    def fuck_around(self):
        self.direction.x = 1 if self.target_rect.centerx > self.hitbox_rect.centerx else -1 if self.target_rect.centerx < self.hitbox_rect.centerx else 0
        self.collission('horizontal')
        self.direction.y = 1 if self.target_rect.centery > self.hitbox_rect.centery else -1 if self.target_rect.centery < self.hitbox_rect.centery else 0
        self.collission('vertical')

        if math.dist(self.hitbox_rect.center, self.target_rect.center) < 1:
            self.hitbox_rect.center = self.target_rect.center
            self.direction = pygame.Vector2(0, 0)
            self.set_new_target()
            
    def return_to_base(self):
        if abs(self.base_pos.x - self.hitbox_rect.centerx) >= 1:
            self.direction.x = (self.base_pos.x > self.hitbox_rect.centerx) - (self.base_pos.x < self.hitbox_rect.centerx)
        elif abs(self.base_pos.y - self.hitbox_rect.centery) >= 1:
            self.direction.y = (self.base_pos.y > self.hitbox_rect.centery) - (self.base_pos.y < self.hitbox_rect.centery)
        
        if math.dist(self.hitbox_rect.center,self.base_pos) < 2:
            if self.resource:
                self.resource.kill()
            self.busy = False
            self.resource = None
            self.waiting = False
            self.returning = False
            self.direction = pygame.Vector2((0,0))
            self.last_position = self.base_pos
    
    def define_direction(self):
        self.target_surf.fill('pink')
        pygame.display.get_surface().blit(self.target_surf, self.target_rect)
        
        self.direction.x = 0
        self.direction.y = 0
        
        if not self.returning:
            self.fuck_around()
        else:
            self.return_to_base()
                
    def move(self, delta_time):
        self.define_direction()
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
            
        self.rect.center = self.hitbox_rect.center