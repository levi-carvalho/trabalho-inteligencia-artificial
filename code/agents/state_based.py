from settings import *
from agents.simple_reactive import SimpleReactive

class StateBased(SimpleReactive):
    def __init__(self, size, position, sprite_sheet, groups, collision_sprites):
        super().__init__(size, position, sprite_sheet, groups, collision_sprites)
        self.matrix = np.zeros(shape=(21,21))
        self.matrix_pos = pygame.Vector2(10,10)
        self.direction = pygame.Vector2((1,0))
        self.direction_index = 0
        self.directions = [
            pygame.Vector2(TILE_SIZE, 0),
            pygame.Vector2(0, TILE_SIZE),
            pygame.Vector2(-TILE_SIZE, 0),
            pygame.Vector2(0, -TILE_SIZE)
        ]
    
    def set_new_target(self):
        self.direction_index += 1
        current_x = int(self.rect.x//64)
        current_y = int(self.rect.y//64)
        self.matrix[current_x][current_y] = 1
        
        new_direction = self.directions[self.direction_index % 4]
        
        # print("new direction: ", new_direction//64)
        # print("current_position: ", current_x, current_y)
        # print("next position: ", new_direction//64 + [current_x, current_y])
        
        next_positions = new_direction//64 + [current_x, current_y]
        
        if self.matrix[int(next_positions[0])][int(next_positions[1])] == 1:
            self.direction_index -= 1
            new_direction = self.directions[self.direction_index % 4]
        
        self.target_rect = self.hitbox_rect.move(new_direction.x, new_direction.y)