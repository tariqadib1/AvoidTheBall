import pygame, random, threading

LEFT = 'LEFT'
RIGHT = 'RIGHT'
DOWN = 'DOWN'
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
playerLength = 125
playerWidth = 79
catImg = pygame.image.load('cat.png')
ballImg = pygame.image.load('ball.jpeg')
fallSize = [20,20]

def isPointInsideRect(x, y, rect):
	if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
		return True

def isCollision(drop,playerTab):
	if ((isPointInsideRect(drop.left, drop.top, playerTab)) or (isPointInsideRect(drop.left, drop.bottom, playerTab)) or (isPointInsideRect(drop.right, drop.top, playerTab)) or (isPointInsideRect(drop.right, drop.bottom, playerTab))):
		return True
	return False

def GameOver(killCount):
	font = pygame.font.Font('Calibri.ttf', 32)
	text = font.render("Game Over", True, RED, BLACK)
	textRect = text.get_rect() 
	textRect.center = (300,200)
	screen.blit(text, textRect)
	
	font = pygame.font.Font('Calibri.ttf', 30)
	text = font.render("Your Score = {}".format(killCount), True, RED, BLACK)
	textRect = text.get_rect() 
	textRect.center = (300,250)
	screen.blit(text, textRect)
	
	font = pygame.font.Font('Calibri.ttf', 28)
	text = font.render("Press (R) to Rest", True, RED, BLACK)
	textRect = text.get_rect() 
	textRect.center = (300,300)
	screen.blit(text, textRect)
	return True
	
def drawGame(player,fall,isGameOver):
	global screen,killCount,playerLength
	pSurface = pygame.Surface((playerLength,playerWidth))
	pSurface.fill(RED)
	screen.blit(catImg,player)
	collisionDetected = False
	nextFall = []
	
	for drop in fall:
		dSurface = pygame.Surface(fallSize)
		dSurface.fill(WHITE)
		screen.blit(ballImg,drop)
		if drop[1] < 400:
			nextFall.append((drop[0],drop[1]+1))
		else:
			if not isGameOver:
				killCount += 1
			if killCount %50 == 0:
				print(killCount)
		if not collisionDetected:
			collisionDetected = isCollision(pygame.Rect(drop[0],drop[1],fallSize[0],fallSize[1]), pygame.Rect(player[0],player[1],playerLength,playerWidth))
			
	return nextFall, collisionDetected

def drawPlayer():
	global screen
	surface = pygame.Surface((playerLength,1))
	surface.fill(RED)
	screen.blit(surface,player)

def movePlayer(side):
	global player
	if side == LEFT:
		player[0] -= 20
	if side == RIGHT:
		player[0] += 20
	if player[0]<10:
		player[0]=10
	if player[0]>590:
		player[0]=590

def NewDrop():
	global fall
	x,y = random.randint(1,599),random.randint(1,199)
	for drops in fall:
		if x >= drops[0] and x <= drops[0]+(fallSize[0]*2):
			return
	fall.append((x,y))
	
def drawfall():
	global fall,killCount
	for drop in fall:
		surface = pygame.Surface((1,1))
		surface.fill(WHITE)
		screen.blit(surface,drop)
		fall.remove(drop)
		if drop[1] < 400:
			fall.append((drop[0],drop[1]+1))
		else:
			killCount += 1
			print(killCount)
	
	
def isCollisionOld(player,fall):
	for breadthPoint in range(0,playerLength):
		if (player[0]+breadthPoint,player[1]) in fall:
			return True
	return False

def main():
	difficultyControl = 0
	global player,fall,killCount,screen,playerLength,fallDropFrequency
	isGameOver=False
	killCount = 1
	fallDropFrequency = 400
	player = [random.randint(1,599),300]
	fall = []
	pygame.init()
	screen = pygame.display.set_mode((600,400))
	screen.fill(BLACK)
	clock = pygame.time.Clock()
	
	ADDfallDROP = pygame.USEREVENT + 1
	pygame.time.set_timer(ADDfallDROP, fallDropFrequency)
	
	screen.fill(WHITE)
	while True:
		screen.fill(WHITE)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					quit()
				if event.key == pygame.K_r:
					killCount = 0
					isGameOver = False
					fallDropFrequency = 200
					fall.clear()	
					screen.fill(WHITE)
					#playerLength = 10
			if not isGameOver and event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					movePlayer(LEFT)
				if event.key == pygame.K_RIGHT:
					movePlayer(RIGHT)
			if event.type == ADDfallDROP:
				newThread = threading.Thread(target=NewDrop, args=())
				newThread.start()
					
		fall, collisionDetected = drawGame(player,fall,isGameOver)
		
		# ~ newThread = threading.Thread(target=drawGame, args=(player,fall,isGameOver))
		# ~ newThread.start()
		# ~ fall, collisionDetected = newThread.join()
		
		# ~ print(collisionDetected)
		# ~ print(killCount)
		if collisionDetected or isGameOver:
			isGameOver=GameOver(killCount)
		
		if killCount % 50 == 0 and difficultyControl!=killCount:
			difficultyControl=killCount
			fallDropFrequency -= 20
			#playerLength += 5
		
		pygame.display.update()
		clock.tick(60)

if __name__ == '__main__':
	main()
