import pygame
import random

pygame.init() #기본 초기화 (반드시 호출 필요)

# 화면 크기 설정
screen_width = 480 
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("폭탄 여러개 피하기") # 게임 이름

# FPS (frame per second : 초당 프레임 수)
# 프레임수가 높을수록 화면이(ex. 캐릭터 이동) 부드러움
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("game_01.pygameBasic/images/background.png")

# 캐릭터(스프라이트) 불러오기
character = pygame.image.load("game_01.pygameBasic/images/person.png").convert_alpha()
character = pygame.transform.scale(character, (70, 70))

# 캐릭터(이미지) 크기를 구해옴
character_size = character.get_rect().size
character_width = character_size[0] # 가로 크기
character_height = character_size[1] # 세로 크기

# 이미지 위치
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height 

# 이동할 좌표
to_x = 0
# to_y = 0

# 이동 속도
character_speed = 0.6
enemy_speed = 0.5

# 적 enemy 캐릭터 생성
enemies = []

enemy = pygame.image.load("game_01.pygameBasic/images/bomb.png").convert_alpha()
enemy = pygame.transform.scale(enemy, (40, 40))
enemy_size = enemy.get_rect().size # rectangle 정보 : width, height, 좌표 포함
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.uniform(0, screen_width-enemy_width)
enemy_y_pos = 0

for i in range(5):
	rect = pygame.Rect(enemy.get_rect())
	rect.left = random.uniform(0, screen_width-enemy_width)
	rect.top = 0
	speed = random.randint(3, 9)
	enemies.append({
		"pos_x": rect.left, 
		"pos_y": rect.top,
		"speed": speed  
	})	
	
running = True # 게임이 진행중인가?
while running:
	
	dt = clock.tick(60) # 게임 화면의 초당 프레임 수를 설정 
	
	for enemy_idx, enemy_value in enumerate(enemies):
		if screen_height <= enemy_value["pos_y"]:
			# enemy_value["pos_x"] = random.uniform(0, screen_width - enemy_width)
			# enemy_value["pos_y"] = 0
			del enemies[enemy_idx]
			rect = pygame.Rect(enemy.get_rect())
			rect.left = random.uniform(0, screen_width-enemy_width)
			rect.top = 0
			speed = random.randint(3, 9)
			enemies.append({
				"pos_x": rect.left, 
				"pos_y": rect.top,
				"speed": speed 
			})
		else:
			enemy_value["pos_y"] += enemy_value["speed"]

	# 이벤트 처리
	for event in pygame.event.get():  # 반드시 써야하는 부분 (이벤트 발생 체크)
		if event.type == pygame.QUIT: # 창 닫기버튼 누를때
			running = False

		if event.type == pygame.KEYDOWN: # 키보드 키가 눌러짐
			if event.key == pygame.K_LEFT: # 왼쪽 방향키 (캐릭터를 왼쪽으로)
				to_x = to_x - character_speed
			elif event.key == pygame.K_RIGHT:
				to_x += character_speed
			
		if event.type == pygame.KEYUP: # 방향키를 떼면 멈춤
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				to_x = 0

	character_x_pos = character_x_pos + to_x * dt

	# 창에서 벗어나지 않도록 제한
	if character_x_pos < 0:
		character_x_pos = 0
	elif character_x_pos > screen_width - character_width:
		character_x_pos = screen_width - character_width
	
	# 충돌처리를 위한 rect 정보 업데이트
	character_rect = character.get_rect() # 업데이트 안해주면 초기값 그대로 유지됨
	character_rect.left = character_x_pos # 따라서 이동한 위치로 업데이트해줘야함
	character_rect.top = character_y_pos 

	for enemy_value in enemies:
		enemy_rect = enemy.get_rect()
		enemy_rect.left = enemy_value["pos_x"]
		enemy_rect.top = enemy_value["pos_y"]

		# 충돌 체크
		if character_rect.colliderect(enemy_rect):
			print("충돌했어요")
			running = False
			break

	# 배경 그리기
	screen.blit(background, (0,0))	
	# 캐릭터 그리기
	screen.blit(character, (character_x_pos, character_y_pos))
	# screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
	for idx, val in enumerate(enemies):
		pos_x = val["pos_x"]
		pos_y = val["pos_y"]
		screen.blit(enemy, (pos_x, pos_y))
	
	# 반드시 호출되어야 하는 부분 : 화면을 다시 그리기
	pygame.display.update()


pygame.time.delay(1000) 
# pygame 종료
pygame.quit()