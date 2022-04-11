import turtle
import os
import winsound

speed = 0.1
score_a = 0
score_b = 0

wn = turtle.Screen()
wn.title("Pong by jimmy")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # update game screen manually

# Paddle A
paddleA = turtle.Turtle()
paddleA.speed(0)  # speed of animation
paddleA.shape("square")
paddleA.color("white")
paddleA.shapesize(stretch_wid=5, stretch_len=1)  # by default it's 20px with / height
paddleA.penup()
paddleA.goto(-350, 0)  # 0,0 is center of the screen

# Paddle B
paddleB = turtle.Turtle()
paddleB.speed(0)  # speed of animation
paddleB.shape("square")
paddleB.color("white")
paddleB.shapesize(stretch_wid=5, stretch_len=1)  # by default it's 20px with / height
paddleB.penup()
paddleB.goto(350, 0)  # 0,0 is center of the screen

# Ball
ball = turtle.Turtle()
ball.speed(0)  # speed of animation
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)  # 0,0 is center of the screen
ball.dx = speed
ball.dy = speed

# Pen score
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

def paddle_a_up():
    y = paddleA.ycor()  # return the y coordinate
    y += 20
    if y > 260:
        y = 260
    paddleA.sety(y)


def paddle_a_down():
    y = paddleA.ycor()  # return the y coordinate
    y -= 20
    if y < -240:
        y = -240
    paddleA.sety(y)


def paddle_b_up():
    y = paddleB.ycor()  # return the y coordinate
    y += 20
    if y > 260:
        y = 260
    paddleB.sety(y)


def paddle_b_down():
    y = paddleB.ycor()  # return the y coordinate
    y -= 20
    if y < -240:
        y = -240
    paddleB.sety(y)


# keyboard binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

# Main game loop
while True:
    wn.update()  # update the screen everytime the loop runs

    # animate the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # border check
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= - 1
        winsound.PlaySound("beep_one.mp3", winsound.SND_ASYNC)

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= - 1
        winsound.PlaySound("beep_one.mp3", winsound.SND_ASYNC)

    if ball.xcor() > 390:
        ball.goto(0, 0)  # reset ball position
        ball.dx *= - 1
        score_a += 1
        pen.clear()
        pen.write("Player A: {0}  Player B: {1}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)  # reset ball position
        ball.dx *= - 1
        score_b += 1
        pen.clear()
        pen.write("Player A: {0}  Player B: {1}".format(score_a, score_b), align="center",
                  font=("Courier", 24, "normal"))

    # paddle and ball collision
    if (340 < ball.xcor() < 350) and ((paddleB.ycor() + 40) > ball.ycor() > (paddleB.ycor() - 40)):
        ball.setx(340)
        ball.dx *= -1
        winsound.PlaySound("beep_one.mp3", winsound.SND_ASYNC)

    if (-350 < ball.xcor() < -340) and ((paddleA.ycor() + 40) > ball.ycor() > (paddleA.ycor() - 40)):
        ball.setx(-340)
        ball.dx *= -1
        winsound.PlaySound("beep_one.mp3", winsound.SND_ASYNC)
