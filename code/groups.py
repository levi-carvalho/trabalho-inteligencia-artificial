from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2((0,0))
        
    def draw(self, target_pos):
        self.offset.x = -target_pos[0] + WINDOW_WIDTH /2
        self.offset.y = -target_pos[1] + WINDOW_HEIGHT /2
        
        # self.offset.x = 0
        # self.offset.y = 0
        
        sorted_sprites = sorted(self.sprites(), key=lambda sprite: (sprite.layer_order, sprite.rect.centery))

        for sprite in sorted_sprites:
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)
            pygame.draw.rect(self.display_surface, 'white', pygame.Rect(sprite.rect.left + self.offset.x, sprite.rect.top + self.offset.y, sprite.rect.width, sprite.rect.height), 1)
            
            if hasattr(sprite, 'perception'):
                pygame.draw.rect(self.display_surface, 'white', pygame.Rect(sprite.perception.left + self.offset.x, sprite.perception.top + self.offset.y, sprite.perception.width, sprite.perception.height), 4)