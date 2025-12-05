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
fondo = pygame.transform.scale(
    pygame.image.load("fondo.jpg").convert(),
    (ancho_ventana, alto_ventana)
)
fondo_y = 0
vel_fondo = 3

# Imagen de intro
intro_img = pygame.image.load("INTRO3.jpg").convert()
intro_img = pygame.transform.scale(intro_img, (ancho_ventana, alto_ventana))

# Fuente
fuente = pygame.font.Font(None, 36)

# Variables globales
puntos = 0
juego_activo = True
mostrar_intro = True
victoria = False

# Melodía de fondo
pygame.mixer.music.load("melodia.mp3")
pygame.mixer.music.play(-1)  # -1 = loop infinito
pygame.mixer.music.set_volume(0.5)  # volumen opcional (0.0 a 1.0)



# ----------------------- CLASES ----------------------------
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

        # Movimiento normal
        self.velocidad = 3

        # Dirección actual ("right" o "left")
        self.direccion = "right"

        # SALTO
        self.vel_y = 0
        self.gravedad = 0.8
        self.en_suelo = True

        # DASH
        self.dash_vel = 50 #Antes 12
        self.dash_cooldown = 0
        self.dash_cooldown_max = 25 # frames de espera

    def mover(self, teclas):
        # ---------------- MOVIMIENTO HORIZONTAL ----------------
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
            self.image = self.image_derecha
            self.direccion = "right"

        elif teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
            self.image = self.image_izquierda
            self.direccion = "left"

        # ---------------- SALTO ----------------
        if teclas[pygame.K_UP] and self.en_suelo:
            self.vel_y = -15  # fuerza del salto
            self.en_suelo = False

        # ---------------- DASH ----------------
        if teclas[pygame.K_SPACE] and self.dash_cooldown == 0:
            if self.direccion == "right":
                self.rect.x += self.dash_vel
            else:
                self.rect.x -= self.dash_vel

            self.dash_cooldown = self.dash_cooldown_max

    def aplicar_gravedad(self):
        self.rect.y += self.vel_y
        self.vel_y += self.gravedad

        # Suelo a 550 (como tu juego)
        if self.rect.bottom >= 550:
            self.rect.bottom = 550
            self.vel_y = 0
            self.en_suelo = True

    def update(self):
        # reducir cooldown del dash
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        # gravedad siempre activa
        self.aplicar_gravedad()






class Objeto(pygame.sprite.Sprite):
    # Cargamos todos los sprites una sola vez (mejor rendimiento)
    sprites_cargados = []

    @staticmethod
    def cargar_sprites():
        if not Objeto.sprites_cargados:
            for i in range(1, 13):  # del 1 al 12
                ruta = f"sprites-coins/sprite1-{i}.jpg"
                try:
                    img = pygame.image.load(ruta).convert()
                    img.set_colorkey((255, 255, 255))
                    img = pygame.transform.scale(img, (30, 50))
                    Objeto.sprites_cargados.append(img)
                except:
                    print(f"No se encontró la imagen: {ruta}")

    def __init__(self, x, y, velocidad):
        super().__init__()

        # Cargar imágenes si aún no están cargadas
        Objeto.cargar_sprites()

        # Elegir sprite aleatorio
        self.image = random.choice(Objeto.sprites_cargados)
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidad_y = velocidad

    def update(self):
        self.rect.y += self.velocidad_y

        # Si toca el suelo, reaparece arriba CON OTRA IMAGEN
        if self.rect.bottom >= 550:
            nueva_x = random.randint(0, ancho_ventana - self.rect.width)
            self.rect.center = (nueva_x, 50)
            self.image = random.choice(Objeto.sprites_cargados)






class Fuego(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []
        for i in range(1, 6):
            img = pygame.image.load(f"sprites-fire/f{i}.jpg").convert()
            img.set_colorkey((255, 255, 255))
            img = pygame.transform.scale(img, (50, 60))
            self.frames.append(img)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidad_y = 4
        self.anim_speed = 0.15

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom >= 550:
            nueva_x = random.randint(0, ancho_ventana - self.rect.width)
            self.rect.center = (nueva_x, 50)

        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]


# ----------------------- FUNCIÓN REINICIAR ----------------------------
def reiniciar_juego():
    global puntos, juego_activo, mostrar_intro, victoria
    global grupo_jugador, grupo_objetos, grupo_fuego, jugador
    
    puntos = 0
    juego_activo = True
    victoria = False

    jugador = Jugador(400, 300)
    jugador.rect.bottom = 550
    grupo_jugador = pygame.sprite.GroupSingle(jugador)

    # Crear 3 objetos simultáneos con velocidades diferentes
    grupo_objetos = pygame.sprite.Group()
    for i in range(3):
        x = random.randint(0, ancho_ventana - 50)
        y = random.randint(20, 200)
        velocidad = random.randint(2, 6)
        grupo_objetos.add(Objeto(x, y, velocidad))

    # Crear fuego
    fuego_x = random.randint(0, ancho_ventana - 50)
    fuego = Fuego(fuego_x, 30)
    grupo_fuego = pygame.sprite.Group(fuego)


reiniciar_juego()
clock = pygame.time.Clock()


# ----------------------- GAME LOOP ----------------------------
corriendo = True
while corriendo:

    # ----------- PANTALLA DE INTRO -------------
    if mostrar_intro:
        pantalla.blit(intro_img, (0, 0))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mostrar_intro = False

        continue

    # ----------- EVENTOS GENERALES ------------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if not juego_activo and evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_rect.collidepoint(evento.pos):
                reiniciar_juego()

    # ----------- FONDO -------------
    fondo_y += vel_fondo
    if fondo_y >= alto_ventana:
        fondo_y = 0

    pantalla.blit(fondo, (0, fondo_y))
    pantalla.blit(fondo, (0, fondo_y - alto_ventana))

    pygame.draw.rect(pantalla, (180, 220, 255), (0, 550, 800, 50))


    # ----------- JUEGO ACTIVO -------------
    if juego_activo:
        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
        jugador.update()  # gravedad + cooldown del dash
        grupo_objetos.update()
        grupo_fuego.update()


        # Colisión con objetos buenos
        colisiones = pygame.sprite.spritecollide(jugador, grupo_objetos, dokill=True)
        if colisiones:
            puntos += 10

            # Agregar nuevo objeto
            x = random.randint(0, ancho_ventana - 50)
            velocidad = random.randint(2, 6)
            grupo_objetos.add(Objeto(x, 30, velocidad))

        # Win (500 puntos)
        if puntos >= 500:
            juego_activo = False
            victoria = True

        # Colisión con fuego → Game Over
        if pygame.sprite.spritecollide(jugador, grupo_fuego, dokill=False):
            juego_activo = False

        grupo_objetos.draw(pantalla)
        grupo_fuego.draw(pantalla)
        grupo_jugador.draw(pantalla)

        texto_puntos = fuente.render(f"Adornos: {puntos}", True, (0, 0, 0))
        pantalla.blit(texto_puntos, (20, 20))

    # ----------- GAME OVER / WIN -------------
    else:
        if victoria:
            texto_win = fuente.render("¡HAS GANADO!", True, (0, 150, 0))
            pantalla.blit(texto_win, (ancho_ventana//2 - 120, 200))
        else:
            texto_gameover = fuente.render("¡Vuelve a intentarlo!", True, (200, 0, 0))
            pantalla.blit(texto_gameover, (ancho_ventana//2 - 120, 200))

        texto_puntaje = fuente.render(f"Puntuación final: {puntos}", True, (0, 0, 0))
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



