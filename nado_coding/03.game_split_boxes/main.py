
import pygame
import os

###################################################### ▼ 반드시 해야하는 부분 (기본 초기화)

pygame.init() #기본 초기화 (반드시 호출 필요)

# 화면 크기 설정
screen_width = 640 
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("공 없애기") # 게임 이름

# FPS (frame per second : 초당 프레임 수)
# 프레임수가 높을수록 화면이(ex. 캐릭터 이동) 부드러움
clock = pygame.time.Clock()

###################################################### ▼ 사용자 게임 초기화

## 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

# 현재 파일 위치 반환
current_path = os.path.dirname(__file__)
# 폴더 위치 반환
image_path = os.path.join(current_path, "images")

# 배경 이미지 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 세로 크기 (스테이지 위에 캐릭터를 두기 위함)

########

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))

# 캐릭터 크기 정보 및 위치 설정
character_size = character.get_rect().size
character_height = character_size[1]
character_width = character_size[0]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동할 좌표
character_to_x = 0

# 캐리터 이동 속도
character_speed = 0.6

########

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

########

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
	pygame.image.load(os.path.join(image_path, "balloon1.png")),
	pygame.image.load(os.path.join(image_path, "balloon2.png")),
	pygame.image.load(os.path.join(image_path, "balloon3.png")),
	pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공 크기에 따른 최초 스피드 설정 (공이 클수록 속도가 빠름)
ball_spped_y = [-18, -15, -12, -9] # 공이 올라갈땐 y값이 내려가는것이므로

# 공이 쪼개짐
balls = []

# 정보가 많으므로 Dictionary 로 관리!!
# 최초 발생하는 큰 공 추가 (공이 한개로 시작)
balls.append({
	"pos_x": 50, #공이 그려지는 x좌표
	"pos_y": 50, #공이 그려지는 y좌표
	"img_idx" : 0, #공의 이미지 인덱스 (가장 큰 공 index : 0)
	"to_x": 3, # x축 이동 방향 (음수면 왼쪽, 양수면 오른쪽)
	"to_y": -6, # y축 이동방향
	"init_spd_y" : ball_spped_y[0] # y 최초 속도
})

# 사라질 무기와 공 정보(인덱스) 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# 폰트 설정 및 메시지
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기) , None 이면 디폴트 폰트
game_result = "Game Over" # "TimeOut", "Mission Complete", "Game Over"

# 총 시간(s)
total_time = 100

# 시작 시간 정보
start_ticks = pygame.time.get_ticks() # 현재 tick (타이머 인터럽트 간격) 정보를 받아옴

