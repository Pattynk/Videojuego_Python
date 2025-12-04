import pygame
import sys 
import random

pygame.init()

# Configuración de pantalla
ancho_ventana = 800
alto_ventana = 600
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("PIXIVIDAD")


# Fondo
# Fondo ajustado al tamaño de la ventana
fondo = pygame.transform.scale(
    pygame.image.load("fondo.jpg").convert(),
    (ancho_ventana, alto_ventana)
)
fondo_y = 0
vel_fondo = 3


# Fuente para texto
fuente = pygame.font.Font(None, 36)

# Variables del juego
puntos = 0
juego_activo = True  # Nuevo: indica si el juego sigue o está en "game over"

# Clases del juego______________________________________________________
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_derecha = pygame.image.load("sprite-pixie/idle1-pixie-rigth.jpg").convert()
        self.image_derecha.set_colorkey((255, 255, 255))
        self.image_derecha = pygame.transform.scale(self.image_derecha, (90, 120))

        self.image_izquierda = pygame.image.load("sprite-pixie/idle1-pixie-left.jpg").convert()
        self.image_izquierda.set_colorkey((255, 255, 255))
        self.image_izquierda = pygame.transform.scale(self.image_izquierda, (90, 120))

        self.image = self.image_derecha
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = 3

    def mover(self, teclas_presionadas):
        if teclas_presionadas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.image = self.image_derecha
        elif teclas_presionadas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.image = self.image_izquierda


class Objeto(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("sprites-coins/sprite1-1.jpg").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad_y = 3

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom >= 550:
            nueva_x = random.randint(0, ancho_ventana - self.rect.width)
            self.rect.center = (nueva_x, 50)


class Fuego(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Cargar todos los frames de animación
        self.frames = []
        for i in range(1, 6):  # f1 a f5
            img = pygame.image.load(f"sprites-fire/f{i}.jpg").convert()
            img.set_colorkey((255, 255, 255))
            img = pygame.transform.scale(img, (50, 60))
            self.frames.append(img)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidad_y = 4
        self.anim_speed = 0.15  # velocidad de animación, entre más alto el valor, la animación va más rápidito

    def update(self):
        # Movimiento hacia abajo
        self.rect.y += self.velocidad_y
        if self.rect.bottom >= 550:
            nueva_x = random.randint(0, ancho_ventana - self.rect.width)
            self.rect.center = (nueva_x, 50)

        # Animación (cambiar frame)
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]


# _______________________________________________________________________

def reiniciar_juego():
    global puntos, juego_activo, grupo_objetos, grupo_fuego, jugador, grupo_jugador
    puntos = 0
    juego_activo = True
    # Recrear jugador y objetos
    jugador = Jugador(400, 300)
    jugador.rect.bottom = 550
    grupo_jugador = pygame.sprite.GroupSingle(jugador)

    x_random = random.randint(0, ancho_ventana - 50)
    objeto = Objeto(x_random, 30)
    grupo_objetos = pygame.sprite.Group(objeto)

    fuego_x = random.randint(0, ancho_ventana - 50)
    fuego = Fuego(fuego_x, 30)
    grupo_fuego = pygame.sprite.Group(fuego)

# Inicialización de sprites
reiniciar_juego()

# Reloj del juego
clock = pygame.time.Clock()
corriendo = True

# Game Loop
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        # Si el juego terminó, detectar clic en el botón
        if not juego_activo and evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(evento.pos):
                reiniciar_juego()

    # Mover fondo hacia abajo
    fondo_y += vel_fondo
    if fondo_y >= alto_ventana:
        fondo_y = 0


    # Dibujar fondo cayendo
    pantalla.blit(fondo, (0, fondo_y))
    pantalla.blit(fondo, (0, fondo_y - alto_ventana))

    pygame.draw.rect(pantalla, (180, 220, 255), (0, 550, 800, 50))

    if juego_activo:
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)

        grupo_objetos.update()
        grupo_fuego.update()
        jugador.rect.bottom = 550

        # Colisión con objetos buenos
        colisiones = pygame.sprite.spritecollide(jugador, grupo_objetos, dokill=True)
        if colisiones:
            puntos += 10
            nueva_x = random.randint(0, ancho_ventana - 50)
            nuevo_objeto = Objeto(nueva_x, 30)
            grupo_objetos.add(nuevo_objeto)

        # Colisión con fuego → fin del juego
        if pygame.sprite.spritecollide(jugador, grupo_fuego, dokill=False):
            juego_activo = False

        # Dibujo de sprites
        grupo_objetos.draw(pantalla)
        grupo_fuego.draw(pantalla)
        grupo_jugador.draw(pantalla)

        # Puntuación
        texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
        pantalla.blit(texto_puntos, (20, 20))

    else:
        # Pantalla de Game Over
        texto_gameover = fuente.render("¡Vuelve a intentarlo!", True, (200, 0, 0))
        texto_puntaje = fuente.render(f"Puntuación final: {puntos}", True, (0, 0, 0))
        pantalla.blit(texto_gameover, (ancho_ventana//2 - 120, 200))
        pantalla.blit(texto_puntaje, (ancho_ventana//2 - 110, 250))

        # Botón Reiniciar
        boton_rect = pygame.Rect(ancho_ventana//2 - 70, 320, 140, 50)
        pygame.draw.rect(pantalla, (100, 180, 255), boton_rect)
        texto_boton = fuente.render("Reiniciar", True, (255, 255, 255))
        pantalla.blit(texto_boton, (ancho_ventana//2 - 45, 335))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

pygame.quit()
sys.exit()


