# main del juego
import pygame
import sys 
import random

# 1. Inicializa Pygame
pygame.init()

# 2. Crea la ventana
ancho_ventana = 800
alto_ventana = 600
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("PIXIVIDAD")



# Creación de clases para el juego___________________________________
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("sprite-pixie/idle1-pixie-rigth.jpg").convert()
        self.image.set_colorkey((255, 255, 255))  # quita fondo blanco
        self.image = pygame.transform.scale(self.image, (90, 120))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.center = (x, y)
# Esta instrucción es en caso de que la caja de colisión sea diferente
#       self.rect.width = 100 y self.rect.height = 100,
        

# Clase del objeto a recolectar
class Objeto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("sprites-coins/sprite1-1.jpg").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
# ___________________________________________________________________

# Creamos al jugador
jugador = Jugador(400, 300) # Coordenadas de creación 
jugador.rect.bottom = 550 # Coordenadas al mandarlo al fondo 
grupo_jugador = pygame.sprite.GroupSingle(jugador)


#Esto en caso de que después de crearse se modifique el sprite individual
#   jugador.image = pygame.transform.scale(jugador.image, (80, 100))
#   jugador.rect = jugador.image.get_rect(center=jugador.rect.center)
# Esto es al crearlo que se le ponga una coordenada desde el inicio
#   jugador = Jugador(400, 580)


# Creamos el objeto
x_random = random.randint(0, ancho_ventana - 50)
objeto = Objeto(x_random, 30)
grupo_objetos = pygame.sprite.Group(objeto)

# Se inicia el reloj del juego para iniciarlo
clock = pygame.time.Clock()
corriendo = True


# Bucle principal del juego
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False


# Creación del fondo del juego 
    pantalla.fill((255, 250, 250)) #Color de la nieve
    pygame.draw.rect(pantalla, (180, 220, 255), (0, 550, 800, 50))

# Dibuja los sprites con el draw
    grupo_objetos.draw(pantalla)
    grupo_jugador.draw(pantalla)

# Actualizar la pantalla 
    pygame.display.flip()
    clock.tick(60)

# Cierra Pygame
pygame.quit()
sys.exit()

