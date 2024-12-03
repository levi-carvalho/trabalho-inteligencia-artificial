from settings import *
from agents.agent import Agent
import math
import random

class SimpleReactive(Agent):
    def __init__(self, size, position, spritesheet,game):
        super().__init__(size, position, spritesheet, game)
        self.returning = False
        self.waiting = False        
        self.directions = [
            pygame.Vector2(1, 0),
            pygame.Vector2(-1, 0),
            pygame.Vector2(0, 1),
            pygame.Vector2(0, -1)
        ]
        
        self.resource = None
    
    def fuck_around(self):
        curr_x = round(self.rect.center[0]/TILE_SIZE)
        curr_y = round(self.rect.center[1]/TILE_SIZE)
        curr_pos = pygame.Vector2((curr_x, curr_y))
        
        next_move = rd.choice(self.directions)
        next_position = curr_pos + next_move
        
        if next_position.x > (self.game.map_size - 1) or \
            next_position.y > (self.game.map_size - 1) or \
            next_position.x < 0 or \
            next_position.y < 0:
            return
        elif not self.game.matrix[int(next_position.y)][int(next_position.x)] == 0:
            self.moves.append(next_move)
    
    def define_resources_priority(self):
        self.found_resources = [resource for resource in self.found_resources if resource.value <= self.limit]
        return
    
    def take_resource(self):
        if self.found_resources[0].holder:
            self.found_resources.remove(self.found_resources[0])
            self.busy = False
            return
        self.define_path_to(self.game.base.m_position)
        self.returning = True
        self.resource.holders_list.append(self)
        self.resource.holder = self
    
    def define_target(self):
        if self.busy and not self.returning:
            self.take_resource()
        elif self.returning:
            self.found_resources.remove(self.resource)
            self.returning = False
            self.busy = False
            self.resource.kill()
            
        else:
            self.define_resources_priority()
            if len (self.found_resources) == 0: return
            if self.found_resources[0].holder:
                self.found_resources.remove(self.found_resources[0])
                return
            
            self.resource = self.found_resources[0]
            resource_position = self.resource.m_position
            self.define_path_to(resource_position)
            self.going_to_resource = True
            self.busy = True
            # print("definiu")
                
        # elif self.resource:
        #     print('k', pygame.time.get_ticks())
        #     agent_position = (int(self.rect.centerx/TILE_SIZE), int(self.rect.centery/TILE_SIZE))
        #     resource_position = (int(self.resource.rect.centerx/TILE_SIZE), int(self.resource.rect.centery/TILE_SIZE))
            
        #     if math.dist(agent_position, resource_position) < 2:
        #         base_pos = (int(self.game.base.rect.center[0]/TILE_SIZE), int(self.game.base.rect.center[1]/TILE_SIZE))
        #         self.define_path_to(base_pos)
        #         self.found_resources.remove(self.resource)
        #         self.resource.holder = self
        #         print('to base', pygame.time.get_ticks())
        #         self.resource.kill()
    # def on_reach_target(self):
    #     if self.resource:
    #         print(self.resource.rect.center, self.rect.center)
    #         print("aau")