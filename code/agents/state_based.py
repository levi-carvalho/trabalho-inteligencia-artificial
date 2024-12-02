from settings import *
from agents.simple_reactive import SimpleReactive

class StateBased(SimpleReactive):
    def __init__(self, size, position, spritesheet, game):
        super().__init__(size, position, spritesheet, game)
        self.matrix = np.zeros((self.game.map_size, self.game.map_size))
        self.direction = pygame.Vector2((1,0))
        self.direction_index = rd.randint(0,4)
        self.moviment_history = []
        self.directions = [
            pygame.Vector2(1, 0),
            pygame.Vector2(0, 1),
            pygame.Vector2(-1, 0),
            pygame.Vector2(0, -1),
        ]
        self.no_reference_steps = 0
        
    def fuck_around(self):
        # print('inputou')
        current_x, current_y = self.m_position
        
        self.matrix[current_y][current_x] = 1
        
        new_direction = self.directions[self.direction_index % 4]
        new_position = self.m_position + new_direction
        new_x, new_y = int(new_position[0]), int(new_position[1])
        
        if self.valid_move(new_x, new_y, new_direction): return
        if self.valid_adjascent(current_x, current_y): return
        if self.any_valid(new_x, new_y): return
        
        self.moves.append(new_direction)
        next_move = pygame.Vector2(new_direction)
        if not self.moviment_history[-1:] == [new_direction]:
            self.moviment_history.append(new_direction)
            self.check_repeated_moves()
        
        if self.no_reference_steps == 40:
            # print('aqui zerou')
            self.no_reference_steps = 0
            self.direction_index = rd.randint(0,4)
        self.no_reference_steps += 1
        # print("asd", pygame.time.get_ticks())


    
    def valid_move(self, new_x, new_y, new_direction):
        if (0 <= new_x < self.game.map_size and
            0 <= new_y < self.game.map_size and
            self.matrix[new_y][new_x] == 0 and
            self.game.matrix[new_y][new_x] != 0):
            self.m_position = pygame.Vector2(new_x, new_y)
            self.moves.append(new_direction)
            return True
        return False
    
    def valid_adjascent(self, current_x, current_y):
        for direction in self.directions:
            adj_x, adj_y = current_x + int(direction.x), current_y + int(direction.y)
            if (0 <= adj_x < self.game.map_size and
                0 <= adj_y < self.game.map_size and
                self.matrix[adj_y][adj_x] == 0 and
                self.game.matrix[adj_y][adj_x] != 0):
                self.m_position = pygame.Vector2(adj_x, adj_y)
                self.moves.append(direction)
                return True
        return False
    
    
    def any_valid(self, new_x, new_y):
        next_is_outside = 0 <= new_x < (self.game.map_size-1) and 0 <= new_y < (self.game.map_size-1)
        if not next_is_outside:
            self.direction_index += 1
            return True
        if self.game.matrix[new_y][new_x] == 0:
            self.direction_index += 1
            return True
        return False
    
    def check_repeated_moves(self, min_length=5):
        if len(self.moviment_history) < 2 * min_length:
            return False

        for length in range(min_length, len(self.moviment_history) // 2 + 1):
            seq1 = self.moviment_history[-2*length:-length]
            seq2 = self.moviment_history[-length:]
            
            if seq1 == seq2:
                self.direction_index += rd.randint(0,4)
                self.directions.reverse()
    # def print_adjacent_matrix(self):
    #     current_x, current_y = self.m_position
    #     print("Matriz adjacente:")

    #     matrix = []
    #     for dy in [-1, 0, 1]:
    #         row = []
    #         for dx in [-1, 0, 1]:
    #             adj_x, adj_y = current_x + dx, current_y + dy

    #             if 0 <= adj_x < self.game.map_size and 0 <= adj_y < self.game.map_size:
    #                 if dx == 0 and dy == 0:
    #                     row.append("A")
    #                 else:
    #                     row.append(int(self.matrix[adj_y][adj_x]))
    #             else:
    #                 row.append("X")
    #         matrix.append(row)

    #     for row in matrix:
    #         print(" ".join(map(str, row)))