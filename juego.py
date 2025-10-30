import pygame
import sys 
import random

# Inicializa Pygame
pygame.init()

# Crea la ventana
ancho_ventana = 800
alto_ventana = 600
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("PIXIVIDAD")

# Se agregarán los puntos, por lo que se requiere un estilo para los letreros, tipo y tamaño
fuente = pygame.font.Font(None, 36)

# Se crea la variable que servirá como contador de los puntos obtenidos al colisionar con el objeto
puntos = 0


# Creación de clases para el juego___________________________________
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Avanzar a la derecha
        self.image_derecha = pygame.image.load("sprite-pixie/idle1-pixie-rigth.jpg").convert()
        self.image_derecha.set_colorkey((255, 255, 255))  # quita fondo blanco
        self.image_derecha = pygame.transform.scale(self.image_derecha, (90, 120))

        # Avanzar a la izquierda
        self.image_izquierda = pygame.image.load("sprite-pixie/idle1-pixie-left.jpg").convert()
        self.image_izquierda.set_colorkey((255, 255, 255))
        self.image_izquierda = pygame.transform.scale(self.image_izquierda, (90, 120))

        self.image = self.image_derecha
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 3
        # Esta instrucción es en caso de que la caja de colisión sea diferente
        # self.rect.width = 100 y self.rect.height = 100,


    # Movimiento con los inputs del teclado
    def mover(self, teclas_presionadas):
        if teclas_presionadas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.image = self.image_derecha
        elif teclas_presionadas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.image = self.image_izquierda


# Clase del objeto a recolectar
class Objeto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("sprites-coins/sprite1-1.jpg").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad_y = 3

    # Movimiento hacia abajo
    def update(self):
        self.rect.y += self.velocidad_y

        # Si toca el piso, reinicia arriba con nueva X aleatoria
        if self.rect.bottom >= 550:
            nueva_x = random.randint(0, ancho_ventana - self.rect.width)
            self.rect.center = (nueva_x, 50)     
   
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
    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    jugador.mover(teclas)

    # Actualización de lógica
    grupo_objetos.update()
    jugador.rect.bottom = 550

    # Detectar colisión entre jugador y objeto
    colisiones = pygame.sprite.spritecollide(jugador, grupo_objetos, dokill=True)
    if colisiones:
        puntos += 10  # Sumar puntos

        # Reaparece un nuevo objeto arriba después de tocar a pixie
        nueva_x = random.randint(0, ancho_ventana - 50)
        nuevo_objeto = Objeto(nueva_x, 30)
        grupo_objetos.add(nuevo_objeto)


    # Creación del fondo del juego 
    pantalla.fill((255, 250, 250)) #Color de la nieve
    pygame.draw.rect(pantalla, (180, 220, 255), (0, 550, 800, 50))

    # Dibuja los sprites con el draw
    grupo_objetos.draw(pantalla)
    grupo_jugador.draw(pantalla)

    # Mostrar puntuación
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
    pantalla.blit(texto_puntos, (20, 20))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

# Cierra Pygame
pygame.quit()
sys.exit()

