import pygame, sys, random, time

#Variables importantes
validChars = "abcdefghijklmnñopqrstuvwxyz"
shiftChars = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
WIDTH=650
HEIGHT=650
BLACK=(0,0,0) #Black color
WHITE=(255,255,255) #White color
GREEN=(0,255,0) #Green color
RED=(255,0,0) #Red color

pygame.init() #Initialize pygame
pygame.font.init() #Initialize font
pygame.mixer.init() #initialize pygame mixer (Music/sound)
screen= pygame.display.set_mode((WIDTH, HEIGHT)) #Set screen
pygame.display.set_caption("OPERATION MOON LIGHT") #Set window name
clock = pygame.time.Clock() #Set FPS clock

#Arreglar
naveprincipal = pygame.image.load("assets/blueship.png")
spriteasteroide=pygame.image.load("assets/bullet.png")
fondojuego = pygame.image.load("assets/spacebg3.png")
fuenteletra = pygame.font.match_font("Arial", 15)
puntuacion = 0
segundo = 0
cronometro=0
nivel =1
facil=True
normal=False
dificil=False

#Functions
#Draw text on the screen
def draw_text(surface, text, size, x, y):
    font= pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect =  text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


#CLASSES

class Jugador(pygame.sprite.Sprite):
    # Sprite del jugador
    def __init__(self):
        super().__init__()
        # jugador
        self.image = naveprincipal
        # Obtiene el rectángulo (sprite)
        self.rect = self.image.get_rect()
        self.rect.x = 325
        self.rect.y = 600
        self.vidas = 3
        self.invencible = 1000
        self.ultimogolpe = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_RIGHT] and 650 > self.rect.right:
            self.rect.x += 6
        if teclas[pygame.K_LEFT] and self.rect.left > 50:
            self.rect.x -= 6
        if teclas[pygame.K_UP] and self.rect.top > 50:
            self.rect.y -= 6
        if teclas[pygame.K_DOWN] and 650 > self.rect.bottom:
            self.rect.y += 6

