from settings import *
from agents.objective_based import ObjectiveBased

class UtilityBased(ObjectiveBased):
    def __init__(self, size, position, sprite_sheet, groups, collision_sprites, objectives, utility_agents):
        super().__init__(size, position, sprite_sheet, groups, collision_sprites, objectives)
        self.colleagues = utility_agents
        self.objective = None
        self.limit = 50
        self.waiting = False
        
    def calc_next_target(self):
        if self.waiting:
            return
        
        objectives = sorted(self.objectives, key = lambda objective: math.dist(objective.rect.center, self.rect.center))
        objectives = [objective for objective in objectives if (pygame.time.get_ticks() - objective.last_tried) >= objective.cooldown_duration]
        
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
                else:
                    sprite.last_tried = pygame.time.get_ticks()
                    self.resource = None
            return
        if not self.busy and not sprite.holder:
            sprite.holder = self
            self.busy = True
            self.returning = True
            self.resource = sprite
            self.target = self.base_pos
            self.target_rect.center = self.base_pos
        
# o agente cooperativo vai encontrar o bagulho grande, vai pegar todos os outros agentes cooperativos e vai mandar um agente.help_me()
#    eles vão responder True  ou False dependendo das condições (ocupado e distância)
# se todos os agentes responderem False o agente vai pro objetivo mais próximo

## cooldown de tentativa, sei lá

## holding = 0/2, 1/2, 2/2
## holders = []
## o item carregado vai ficar na distância média entre os dois agentes

## verifica se o objetivo de algum outro agente cooperativo também é o grandão