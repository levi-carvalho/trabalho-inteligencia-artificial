from settings import *
from agents.simple_reactive import SimpleReactive

class ObjectiveBased(SimpleReactive):
    def __init__(self, size, position, sprite_sheet, groups, collision_sprites, objectives):
        super().__init__(size, position, sprite_sheet, groups, collision_sprites)
        self.objectives = objectives        
        self.objective_index = 0
    
    
    def calc_direction(self):
        best_direction = None
        min_distance = float('inf')
        
        for direction in self.directions:
            next_position = self.rect.center + direction
            distance_to_target = math.dist(self.target_rect.center,next_position)

            if distance_to_target < min_distance:
                min_distance = distance_to_target
                best_direction = direction

        self.target_rect = self.hitbox_rect.move(best_direction.x, best_direction.y)
        
    def calc_next_target(self):
        
        objectives = sorted(self.objectives, key = lambda objective: math.dist(objective.rect.center, self.rect.center))
        objectives = [sprite for sprite in objectives if sprite.value < 50]
        
        while objectives[self.objective_index].holder:
            self.objective_index += 1
        
        self.objective = objectives[self.objective_index]
        self.target_rect = self.objective.rect
        self.objective_index = 0
        
        self.calc_direction()
        
    
    def set_new_target(self):
        self.calc_next_target()