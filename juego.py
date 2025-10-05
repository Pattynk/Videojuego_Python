# Este es un ejemplo básico del código
import pygame

# 1. Inicializa Pygame
pygame.init()

# 2. Crea la ventana
ancho_ventana = 800
alto_ventana = 600
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Mi Primer Juego")

# 3. Bucle principal del juego
corriendo = True
while corriendo:
    # 4. Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # 5. Dibuja en la pantalla (por ejemplo, llena de negro)
    pantalla.fill((0, 0, 0))

    # 6. Actualiza la pantalla
    pygame.display.flip()

# 7. Cierra Pygame
pygame.quit()
