from settings import *
from sprites import CollisionSprite


class Resource(CollisionSprite):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)
        self.holders = 0
        self.cooldown_duration = 15000
        self.last_tried = -30000

class Crystal(Resource):
    def __init__(self, position, groups):
        
        surface = pygame.Surface((64, 64))
        
        super().__init__(position, surface, groups)
        
        self.position = position
        self.value = 10
        self.holder = None
        self.current_frame = 0
        self.load_images()
        
    def load_images(self):
        self.frames = []
        folder_path = path.join('..','crystal')
        
        for file_name in sorted(os.listdir(folder_path), key = lambda name: int(name.split('.')[0])):
            full_path = path.join(folder_path, file_name)
            image = pygame.image.load(full_path)
            image = pygame.transform.scale_by(image, 0.1)
            self.frames.append(image)
            
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_frect(center = self.position)
    
    
    def animate(self, delta_time):
        self.current_frame += uniform(0.2, 1.8) * delta_time
        self.image = self.frames[int(self.current_frame) % len(self.frames)]
        
    def update(self, delta_time, *args):
        self.animate(delta_time)
        if self.holder:
            self.rect.midbottom = self.holder.rect.midtop

class Metal(Crystal):
    def __init__(self, position, groups):
        super().__init__(position, groups)
        self.value = 20
    
    def load_images(self):
        image_path = path.join('..', 'mineral', 'Icon20.png')
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (52, 52))
        self.rect = self.image.get_frect(center = self.position)
    
    def animate(self, delta_time):
        pass
    
class AncientBuilding(Metal):
    def __init__(self, position, groups):
        super().__init__(position, groups)
        self.value = 50
        
    def load_images(self):
        images_path = path.join('..', 'fancient')
        image_path = path.join(images_path, (rd.choice(os.listdir(images_path))))
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_frect(midbottom = self.position)