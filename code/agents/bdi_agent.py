from settings import *
from agents.utility_based import UtilityBased

class BDIAgent(UtilityBased):
    def __init__(self, size, position, sprite_sheet, game):
        super().__init__(size, position, sprite_sheet, game)
    
    def define_resources_priority(self):
        current_time = pygame.time.get_ticks()
        self.found_resources = sorted(
            self.found_resources,
            key=lambda r: (
                not(current_time - r.last_tried) > r.cooldown_duration,
                    (self.calculate_moves(self.m_position, r.m_position) +
                    self.calculate_moves(self.game.base.m_position, r.m_position))/r.value
                )
            )
        return              
    # def calc_objective(self):
    #     objectives = sorted(self.objectives, key = lambda objective: math.dist(objective.rect.center, self.base_pos)//objective.value)
    #     objectives = [objective for objective in objectives if (pygame.time.get_ticks() - objective.last_tried) >= objective.cooldown_duration]
    #     return objectives