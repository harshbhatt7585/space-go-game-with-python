import pygame 
import random
import math
import os

os.environ["SDL_VIDEO_CENTERED"] = "1"

# global variables
WIDTH = 1000
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 120

# colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
brown = (165,42,42)
green = (0,255,0)
blue = (0,0,255)

# images
spaceCraftImgs = [pygame.image.load('images/space craft1.png'),pygame.image.load('images/space craft2.png'),
                    pygame.image.load('images/space craft3.png')]
missileLauncherImg = pygame.image.load('images/missileLauncher.png')
missileImg = pygame.image.load('images/missile.png')
backgroundImg = pygame.image.load('images/space.png')


class Game:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self, img):
        SCREEN.blit(img, (self.x, self.y))

    def movement(self, velX, velY):
        self.x += velX
        self.y += velY

class SpaceCraft(Game):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.velX = 0
        self.velY = 0

    def movement(self):
        self.x += self.velX
        self.y += self.velY

    def outOfTheZone(self):
        if(self.x < -50 or self.x > WIDTH+50 or self.y < -50 or self.y > HEIGHT + 50):
            return True
        return False

class MissileLauncher(Game):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.AB = 0
        self.AC = 0
        self.BC = 0
        self.theta = 0
        self.sideRatio = 0

    def Rotation(self, craftX, craftY):
        self.AB = math.sqrt( (craftX - craftX)**2 + ( (craftY - self.y)**2 ))
        self.AC = math.sqrt( (craftX - self.x)**2 + ( (craftY - self.y)**2 ))
        self.BC = math.sqrt( (craftX - self.x)**2 + ( (self.y - self.y)**2 ))
        self.sideRatio = self.AB/self.AC
        self.theta = int(round(math.degrees(math.asin(self.sideRatio))))
        self.theta = -self.theta
        

        if (craftX > WIDTH/2.5):
            self.theta = -(180 + self.theta) + 5
        return self.theta

class Missile(Game):
    def __init__(self, x,y, velX, velY, theta):
        super().__init__(x,y)
        self.theta = theta
        self.velX = velX
        self.velY = velY

    def draw(self, img):
        SCREEN.blit(pygame.transform.rotate(img, self.theta), (self.x, self.y))


class SpaceGO:

    def __init__(self):
        self.gameOn = True
        self.craftImg = spaceCraftImgs[0]    
        self.craft = SpaceCraft(random.randrange(50, WIDTH-50), random.randrange(50, HEIGHT-50))
        self.missileLauncher = MissileLauncher(WIDTH/2.5, HEIGHT-100)
        self.background1 = Game(0,0)
        self.background2 = Game(0, -HEIGHT)
        self.countdown = 100
        self.lifeLine = 100
        self.gameOver = False
        self.missiles = []
        self.gameSpeed = 5
        self.score = 0 
        self.startGame = False

    def backgroundMovement(self):
        if(self.background1.y > HEIGHT):
            self.background1.y = -HEIGHT

        if(self.background2.y > HEIGHT):
            self.background2.y = -HEIGHT
    
    def speedIncrement(self):
        self.gameSpeed += 0.005

    def screenText(self, text, color, x,y, size, style, bold=False):
        font = pygame.font.SysFont(style, size, bold=bold, italic=False)
        screen_text = font.render(text, True, color)
        SCREEN.blit(screen_text, (int(x),int(y)))

    def GameOver(self):
        self.gameOver = True
        self.craft.velX = 0
        self.craft.velY = 0
        self.missiles.clear()
        self.screenText("Game Over", red , WIDTH/3, 300, 70, 'Arial', bold=True)
        self.screenText("Press Space to Play Again", white, 200, 400 , 54, 'Arial')
        self.screenText('SCORE: '+str(self.score), blue, WIDTH/2.5, 500, 48, 'Airal')

    def getSocre(self):
        self.score += int(self.gameSpeed)
        self.screenText(str(self.score), white, 10, 10, 44, 'Airal', bold = True)
        
    def addMissile(self, launcherRotatedImg):
        self.countdown -= 0.5 + (0.1* self.gameSpeed)

        if self.countdown <= 0:
            velX = round(math.cos(math.radians(self.missileLauncher.theta))*15)
            velY = -round(math.sin(math.radians(self.missileLauncher.theta))*15)
            if(self.craft.x > WIDTH/2.5):
                missile = Missile(self.missileLauncher.x + (launcherRotatedImg.get_width()/1.5), 
                    self.missileLauncher.y, velX, velY, self.missileLauncher.theta)
            else:
                missile = Missile(self.missileLauncher.x + (launcherRotatedImg.get_width()/2), 
                    self.missileLauncher.y +  (launcherRotatedImg.get_height()/2), velX, velY, self.missileLauncher.theta)
            
            self.missiles.append(missile)
            self.countdown = 100

    def launchMissile(self):
        i = 0
        for missile in self.missiles:
            missile.draw(missileImg)
            missile.movement(-missile.velX, -missile.velY)

            if (missile.x < -50 or missile.x >WIDTH + 50 or missile.y < - 50 or missile.y > HEIGHT + 50):
                self.missiles.pop(i)

            if ( (missile.x > self.craft.x)  and  (missile.x < self.craft.x + self.craftImg.get_width())
                and (missile.y > self.craft.y)  and  (missile.y < self.craft.y + self.craftImg.get_height())):
                self.lifeLine -= 1

            i += 1


    def main(self):
        while self.gameOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameOn = False

                if event.type == pygame.KEYDOWN:
                    if(self.gameOver == False):
                        if event.key == pygame.K_RIGHT:
                            self.craft.velX = 12
                            self.craftImg = spaceCraftImgs[2]
                        
                        if event.key == pygame.K_LEFT:
                            self.craft.velX = -12
                            self.craftImg = spaceCraftImgs[1]

                        if event.key == pygame.K_UP:
                            self.craft.velY = -12

                        if event.key == pygame.K_DOWN:
                            self.craft.velY = 12

                    if event.key == pygame.K_SPACE:
                        if(self.gameOver):
                            self.__init__()
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or pygame.K_LEFT or pygame.K_UP or pygame.K_DOWN:
                        self.craft.velX = 0
                        self.craft.velY = 0
                        self.craftImg = spaceCraftImgs[0]

                    

            SCREEN.fill(black)
            self.background1.draw(backgroundImg)
            self.background2.draw(backgroundImg)
            self.background1.movement(0, self.gameSpeed)
            self.background2.movement(0, self.gameSpeed)
            self.backgroundMovement()
            self.craft.draw(self.craftImg)

            if (self.gameOver == False):
                self.launchMissile()
                self.craft.movement()
                self.screenText('Life: '+str(self.lifeLine), green, WIDTH-120, 10, 28, "Arial")
                launcherRotatedImg = pygame.transform.rotate(missileLauncherImg, self.missileLauncher.Rotation(self.craft.x, self.craft.y))
                self.addMissile(launcherRotatedImg)
                self.missileLauncher.draw(launcherRotatedImg)
                self.speedIncrement()
                self.getSocre()

            if(self.craft.outOfTheZone()):
                if(self.lifeLine > 0):
                    self.lifeLine -= 1.5

            if(self.lifeLine <= 0):
                self.GameOver()

            if(self.craft.y >= HEIGHT-50):
                self.GameOver()

            clock.tick(FPS)
            pygame.display.update()

def startGame():
    pygame.init()
    spaceGo = SpaceGO()
    spaceGo.main()

startGame()


        
    
    