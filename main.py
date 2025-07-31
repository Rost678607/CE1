##########################################
#                Imports                 #
##########################################

from time import sleep, time
from keyboard import is_pressed as isPressed
import random

##########################################
#                 Values                 #
##########################################

class Values():

    debug = True

    #screen
    tpsLimit = 30
    height = 45
    width = 149
    doRender = True

values = Values()

##########################################
#                  Game                  #
##########################################
          # govnocoded example #
          ######################

gtick = 5
playerSpeedY = 0.0
groundY = 0
playerY = 0.0
playerX = 0
levelX = 0
level = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 4, 0, 5, 0, 0, 1, 1, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0],
         [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 1, 0, 0]]
levelLen = 0
best = 0
loseSplashs = ("You Lose!", "Oof", "No =(")
winSplashs = ("You Win!", "GG!", "100%")

def start():
    global groundY, playerY, playerX, levelLen

    levelLen = len(level[0]) * 5 + 15
    
    groundY = int(screen.height / 5 * 4)
    playerY = groundY - 3
    playerX = int(screen.width / 4)

    screen.fill(" ")
    screen.drawLine(0, groundY, screen.width - 1, groundY, "M")

def loop():
    global playerY, playerX, playerSpeedY, groundY, gtick, levelX, level, winSplashs
    
    screen.drawRectangle(0, 0, screen.width - 1, screen.height - 1, " ")
    screen.drawLine(0, groundY, screen.width - 1, groundY, "M")

    # ground
    screen.drawLine(0, groundY + 1, screen.width - 1, groundY + 1, "=")
    for i in range(0, screen.width - 1, 32):
        if i + gtick < screen.width:
            screen.drawLine(i + gtick, groundY + 1, i + gtick, screen.height - 1, "M")
    gtick -= 1
    if gtick < 0:
        gtick = 31

    #level
    if isPressed("r"):
        levelX = 0
        gtick = 5
    
    for y in range(7):
        for x in range(int(levelLen / 5 - 3)):
            if level[y][x] == 1:
                drawObject.block(levelX, x, 7 - y)
            elif level[y][x] == 2:
                drawObject.spike(levelX, x, 7 - y, False)
            elif level[y][x] == 3:
                drawObject.spike(levelX, x, 7 - y, True)
            elif level[y][x] == 4:
                drawObject.halfBlock(levelX, x, 7 - y, False)
            elif level[y][x] == 5:
                drawObject.halfBlock(levelX, x, 7 - y, True)
    
    levelX += 1

    #player
    
    if screen.getPoint(playerX - 2, playerY + 3) == " " and screen.getPoint(playerX - 1, playerY + 3) == " " and screen.getPoint(playerX, playerY + 3) == " " and screen.getPoint(playerX + 1, playerY + 3) == " " and screen.getPoint(playerX + 2, playerY + 3) == " ":
        playerSpeedY -= 0.4
    else:
        playerSpeedY = 0.0
        if isPressed("space") or isPressed("up"):
            playerSpeedY = 3

    if playerSpeedY < 0:
        for i in range(int(playerSpeedY), 0):
            if screen.getPoint(playerX - 2, playerY + 3) == " " and screen.getPoint(playerX - 1, playerY + 3) == " " and screen.getPoint(playerX, playerY + 3) == " " and screen.getPoint(playerX + 1, playerY + 3) == " " and screen.getPoint(playerX + 2, playerY + 3) == " ":
                playerY += 1
    elif playerSpeedY > 0:
        for i in range(int(playerSpeedY)):
            if screen.getPoint(playerX - 2, playerY) == " " and screen.getPoint(playerX, playerY) == " " and screen.getPoint(playerX + 2, playerY) == " ":
                playerY -= 1

    for x in range(-2, 3):
        for y in range(-2, 3):
            if screen.getPoint(playerX + x, playerY + y) != " " and levelX > 0:
                gameOver()
                break
        if screen.getPoint(playerX + x, playerY + 3) == "*":
            gameOver()
            break

    screen.drawPoint(playerX, playerY, "#")
    screen.drawRectangle(playerX - 2, playerY - 2, playerX + 2, playerY + 2, "#", False)

    # win
    if levelX > levelLen + 30:
        r = random.randint(0, len(winSplashs) - 1)
        screen.printText(int(screen.width / 2) - int((len(winSplashs[r]) / 2)), int(screen.height / 2), winSplashs[r])

        screen.render()
        sleep(1)
        while True:
            if isPressed("r") or isPressed("space") or isPressed("up"):
                break
        
        gtick = 5
        levelX = 0
        best = 100

