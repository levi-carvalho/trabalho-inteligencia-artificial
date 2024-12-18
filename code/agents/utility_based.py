from settings import *
from agents.objective_based import ObjectiveBased

class UtilityBased(ObjectiveBased):
    def __init__(self, size, position, sprite_sheet, game):
        super().__init__(size, position, sprite_sheet, game)
        self.colleagues = game.utility_agents
        self.limit = 50
        self.waiting = False
        self.set_perception(3)
        game.utility_agents.add(self)
        
    def define_resources_priority(self):
        current_time = pygame.time.get_ticks()
        self.found_resources = sorted(self.found_resources, key=lambda r: (not(current_time - r.last_tried) > r.cooldown_duration, self.calculate_moves(self.m_position, r.m_position) + self.calculate_moves(self.game.base.m_position, r.m_position)))
        return
    
    def take_resource(self):

        if not self.found_resources:
            # print("Nenhum recurso encontrado.")
            self.busy = False
            return

        resource = self.found_resources[0]
        if resource.holder:
            # print("ja holde")
            self.found_resources.remove(resource)
            self.busy = False
            return

        found_colleague = False
        current_time = pygame.time.get_ticks()
        if resource.value == self.limit:
            if (current_time - resource.last_tried) > resource.cooldown_duration:
                for colleague in self.colleagues:
                    if colleague != self:
                        if not resource in colleague.found_resources:
                            colleague.found_resources.append(resource)
                            # print("colocou no do colega")
                        else:
                            # print("não colocou no do colega")
                            pass
                            
                        # print('ai', pygame.time.get_ticks())             
                        if colleague.found_resources[0] == resource:
                            found_colleague = True
                            # print("esperando")
                            if colleague.m_position == self.m_position:
                                    
                                self.define_path_to(self.game.base.m_position)
                                resource.holders_list.append(self)
                                self.returning = True
                                resource.holder = self
                                
                                colleague.moves = []
                                colleague.moves.append(pygame.Vector2(0,0))
                                
                                for move in  self.moves:
                                    colleague.moves.append(pygame.Vector2(move.x, move.y))
                                resource.holders_list.append(colleague)
                                colleague.returning = True
                                resource.holder = self
                                break
                            
                if not found_colleague:
                    # print("Não encontrou colega")
                    resource.last_tried = current_time
                    self.fuck_around()
                    # self.define_path_to(self.m_position)
                    self.busy = False
                    return

        else:
            # print('pegou')
            self.define_path_to(self.game.base.m_position)
            self.returning = True
            self.resource.holders_list.append(self)
            resource.holder = self
            return