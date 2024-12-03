from settings import *
from agents.state_based import StateBased

class ObjectiveBased(StateBased):
    def __init__(self, size, position, spritesheet, game):
        super().__init__(size, position, spritesheet, game)
        
    def calculate_moves(self, start, end):
        grid = Grid(matrix=self.game.matrix)
        start = grid.node(start[0], start[1])
        end = grid.node(end[0], end[1])
        finder = AStarFinder()
        
        path, runs = finder.find_path(start, end, grid)
        return len(path)
        
    def define_resources_priority(self):
        self.found_resources = sorted(self.found_resources, key= lambda resource: self.calculate_moves(self.m_position, resource.m_position))