def end():
    screen.fill(":")
    screen.drawLine(0, screen.height - 1, screen.width - 1, screen.height - 1, "=")
    screen.drawPoint(int(screen.width / 2) - 3, screen.height - 1, "<")
    screen.drawPoint(int(screen.width / 2) - 2, screen.height - 1, "[")
    screen.printText(int(screen.width / 2) - 1, screen.height - 1, "Bye!")
    screen.drawPoint(int(screen.width / 2) + 3, screen.height - 1, "]")
    screen.drawPoint(int(screen.width / 2) + 4, screen.height - 1, ">")
    screen.render(False)

def gameOver():
    global levelX, best, levelLen, loseSplashs, gtick, playerSpeedY, playerX, playerY
    score = int(levelX / (levelLen + 30) * 100)

    screen.drawLine(playerX - 2, playerY - 2, playerX + 2, playerY + 2, "#")
    screen.drawLine(playerX + 2, playerY - 2, playerX - 2, playerY + 2, "#")

    if score > best:
        r = random.randint(0, len(loseSplashs) - 1)
        screen.printText(int(screen.width / 2) - int((len(loseSplashs[r]) / 2)), int(screen.height / 2) + 2, loseSplashs[r])
        screen.printText(int(screen.width / 2) - int((len(str(score)) + 1) / 2), int(screen.height / 2), str(score) + "%")
        best = score

    screen.render()
    
    for i in range(0, 100):
        if isPressed("r"):
            break
        else:
            sleep(0.01)
    
    playerSpeedY = 0.0
    playerY = groundY - 3
    gtick = 5
    levelX = 0

class DrawObject():
    def cordsTranslate(self, levelX, x, y):
        x = x * 5 - levelX + 70
        y = y * -5 + groundY + 2
        return x, y

    def block(self, levelX, x, y):
        x, y = self.cordsTranslate(levelX, x, y)
        screen.drawRectangle(x - 2, y - 2, x + 2, y + 2, "%", False)
        screen.drawLine(x - 1, y - 1, x + 1, y - 1, "*")
        screen.drawLine(x - 1, y, x + 1, y, "`")

    def spike(self, levelX, x, y, inverted = False):
        x, y = self.cordsTranslate(levelX, x, y)
        if inverted:
            screen.drawLine(x - 2, y - 2, x, y + 2, "*")
            screen.drawLine(x + 2, y - 2, x, y + 2, "*")
            screen.drawLine(x - 2, y - 2, x + 2, y - 2, "*")
        else:
            screen.drawLine(x - 2, y + 2, x, y - 2, "*")
            screen.drawLine(x + 2, y + 2, x, y - 2, "*")
            screen.drawLine(x - 2, y + 2, x + 2, y + 2, "*")

    def halfBlock(self, levelX, x, y, inverted = False):
        x, y = self.cordsTranslate(levelX, x, y)
        if inverted:
            screen.drawRectangle(x - 2, y, x + 2, y + 2, "%")
            screen.drawLine(x - 1, y + 1, x + 1, y + 1, "*")
        else:
            screen.drawRectangle(x - 2, y, x + 2, y - 2, "%")
            screen.drawLine(x - 1, y - 1, x + 1, y - 1, "*")

drawObject = DrawObject()

##########################################
#                Graphics                #
##########################################

