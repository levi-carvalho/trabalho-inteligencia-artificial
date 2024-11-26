from settings import *
from agents.objective_based import ObjectiveBased

class UtilityBased(ObjectiveBased):
    def __init__(self, size, position, sprite_sheet, groups, collision_sprites, objectives, utility_agents):
        super().__init__(size, position, sprite_sheet, groups, collision_sprites, objectives)
        self.colleagues = utility_agents
        self.objective = None
        self.limit = 50
        self.waiting = False
    
    def calc_objective(self):
        objectives = sorted(self.objectives, key = lambda objective: math.dist(objective.rect.center, self.rect.center))
        objectives = [objective for objective in objectives if (pygame.time.get_ticks() - objective.last_tried) >= objective.cooldown_duration]
        return objectives
    
    def calc_next_target(self):
        if self.waiting and self.objective:
            print(self.waiting, "waitt", pygame.time.get_ticks(), self.rect.center)
            print('objective = ', self.objective.groups())
            
            found_colleague = False
            for colleague in self.colleagues:
                if colleague.objective == self.objective:
                    if colleague != self:
                        found_colleague = True
                        print("truou")
                        break
            if not found_colleague:
                self.waiting = False
                self.objective.last_tried = pygame.time.get_ticks()                        
            
            if not self.objective or len(self.objective.groups()) == 0 or self.objective.holders > 1:
                self.waiting = False
            
            return
        
        objectives = self.calc_objective()
        
        while objectives[self.objective_index].holder:
            self.objective_index += 1
        
        self.objective = objectives[self.objective_index]
        self.target_rect = self.objective.rect
        self.objective_index = 0
        
        self.calc_direction()
    
    def carry(self, sprite):
        if sprite.value == 50:
            for colleague in self.colleagues:
                if colleague.objective == self.objective:
                    if colleague != self:
                        self.waiting = True
                        if math.dist(colleague.rect.center, self.rect.center) < 30:
                            self.set_returning(sprite, colleague)
                            self.set_returning(sprite, self)
                            self.waiting = False
                            
            if not self.waiting:
                sprite.last_tried = pygame.time.get_ticks()
                self.waiting = False
                
            
            return
        if not self.busy and not sprite.holder:
            self.set_returning(sprite, self)