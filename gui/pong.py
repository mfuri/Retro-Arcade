# pong game for SE project
# Seth Polen SE project 2020
import turtle   # built in no need to install

start = False
playername = "Seth"
def StartMenu():
    screen = turtle.Screen()
    startmenu = turtle.Turtle()
    screen.bgcolor("black")
    startmenu.hideturtle()
    startmenu.penup()
    startmenu.write("Press SPACE to start", align="center", font=("Courier", 36, "normal"))

    screen.onkey(PongGame, 'space')
    screen.onkey(screen.bye, 'Escape')
    screen.listen()
    screen.mainloop()

# main loop
def PongGame():
#    StartMenu()
#   startmenu.clear()
    global start
    start = True 

    wn = turtle.Screen()
    wn.title("Pong Game")

    wn.bgcolor("black")  # background color
    wn.setup(width=1200, height=1000)
    wn.tracer(0)
    # 2 paddles and a ball
    # ### paddle 1 ####
    pad1 = turtle.Turtle()
    pad1.speed(0)
    pad1.shape("square")
    pad1.color("white")
    pad1.shapesize(stretch_wid=5, stretch_len=1)
    pad1.penup()
    pad1.goto(-450, 0)
    # #### paddle 2 ######
    pad2 = turtle.Turtle()
    pad2.speed(0)
    pad2.shape("square")
    pad2.color("white")
    pad2.shapesize(stretch_wid=5, stretch_len=1)
    pad2.penup()
    pad2.goto(450, 0)
    # ### ball ####
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("square")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 4
    ball.dy = 4

    # Scoring
    score1 = 0
    score2 = 0
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 320)
    pen.write("{} {}".format(score1, score2), align="center",
              font=("Courier", 36, "normal"))

    # #### movement function #####
    def pad1_up():
        y_cor = pad1.ycor()
        y_cor += 3.5
        pad1.sety(y_cor)
        # y_cor = pad1.ycor()
        # y_cor += 20
        # pad1.sety(y_cor)

    def pad1_down():
        y_cor = pad1.ycor()
        y_cor -= 3.5
        pad1.sety(y_cor)

    # #### pad2 movement #####
    def pad2_up():
        y_cor = pad2.ycor()
        y_cor += 20
        pad2.sety(y_cor)

    def pad2_down():
        y_cor = pad2.ycor()
        y_cor -= 20
        pad2.sety(y_cor)

    # #### ball movement ####
    # def ball_movement()

    # bind with keyboard
    wn.listen()
    # wn.onkeypress(pad1_up, "w")
    # wn.onkeypress(pad1_down, "s")
    wn.onkeypress(pad2_up, "Up")
    wn.onkeypress(pad2_down, "Down")

    while start:
        wn.update()

        # ### ball movement ####
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # paddle movement with ball
        if pad1.ycor() < ball.ycor():
            pad1_up()
        if pad1.ycor() > ball.ycor():
            pad1_down()

        # wall bouncing top and bottom
        if ball.ycor() > 390:
            ball.sety(390)
            ball.dy *= -1   # reverses the direction

        if ball.ycor() < -390:
            ball.sety(-390)
            ball.dy *= -1   # reverses the direction
        # wall bouncing left and right
        if ball.xcor() > 610:
            ball.goto(0, 0)
            ball.dx *= -1
            score1 += 1
            pen.clear()  # so no overlap with scores
            pen.write("{} {}".format(score1, score2), align="center",
                      font=("Courier", 36, "normal"))

        if ball.xcor() < -610:
            ball.goto(0, 0)
            ball.dx *= -1
            score2 += 1
            pen.clear()
            pen.write("{} {}".format(score1, score2), align="center",
                      font=("Courier", 36, "normal"))

        # ball bouncing off paddle
        if (ball.xcor() < -430 and (ball.ycor() < pad1.ycor() + 50
                                    and ball.ycor() > pad1.ycor() - 50)):
            ball.setx(-430)
            ball.dx *= -1

        if (ball.xcor() > 430 and (ball.ycor() < pad2.ycor() + 50
                                   and ball.ycor() > pad2.ycor() - 50)):
            ball.setx(430)
            ball.dx *= -1

        if score1 == 10 or score2 == 10:
            wn.reset()
	#creat new pen since we called reset
            pen = turtle.Turtle()
            pen.speed(0)
            pen.color("white")
            pen.penup()
            pen.hideturtle()
            pen.goto(0, 320)
            # score 1 means computer won
            # score 2 means player won
            score1 *= 10
            score2 *= 10
            if score1 < score2:
                pen.write("{}, you won!".format(playername), align = "center",
                          font=("Courier", 36, "normal"))
            else:
                pen.write("Game Over, You Lose", align = "center",
                          font =("Courier", 36, "normal"))
            final_score = score2 - score1
            if final_score < 0:
                final_score = 0


StartMenu()
    screen = turtle.Screen()
    startmenu = turtle.Turtle()
    startmenu.hideturtle()
    startmenu.penup()
    startmenu.sety(360)
    startmenu.write("Press SPACE to start", align="center", font=("Courier", 36, "normal"))

    screen.onkeypress(PongGame, 'space')
    screen.listen()