class Screen():
    height = values.height
    width = values.width

    def __init__(self):
        self.frameWithoutOwerlays = [["#" for _ in range(self.height)] for _ in range(self.width)]
        self.frame = self.frameWithoutOwerlays

    def render(self, overlays = True):
        if values.doRender:
            self.frame = self.frameWithoutOwerlays
            if overlays:
                self.addOverlays()
            print("\n".join("".join(self.frame[x][y] for x in range(self.width)) for y in range(self.height)))

    def getPoint(self, x, y):
        if (x < self.width) and (y < self.height):
            return self.frameWithoutOwerlays[x][y]
        else:
            return " "
    
    def drawPoint(self, x, y, char, isOverlay = False):
        if (x < self.width) and (y < self.height):
            char = str(char[:1])

            self.frameWithoutOwerlays[x][y] = char

    def drawLine(self, x1, y1, x2, y2, char, isOverlay = False):
        char = str(char[:1])

        if (x1 < self.width) and (y1 < self.height - 1) and (x2 > -1) and (y2 > -1):
            x1 = 0 if x1 < x2 and x1 < 0 else x1
            y1 = 0 if y1 < y2 and y1 < 0 else y1
            x2 = 0 if x2 < x1 and x2 < 0 else x2
            y2 = 0 if y2 < y1 and y2 < 0 else y2
            x1 = self.width - 1 if x1 > x2 and x1 > self.width - 1 else x1
            y1 = self.width - 1 if y1 > y2 and y1 > self.width - 1 else y1
            x2 = self.width - 1 if x2 > x1 and x2 > self.width - 1 else x2
            y2 = self.width - 1 if y2 > y1 and y2 > self.width - 1 else y2

            if x1 == x2:
                if isOverlay:
                    for i in range(y1, y2 + 1):
                        self.frame[x1][i] = char
                else:
                    for i in range(y1, y2 + 1):
                        self.frameWithoutOwerlays[x1][i] = char

            elif y1 == y2:
                if isOverlay:
                    for i in range(x1, x2 + 1):
                        self.frame[i][y1] = char
                else:
                    for i in range(x1, x2 + 1):
                        self.frameWithoutOwerlays[i][y1] = char

            else:
                dx = abs(x2 - x1)
                dy = abs(y2 - y1)
                sx = 1 if x1 < x2 else -1
                sy = 1 if y1 < y2 else -1
                err = dx - dy
                if isOverlay:
                    while True:
                        self.frame[x1][y1] = char
                        if x1 == x2 and y1 == y2:
                            break
                        e2 = 2 * err
                        if e2 > -dy:
                            err -= dy
                            x1 += sx
                        if e2 < dx:
                            err += dx
                            y1 += sy
                else:
                    while True:
                        self.frameWithoutOwerlays[x1][y1] = char
                        if x1 == x2 and y1 == y2:
                            break
                        e2 = 2 * err
                        if e2 > -dy:
                            err -= dy
                            x1 += sx
                        if e2 < dx:
                            err += dx
                            y1 += sy
    
    def drawBroken(self, vertices, char, isOverlay = False):
        for i in range(len(vertices) - 1):
            self.drawLine(vertices[i][0], vertices[i][1], vertices[i + 1][0], vertices[i + 1][1], char, isOverlay)
    
    def drawPolygon(self, vertices, char, isOverlay = False):
        for i in range(len(vertices) - 1):
            self.drawLine(vertices[i][0], vertices[i][1], vertices[i + 1][0], vertices[i + 1][1], char, isOverlay)
        self.drawLine(vertices[i + 1][0], vertices[i + 1][1], vertices[0][0], vertices[0][1], char, isOverlay)

    def drawRectangle(self, x1, y1, x2, y2, char, isFilled = True, isOverlay = False):
        char = str(char[:1])

        if x1 > x2:
            a = x1
            x1 = x2
            x2 = a
        
        if y1 > y2:
            a = y1
            y1 = y2
            y2 = a

        if (x1 < self.width) and (y1 < self.height - 1) and (x2 > -1) and (y2 > -1):
            x1 = 0 if x1 < 0 else x1
            y1 = 0 if y1 < 0 else y1
            x2 = self.width - 1 if x2 > self.width - 1 else x2
            y2 = self.width - 1 if y2 > self.width - 1 else y2

            if isFilled:
                if isOverlay:
                    for y in range(y1, y2 + 1):
                        for x in range(x1, x2 + 1):
                            self.frame[x][y] = char
                else:
                    for y in range(y1, y2 + 1):
                        for x in range(x1, x2 + 1):
                            self.frameWithoutOwerlays[x][y] = char
            else:
                if isOverlay:
                    for x in range(x1, x2):
                        self.frame[x][y1] = char
                        self.frame[x][y2] = char
                    for y in range(y1, y2 + 1):
                        self.frame[x1][y] = char
                        self.frame[x2][y] = char
                else:
                    for x in range(x1, x2):
                        self.frameWithoutOwerlays[x][y1] = char
                        self.frameWithoutOwerlays[x][y2] = char
                    for y in range(y1, y2 + 1):
                        self.frameWithoutOwerlays[x1][y] = char
                        self.frameWithoutOwerlays[x2][y] = char

    def fill(self, char):
        char = str(char)
        if len(char) == 1:
            for y in range(0, self.height):
                for x in range(0, self.width):
                    self.frameWithoutOwerlays[x][y] = char
        else:
            pass

    def printText(self, x, y, text, isOverlay=False):
        text = str(text)
        if x + len(text) > self.width:
            text = text[:(x+len(text))-self.width]
        if isOverlay:
            for i in range(len(text)):
                self.frame[x + i][y] = text[i:i+1]
        else:
            for i in range(len(text)):
                self.frameWithoutOwerlays[x + i][y] = text[i:i+1]

    def copy(self, x1, y1, x2, y2, targetX, targetY):
        x1 = self.width - 1 if x1 > self.width - 1 else x1
        y1 = self.height - 1 if y1 > self.height - 1 else y1
        x2 = self.width - 1 if x2 > self.width - 1 else x2
        y2 = self.height - 1 if y2 > self.height - 1 else y2

        if x1 > x2:
            a = x1
            x1 = x2
            x2 = a
        
        if y1 > y2:
            a = y1
            y1 = y2
            y2 = a

        width = x2 - x1
        height = y2 - y1

        targetX = self.width - width if x1 + width > self.width else targetX
        targetY = self.height - height if y1 + height > self.height else targetY

        buffer = [[" " for _ in range(height)] for _ in range(width)]
        for x in width:
            for y in height:
                buffer[x][y] = self.frameWithoutOwerlays[1 + x][y1 + y]

        for x in width:
            for y in height:
                self.frameWithoutOwerlays[targetX + x][targetY + y] = buffer[x][y]