class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(spriteasteroide, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(650-self.rect.width)
        self.rect.y = 25
        self.velocidad=random.randrange(2, 8)
        self.derecha=True
        self.abajo=True

    def update(self):
        self.velocidadx = self.velocidad
        self.velocidady = self.velocidad
        if self.derecha:
            self.rect.x += self.velocidadx
        else: self.rect.x -= self.velocidadx
        if self.abajo:
            self.rect.y += self.velocidady
        else: self.rect.y -= self.velocidady
        if self.rect.right >650:
            self.velocidad=random.randrange(2, 8)
            self.derecha=False
        if self.rect.left < 0:
            self.velocidad = random.randrange(2, 8)
            self.derecha=True
        if self.rect.bottom > 650:
            self.velocidad = random.randrange(2, 8)
            self.abajo=False
        if self.rect.top < 25:
            self.velocidad = random.randrange(2, 8)
            self.abajo=True

#Set class for gamestate (Stages/Screens)
class GameState():
    def __init__(self):
        super().__init__()
        self.state= 'nameScreen'

    # Set screen manager (Changes betweeen screens)
    def StateManager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'nameScreen':
            self.nameScreen()
        if self.state == 'main_game':
            self.main_game()

    def main_game(self):
        global cronometro, segundo, facil, normal, dificil, puntuacion
        screen.blit(background, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        sprites.update()
        enemigo.update()
        sprites.draw(screen)
        enemigo.draw(screen)
        tiempoactual = pygame.time.get_ticks()
        impactos = pygame.sprite.spritecollide(jugador, enemigo, False)
        if impactos and (tiempoactual - jugador.ultimogolpe) > jugador.invencible:
            jugador.vidas -= 1
            jugador.ultimogolpe = tiempoactual
        if tiempoactual - cronometro > 1000:
            segundo += 1
            if facil:
                puntuacion += 1
            if normal:
                puntuacion += 3
            if dificil:
                puntuacion += 5
            cronometro = tiempoactual
        if segundo > 5:
            enemigo.add(asteroide2)
        if segundo == 60:
            enemigo.add(asteroide3)
            facil = False
            normal = True
            jugador.vidas = 3
        if segundo > 65:
            enemigo.add(asteroide4)
        if segundo == 120:
            enemigo.add(asteroide5)
            normal = False
            dificil = True
            jugador.vidas = 3
        if segundo > 125:
            enemigo.add(asteroide6)
        if segundo > 180:
            asteroide1.kill()
            asteroide2.kill()
            asteroide3.kill()
            asteroide4.kill()
            asteroide5.kill()
            asteroide6.kill()
        if jugador.vidas == 0:
            asteroide1.kill()
            asteroide2.kill()
            asteroide3.kill()
            asteroide4.kill()
            asteroide5.kill()
            asteroide6.kill()
            facil = False
            normal = False
            dificil = False
        pygame.display.flip()

    #Set name screen
    def nameScreen(self):
        global shiftDown
        screen.blit(background, [0, 0])
        screen.blit(textBox.image, textBox.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = False
            if event.type == pygame.KEYDOWN:
                textBox.add_chr(pygame.key.name(event.key))
                if event.key == pygame.K_SPACE:
                    textBox.text += " "
                    textBox.update()
                if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = True
                if event.key == pygame.K_BACKSPACE:
                    textBox.text = textBox.text[:-1]
                    textBox.update()
                if event.key == pygame.K_RETURN:
                    if len(textBox.text) > 0:
                        self.state = 'intro'

    #Set main menu screen
    def intro(self):
        screen.blit(background, [0, 0])
        draw_text(screen, "OPERATION MOON LIGHT", 65, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, "Presione una tecla para proceder", 27, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "(1) Iniciar", 20, WIDTH // 2, HEIGHT * 3 / 4)
        draw_text(screen, "(2) About", 20, WIDTH // 2, HEIGHT * 3 / 4 + 30)
        draw_text(screen, "(3) Scores", 20, WIDTH // 2, HEIGHT * 3 / 4 + 60)
        draw_text(screen, "(4) Intrucciones", 20, WIDTH // 2, HEIGHT * 3 / 4 + 90)
        draw_text(screen, "(5) Escoger nivel", 20, WIDTH // 2, HEIGHT * 3 / 4 + 120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.state = 'main_game'
                elif event.key == pygame.K_2:
                    self.state = 'about'
                elif event.key == pygame.K_3:
                    self.state = 'scores'
                elif event.key == pygame.K_4:
                    self.state = 'rules'
                elif event.key == pygame.K_5:
                    self.state = 'levels'
        pygame.display.flip()

    #Set about screen
    def about(self):
        screen.blit(background, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

    #Set scores screen
    def scores(self):
        screen.blit(background, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

    #Set intructions screen
    def rules(self):
        screen.blit(background, [0, 0])
        draw_text(screen, "OPERATION MOON LIGHT", 65, WIDTH // 2, HEIGHT // 4)
        draw_text(screen, "Para moverse utilice las flechas del teclado", 27, WIDTH // 2, HEIGHT // 2)
        draw_text(screen, "Para disparar utilice la barra espaciadora", 27, WIDTH//2, HEIGHT//2 +32)
        draw_text(screen, "Para volver a la pantalla inicial presione la tecla escape", 27, WIDTH // 2, HEIGHT//2 +32*2)
        draw_text(screen, "Mientras juega, presione escape para volver al incio", 27, WIDTH // 2, HEIGHT//2 +32*3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'intro'
        pygame.display.flip()

    # Set intructions screen
    def levels(self):
        screen.blit(background, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

    def level1(self):
        screen.blit(background,[0 , 0])
        pygame.display.flip()

    def level2(self):
        screen.blit(background,[0 , 0])
        pygame.display.flip()

    def level3(self):
        screen.blit(background, [0, 0])
        hola=0
        pygame.display.flip()

    #Set game over screen
    def go_screen(self):
        screen.blit(background, [0, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

#Set class for TextBox (Write your name menu)
class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font(None, 50)
        self.image = self.font.render("Digite su nombre", True, WHITE)
        self.rect = self.image.get_rect()

    def add_chr(self, character):
        global shiftDown
        if character in validChars and not shiftDown:
            self.text += character
        elif character in validChars and shiftDown:
            self.text += shiftChars[validChars.index(character)]
        self.update()

    def update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, True, WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos

#Variables
background=pygame.image.load("spacebg3.jpg").convert()
game_state=GameState()
textBox = TextBox()
textBox.rect.center = [325, 325]

#Arreglar
sprites=pygame.sprite.Group()
jugador=Jugador()
sprites.add(jugador)

enemigo=pygame.sprite.Group()
asteroide1=Asteroide()
asteroide2=Asteroide()
asteroide3=Asteroide()
asteroide4=Asteroide()
asteroide5=Asteroide()
asteroide6=Asteroide()
enemigo.add(asteroide1)

#Main-loop
while True:
    game_state.StateManager()
    clock.tick(60)  # FPS

pygame.quit()
