from settings import *
from agents.simple_reactive import SimpleReactive

class ObjectiveBased(SimpleReactive):
    def __init__(self, size, position, sprite_sheet, groups, collision_sprites, objectives):
        super().__init__(size, position, sprite_sheet, groups, collision_sprites)
        
# o agente cooperativo vai encontrar o bagulho grande, vai pegar todos os outros agentes cooperativos e vai mandar um agente.help_me()
#    eles vão responder True  ou False dependendo das condições (ocupado e distância)
# se todos os agentes responderem False o agente vai pro objetivo mais próximo

## cooldown de tentativa, sei lá

## holding = 0/2, 1/2, 2/2
## holders = []
## o item carregado vai ficar na distância média entre os dois agentes

## verifica se o objetivo de algum outro agente cooperativo também é o grandão