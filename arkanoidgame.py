import pygame

pygame.init()


#inicializa el modulo para la musica
pygame.mixer.init()

pygame.mixer.music.load('')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
#se carga la musica de fondo y se reproduce en bucle infinito


sonido_barra= pygame.mixer.Sound('bounce.mp3')
sonido_barra.set_volume(0.5)

sonido_game_over= pygame.mixer.Sound()

#ancho y alto de la ventana
width, height = 800,600
#Colores en RGB
blanco = (255, 255, 255)
negro = (0, 0, 0)
azul = (0, 0, 255)
rojo = (255, 0, 0)

#radio del baloncito
r_balon = 10

#borde de la ventana
b_ventana_w = 8 
b_ventana_h = 8
vel_balon = 5

#dimensiones de la barra
barrita_w = 100
barrita_h = 10

#ladrillos
ladrillo_w = 60
ladrillo_h = 20

#aca definimos  cual va ser la cantidad de filas y columnas a mostrar
filas_lad = 8
columnas_lad = 10
#-----------------------------------------------

#centrar la barra
pos_barra = [width // 2 - barrita_w // 2, height - barrita_h] # se centra dividiendo en 2 la medida de la ventana y la barrita(ancho)
barrita_v = 10
#posicion inicial del balon
pos_balon = [width // 2, height // 2] #justo en el centro de la ventana
balon_vel = [vel_balon, -vel_balon]

ventana= pygame.display.set_mode((width,height))#aca definimos el tamaño de la ventana
pygame.display.set_caption("Arkanoid game")# nombramos el nombre del juego en la esquina ixquierda de la ventana
reloj= pygame.time.Clock()

ladrillos=[]
##organizar los ladrillos en filas y columnas
for i in range(filas_lad):
    fila= []
    
    for x in range(columnas_lad):
        pos_lad_x= x * (ladrillo_w + 10) +35 #el 35 es cuanto se desplaza y el 10 es el espacio que se deja
        pos_lad_y = i* (ladrillo_h +8)+50 # funciona igual pero verticalmente

        fila.append((pos_lad_x,pos_lad_y))
    
    ladrillos.append(fila)

#aca lo que hicimos fue la matriz de las ubicaciones de los ladrillos
#lo imprimo para que observen la matriz
for fila in ladrillos:
    print(fila)



#el canvas se refere en donde voy a dibujar, en este caso seria en la ventana
def interfaz(canvas):

    pygame.draw.rect(canvas,azul, (pos_barra[0], pos_barra[1], barrita_w, barrita_h))
    pygame.draw.circle(canvas,rojo,(int(pos_balon[0]), int(pos_balon[1])), r_balon)

    #dibujar los ladrillitos
    for fila in ladrillos:
        for ladrillo in fila:
            pygame.draw.rect(canvas, blanco, (ladrillo[0], ladrillo[1], ladrillo_w, ladrillo_h))
            
def rebotes_balon():

    #actualizar la posicion
    pos_balon[0] += balon_vel[0]
    pos_balon[1] += balon_vel[1]
    # esta posicion se actualiza sumando la velocidad del balon en x y en Y
    #pos_balon[0] es la coordenada x en la bola
    #pos_balon[1] es la coordenada en y de la bola
    # funciona igual con la velocidad

    #Los rebotes en las paredes
    if pos_balon[0] <= r_balon or pos_balon[0] >= width - r_balon:
        balon_vel[0] = -balon_vel[0]
    if pos_balon[1] <= r_balon:
        balon_vel[1] = -balon_vel[1]
    # esto significa que si la posicion del balon es igual o mayor al ancho de la pantalla, se invierte la vel del eje
    #es decir va hacia el lado contrario
    #con el eje y se maneja a partir de la bola, si la posicion en y es menor o igual al radio entonces se invierte la vel del eje

    #si rebota en la barra:
    if pos_barra[1] <= pos_balon[1] + r_balon <= pos_barra[1] + barrita_h:
        #con esto asegura que esta en el rango de la barrita, entre el tope superior y el inferior
        if pos_barra[0] <= pos_balon[0] <= pos_barra[0] + barrita_w:
            balon_vel[1] = -balon_vel[1]
            sonido_barra.play()
            #invierte hacia donde va el balon (iba hacia abajo ahora va hacia arriba)

    #si el balon esta en el filo inferior se acaba el juego
    if pos_balon[1] >= height:
        return True #para que el juego termine

    #ahora los puntos 
    balon_rect = pygame.Rect(pos_balon[0] - r_balon, pos_balon[1] - r_balon, 2 * r_balon, 2 * r_balon)
    #el rect representa el area del balon
    for fila in ladrillos:
        for ladrillo in fila:
            #de igual forma se hace con el ladrillo
            ladrillo_rect = pygame.Rect(ladrillo[0], ladrillo[1], ladrillo_w, ladrillo_h)
            #se verifica si lo golpea:
            if balon_rect.colliderect(ladrillo_rect):
                #se invierte la velocidad
                balon_vel[1] = -balon_vel[1]
                fila.remove(ladrillo)
                break
    return False

def salida():
    ventana.fill(negro) #rellena la pantalla de negro 
    font = pygame.font.SysFont(None, 60)
    # Renderiza el texto "Game Over"
    texto = font.render("Game Over", True,rojo)
    # Obtiene el rectángulo del texto
    texto_ubi = texto.get_rect(center=(width // 2, height // 2))

    #dice que presione una tecla para salir
    texto_salir= font.render("Presiona una tecla para salir",True,blanco)
    texto_salir_ubi=texto_salir.get_rect(center=(width//2,height//2+100))

    # Dibuja el texto en la pantalla
    ventana.blit(texto, texto_ubi)
    ventana.blit(texto_salir,texto_salir_ubi)
    pygame.display.update()  # Actualiza la pantalla

    pygame.time.wait(2000)  # Espera 2 segundos para que el jugador vea el mensaje

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            elif evento.type == pygame.KEYDOWN:
                pygame.quit()

def inicio():
    ventana.fill(negro)  # Rellena la pantalla de negro
    font = pygame.font.SysFont(None, 55)
    # Renderiza el texto "Presiona una tecla para comenzar"
    texto_inicio = font.render("Presiona una tecla para comenzar", True, blanco)
    # Obtiene el rectángulo del texto
    text_rect = texto_inicio.get_rect(center=(width // 2, height // 2))
    # Dibuja el texto en la pantalla
    ventana.blit(texto_inicio, text_rect)
    
    pygame.display.update()  # Actualiza la pantalla

    # Espera a que se presione la tecla
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                return  # Sale del bucle y comienza el juego

def ganador():
    ventana.fill(negro)  # Rellena la pantalla de negro
    font = pygame.font.SysFont(None, 150)
    # Renderiza el texto "Presiona una tecla para comenzar"
    texto_inicio = font.render("GANASTE !!!", True, blanco)
    # Obtiene el rectángulo del texto
    text_rect = texto_inicio.get_rect(center=(width // 2, height // 2))
    # Dibuja el texto en la pantalla
    ventana.blit(texto_inicio, text_rect)
    
    pygame.display.update()  # Actualiza la pantalla

    # Espera a que se presione la tecla
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
            if evento.type == pygame.KEYDOWN:
                return  # Sale del bucle y comienza el juego


#inicializar el juego:
inicio()

game_over = False
espera = True
while not game_over:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()

    ventana.fill(negro)
    interfaz(ventana)
    pygame.display.update()
    reloj.tick(60) #limite de FPS 60

    while espera == True:
        pygame.time.wait(800) 
        espera = False

    if len(ladrillos)== 0:
        ganador()
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        pos_barra[0] -= barrita_v 
    if keys[pygame.K_RIGHT]:
        pos_barra[0] += barrita_v
    
    if pos_barra[0] < 0:
        pos_barra[0] = 0  # Limita el borde izquierdo

    elif pos_barra[0] > width - barrita_w - b_ventana_w:
        pos_barra[0] = width - barrita_w - b_ventana_w  # Limita el borde derecho

    #sirve para mantener a la barrita dentro de los limites, calcula el max entre la barrita y lo minimo de la resta de los anchos
    if rebotes_balon():
        game_over = True

    if game_over:
        pygame.mixer.music.stop()

        salida()
        pygame.quit()
        



