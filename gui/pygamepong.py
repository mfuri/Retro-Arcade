import pygame
#Seth Polen
#switched because turtle wasn't very intuitive with start screen

pygame.init()
clock = pygame.time.Clock()


screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('PONG GAME')


#paddle1 = player paddle2 = opponent AI
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15,30,30)
paddle1 = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
paddle2 = pygame.Rect(10, screen_height/2 - 70, 10, 140)

paddle1_score = 0
paddle2_score = 0
thefont = pygame.font.Font(None, 36)


#pygame draw (r,g,b) 0-255 0 is no color 255 pure color

bg_color = pygame.Color(0,0,0)
paddlecolor = (255, 255, 255)


######## object movement ########
x_speed = 7
y_ball_speed = 7
player_speed = 0
AI_Speed = 6.25

######## ball movement function #######
def ballmovement():
	global x_speed, y_ball_speed
	ball.x += x_speed
	ball.y += y_ball_speed
	
	######ball bounce#######
	if ball.top <= 0 or ball.bottom >= screen_height:
		y_ball_speed *= -1
	if ball.left <= 0
		ball.center = (screen_width/2, screen_height/2)
		y_ball_speed *= -1
		x_speed *= -1
		paddle1_score += 1
	if ball.right >= screen_width:
		ball.center = (screen_width/2, screen_height/2)
		y_ball_speed *= -1
		x_speed *= -1
		paddle2_score += 1
		
	######ball collision with paddle######
	if ball.colliderect(paddle1) or ball.colliderect(paddle2):
		x_speed *= -1


######### Main Loop #########

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			#sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed += 7
			if event.key == pygame.K_UP:
				player_speed -= 7
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -= 7
			if event.key == pygame.K_UP:
				player_speed += 7		
	#######object coloring#######

	screen.fill(bg_color)

	pygame.draw.rect(screen,paddlecolor,paddle1)
	pygame.draw.rect(screen,paddlecolor,paddle2)
	pygame.draw.ellipse(screen, paddlecolor, ball)

	left_text = thefont.render(f"{paddle2_score}", True, paddlecolor)
	screen.blit(left_text, (360, 1000))

	right_text = thefont.render(f"{paddle1_score}", True, paddlecolor)
	screen.blit(right_text, (460, 1000))

	ballmovement()
	paddle1.y += player_speed
	if paddle1.top <= 0:
		paddle1.top = 0
	if paddle1.bottom >= screen_height:
		paddle1.bottom = screen_height

	#####AI MOVEMENT#####
	if paddle2.top < ball.y:
		paddle2.top += AI_Speed
	if paddle2.bottom > ball.y:
		paddle2.bottom -= AI_Speed
	if paddle2.top <= 0:
		paddle2.top = 0
	if paddle2.bottom >= screen_height:
		paddle2.bottom = screen_height
	
	
	pygame.display.flip()
	clock.tick(50)