##########################################
#                Overlays                #
##########################################

    def addOverlays(self):
        if values.debug:
            self.printText(0, 0, "Size: " + str(self.width) + "x" + str(self.height) + " ", True)
            if debugInfo.tps > 0:
                self.printText(0, 1, "FPS: " + str(debugInfo.tps) + " ", True)
                self.printText(0, 2, "TPS: " + str(debugInfo.tps) + " ", True)
            else:
                self.printText(0, 1, "FPS: < 1 ", True)
                self.printText(0, 2, "TPS: < 1 ", True)
            self.printText(0, 3, "Last tick duration: " + str(debugInfo.tickDuration)[:8] + " ")

##########################################
#                 Input                  #
##########################################

class Enter():
    def text(self, ask = "", type = "str"):
        ask = str(ask)
        screen.drawLine(0, screen.height - 1, screen.width - 1, screen.height - 1, "=", True)
        if ask == "":
            ask = " "
        else:
            screen.drawPoint(len(ask) + 2, screen.height - 1, "#", True)
            ask = " " + ask + " # "
        screen.render()
        if type == "str":
            result = str(input(ask))
        if type == "int":
            error = ""
            while True:
                try:
                    result = int(input(error + ask))
                    break
                except ValueError:
                    error = " Enter number #"
                    screen.drawLine(0, screen.height - 1, screen.width - 1, screen.height - 1, "=", True)
                    screen.drawPoint(14, screen.height - 1, "#", True)
                    if ask != " ":
                        screen.drawPoint(len(ask) + 13, screen.height - 1, "#", True)
                    screen.render()
        return result

enter = Enter()

#    def log(msg):
#        if debug:

screen = Screen()

##########################################
#                Runtime                 #
##########################################

class DebugInfo():
    tps = 0
    tickDuration = 0

debugInfo = DebugInfo()

class Runtime():
    tick = 1 / values.tpsLimit
    run = True

    def exit(self):
        self.run = False

    def runtime(self):
        start()
        while self.run:
            loopstart = time()
            loop()
            screen.render()
            debugInfo.tickDuration = time() - loopstart
            debugInfo.tps = int(1 / max(debugInfo.tickDuration, self.tick))
            if debugInfo.tickDuration < self.tick:
                sleep(self.tick - debugInfo.tickDuration)
        end()
    
    def main(self):
        self.runtime()

runtime = Runtime()

if __name__ == "__main__":
    runtime.main()