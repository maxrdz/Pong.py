from graphics import *
import random

margin = 10
moveIncrement = 13
bounceIncrement = 7
ballRadius = 15
bounceWait = 2400


class Timer:
    def __init__(self):
        self.value = 0


class Paddle:

    def __init__(self, color, width, height, coordx, win):
        self.color = color
        self.width = width
        self.height = height
        self.x = coordx
        self.shape = Rectangle(Point(self.x - int(self.width / 2), win.getHeight() - margin - self.height),
                               Point(self.x + int(self.width / 2), win.getHeight() - margin))
        self.shape.setFill(self.color)
        self.window = win
        self.shape.draw(self.window)

    def move_left(self):
        if self.x - margin - int(self.width / 2) > 0:
            self.x -= moveIncrement
            self.shape.move(-moveIncrement, 0)

    def move_right(self):
        if self.x + margin + int(self.width / 2) < self.window.getWidth():
            self.x += moveIncrement
            self.shape.move(moveIncrement, 0)


class Ball:

    def __init__(self, coordx, coordy, color, radius, win):
        self.shape = Circle(Point(coordx, coordy), radius)
        self.x = coordx
        self.y = coordy
        self.xMovement = 0
        self.yMovement = 0
        self.color = color
        self.window = win
        self.shape.setFill(self.color)
        self.shape.draw(self.window)
        self.radius = radius
        self.timer = 0

    def is_moving(self):
        if self.xMovement != 0 and self.yMovement != 0:
            return True
        else:
            return False

    def bounce(self, gameTimer, minX, maxX, maxY):
        # Calculating x-axis ball movement and bouncing

        gameOver = False

        if gameTimer >= self.timer + bounceWait:
            self.timer = gameTimer
            if self.xMovement == 1:
                if self.x + self.radius + margin + bounceIncrement > self.window.getWidth():
                    self.xMovement = -1
                    self.x -= bounceIncrement
                else:
                    self.x += bounceIncrement
            elif self.xMovement == -1:
                if self.x - self.radius - margin - bounceIncrement < 0:
                    self.xMovement = 1
                    self.x += bounceIncrement
                else:
                    self.x -= bounceIncrement

            # Calculating y-axis ball movement and bouncing
            if self.yMovement == 1:
                if self.y + self.radius + bounceIncrement > maxY:
                    if minX <= self.x <= maxX:
                        self.yMovement = -1
                        self.y -= bounceIncrement
                    else:
                        gameOver = True
                else:
                    self.y += bounceIncrement
            elif self.yMovement == -1:
                if self.y - self.radius - margin - bounceIncrement < 0:
                    self.yMovement = 1
                    self.y += bounceIncrement
                else:
                    self.y -= bounceIncrement
            self.shape.move(self.xMovement * bounceIncrement, self.yMovement * bounceIncrement)
            return gameOver


def game_over_screen(ball, paddle, window):
    ball.shape.undraw()
    paddle.shape.undraw()
    endTxt = Text(Point(int(window.getWidth() / 2), int(window.getHeight() / 2)), "GAME OVER")
    endTxt.setTextColor("Red")
    endTxt.setSize(20)
    moreTxt = Text((Point(int(window.getWidth() / 2), int(window.getHeight() / 2) + 40)), "Press Any Key To Quit")
    moreTxt.setTextColor("Red")
    moreTxt.setSize(20)
    endTxt.draw(window)
    moreTxt.draw(window)
    window.getKey()


def main():
    win = GraphWin("Pong", 824, 568)
    lives = 3
    win.setBackground("Black")
    myPaddle = Paddle("White", 100, 25, 512, win)
    myBall = Ball(myPaddle.x, win.getHeight() - margin - myPaddle.height - ballRadius, "Cyan", ballRadius, win)
    livesCounter = Text(Point(win.getWidth() - int(win.getWidth() / 10), int(win.getHeight() / 10)), f'Lives -- {lives}')
    livesCounter.setTextColor("Cyan")
    livesCounter.setSize(15)
    livesCounter.draw(win)
    gameTimer = Timer()
    gameOver = False
    while lives > 0:
        while not gameOver:
            keyPress = win.checkKey()
            if keyPress == 'a':
                myPaddle.move_left()
                if not myBall.is_moving():
                    myBall.xMovement = -1
                    myBall.yMovement = -1
            if keyPress == 'd':
                myPaddle.move_right()
                if not myBall.is_moving():
                    myBall.xMovement = 1
                    myBall.yMovement = -1
            if keyPress == 'q':
                gameOver = True
            gameTimer.value += 1
            gameOver = myBall.bounce(gameTimer.value, (myPaddle.x-int(myPaddle.width/2)), (myPaddle.x+int(myPaddle.width/2)), win.getHeight() - margin - myPaddle.height)

        if gameOver:
            lives -= 1
            livesCounter.setText(f"Lives -- {lives}")
            myPaddle.shape.undraw()
            myBall.shape.undraw()
            myPaddle = Paddle("White", 100, 25, 512, win)
            myBall = Ball(myPaddle.x, win.getHeight() - margin - myPaddle.height - ballRadius, "Cyan", ballRadius, win)
            gameOver = False

    game_over_screen(myBall, myPaddle, win)


main()
