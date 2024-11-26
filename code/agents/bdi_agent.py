from settings import *
from agents.utility_based import UtilityBased

class BDIAgent(UtilityBased):
    def __init__(self, size, position, sprite_sheet, groups, collision_sprites, objectives, utility_agents):
        super().__init__(size, position, sprite_sheet, groups, collision_sprites, objectives, utility_agents)
    
    def calc_objective(self):
        objectives = sorted(self.objectives, key = lambda objective: math.dist(objective.rect.center, self.rect.center)//objective.value)
        objectives = [objective for objective in objectives if (pygame.time.get_ticks() - objective.last_tried) >= objective.cooldown_duration]
        return objectives