###################################################### 

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
	
	dt = clock.tick(30) # 게임 화면의 초당 프레임 수를 설정 

	## 2. 이벤트 처리 (키보드, 마우스 등)
	for event in pygame.event.get():  # 반드시 써야하는 부분 (이벤트 발생 체크)
		if event.type == pygame.QUIT: # 창 닫기버튼 누를때
			running = False

		if event.type == pygame.KEYDOWN: # 키보드 키가 눌러짐
			if event.key == pygame.K_LEFT:
				character_to_x -= character_speed
			elif event.key == pygame.K_RIGHT:
				character_to_x += character_speed
			elif event.key == pygame.K_SPACE: # 무기 발사
				# 무기 위치 설정
				weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
				weapon_y_pos = character_y_pos
				# 리스트에 좌표 추가
				weapons.append([weapon_x_pos, weapon_y_pos])
			
		if event.type == pygame.KEYUP: # 방향키를 떼면 멈춤
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				character_to_x = 0

	## 3. 캐릭터 위치 정의
	character_x_pos += character_to_x * dt

	# 창에서 벗어나지 않도록 제한
	if character_x_pos < 0:
		character_x_pos = 0
	elif character_x_pos > screen_width - character_width:
		character_x_pos = screen_width - character_width

	# 무기 위치 조정 ==> 한줄 for 문 활용
	# [w[0], w[1] - weapon_speed] : 처리한 결과들을 또다른 하나의 리스트로 감싸서 weapons 로 할당
	# 100,200 -> 180 160 140..... 작아질수록 위로 올라가는것
	weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

	# 천장에 닿은 무기 없애기
	weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0] # y좌표가 0보다 작으면 사라짐

	# 공 위치 정의
	# enumerate : 인덱스 정보도 가져올 수 있음
	for ball_idx, ball_val in enumerate(balls):
		ball_pos_x = ball_val["pos_x"]
		ball_pos_y = ball_val["pos_y"]
		ball_img_idx = ball_val["img_idx"]
		
		ball_size = ball_images[ball_img_idx].get_rect().size
		ball_width = ball_size[0]
		ball_height = ball_size[1]

		# 양옆 벽에 닿았을 때 공 이동 위치 변경 (튕겨나오는 효과)		
		if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
			ball_val["to_x"] = ball_val["to_x"] * -1
		# 스테이지(바닥)에 튕겨서 올라가는 처리
		if ball_pos_y >= screen_height - stage_height - ball_height:
			ball_val["to_y"] = ball_val["init_spd_y"] # 다시 최초속도로 설정됨
		else: 
			ball_val["to_y"] += 0.5 # 포물선을 그리기 위함
			'''
			to_y rk (상승곡선) -6 => -5.5 => -4.5 ... => 0 => (하강곡선) 0.5 => 0.1 ... 
			절대값이 커질수록 한번에 이동을 많이 함 
			 = 속도가 빨라짐 (위로갈수록 느리고 아래로갈수록 빨라지는 효과)
			'''

		ball_val["pos_x"] += ball_val["to_x"]
		ball_val["pos_y"] += ball_val["to_y"]

	## 4. 충돌처리
	# 충돌처리를 위한 rect 정보 업데이트
	character_rect = character.get_rect() # 업데이트 안해주면 초기값 그대로 유지됨
	character_rect.left = character_x_pos # 따라서 이동한 위치로 업데이트해줘야함
	character_rect.top = character_y_pos 
	
	for ball_idx, ball_val in enumerate(balls):
		# 현재 공 위치
		ball_pos_x = ball_val["pos_x"]
		ball_pos_y = ball_val["pos_y"]
		ball_img_idx = ball_val["img_idx"]
		
		# 공 rect 정보 업데이트
		ball_rect = ball_images[ball_img_idx].get_rect()
		ball_rect.left = ball_pos_x
		ball_rect.top = ball_pos_y

		# 공과 캐릭터 충돌 처리
		if character_rect.colliderect(ball_rect):
			running = False
			break
		
		for weapon_idx, weapon_val in enumerate(weapons):
			weapon_pos_x = weapon_val[0]
			weapon_pos_y = weapon_val[1]

			# 무기 rect 정보 업데이트
			weapon_rect = weapon.get_rect()
			weapon_rect.left = weapon_pos_x
			weapon_rect.top = weapon_pos_y

			# 공과 무기들 충돌 처리
			if weapon_rect.colliderect(ball_rect):
				# 해당 무기와 공을 없애기 위한 값 설정
				weapon_to_remove = weapon_idx
				ball_to_remove = ball_idx

				# 가장 작은 크기의 공 (index : 3)이 아니라면, 다음 단계의 공으로 나누어주기 
				if ball_img_idx < 3 : 
					# 현재 공 크기 정보를 가지고 옴
					ball_width = ball_rect.size[0]
					ball_height = ball_rect.size[1]

					# 나눠진 공 이미지 정보
					small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
					small_ball_width = small_ball_rect.size[0]
					small_ball_height = small_ball_rect.size[1]

					# 왼쪽으로 튕겨 나가는 작은 공
					balls.append({
						"pos_x": ball_pos_x + ((ball_width / 2) - (small_ball_width / 2)), #공이 그려지는 x좌표
						"pos_y": ball_pos_y + ((ball_height / 2) - (small_ball_height / 2)), #공이 그려지는 y좌표
						"img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
						"to_x": -3, # x축 이동 방향 (음수면 왼쪽, 양수면 오른쪽)
						"to_y": -6, # y축 이동방향
						"init_spd_y" : ball_spped_y[ball_img_idx + 1] # y 최초 속도
					})
					# 오른쪽으로 튕겨 나가는 작은 공
					balls.append({
						"pos_x": ball_pos_x + ((ball_width / 2) - (small_ball_width / 2)),
						"pos_y": ball_pos_y + ((ball_height / 2) - (small_ball_height / 2)), 
						"img_idx" : ball_img_idx + 1, #공의 이미지 인덱스
						"to_x": 3, # x축 이동 방향 (음수면 왼쪽, 양수면 오른쪽)
						"to_y": -6, # y축 이동방향
						"init_spd_y" : ball_spped_y[ball_img_idx + 1] # y 최초 속도
					})

				break # 안쪽 for문 탈출

		else: # weapons 값이 없으면 여기를 거침 (if-else 처럼 동작)
			continue # 안쪽 for 문 조건이 맞지 않은 경우. 바깥 for 문 계속 수행

		break # for-else (안쪽 for문)에서 break를 만나야 여기에 진입. 2중 for문 한번에 탈출

	# 충돌된 공과 무기 없애기
	if ball_to_remove > -1:
		del balls[ball_to_remove]
		ball_to_remove = -1
	if weapon_to_remove > -1:
		del weapons[weapon_to_remove]
		weapon_to_remove = -1
	
	# 모든 공을 없앤 경우 게임 종료 (성공)
	if len(balls) == 0:
		game_result = "Mission Complete"
		running = False

	## 5. 화면에 그리기
	screen.blit(background, (0,0))
	
	# 무기를 먼저 그려야 그 위에 캐릭터가 덮어짐
	for weapon_x_pos, weapon_y_pos in weapons:
		screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

	# 공 그리기 
	for idx, val in enumerate(balls):
		ball_pos_x = val["pos_x"]
		ball_pos_y = val["pos_y"]
		ball_img_idx = val["img_idx"]
		screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

	screen.blit(stage, (0, screen_height - stage_height))
	screen.blit(character, (character_x_pos, character_y_pos))
	
	# 경과 시간 계산
	elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
	timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255)) # 흰색
	screen.blit(timer, (10,10))

	if(total_time - elapsed_time <= 0):
		game_result = "Time Over"
		running = False

	# 반드시 호출되어야 하는 부분 : 화면을 다시 그리기
	pygame.display.update()


msg = game_font.render(game_result, True, (255,255,0)) # 노란색
# 메시지가 화면 중앙에 나오도록 설정 (center(width, height)) 
# int 로 감싸는것은 실수를 정수화하기 위함
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)
# pygame 종료
pygame.quit()
