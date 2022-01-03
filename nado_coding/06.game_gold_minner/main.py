import pygame, os, random
from _class import Gemstone, Claw, STOP, default_offset_x_claw

def setup_gemstone():	
	# 보석 객체 생성
	small_gold = Gemstone(gemstone_images[0], random_poistion(0), price[0], speed[0])
	gemstone_group.add(small_gold)
	gemstone_group.add(Gemstone(gemstone_images[1], random_poistion(1), price[1], speed[1]))
	gemstone_group.add(Gemstone(gemstone_images[2], random_poistion(2), price[2], speed[2]))
	gemstone_group.add(Gemstone(gemstone_images[3], random_poistion(3), price[3], speed[3]))

	for i in range(0, 4):
		index = random.randint(0,3)
		gemstone_group.add(Gemstone(gemstone_images[index], random_poistion(index), price[index], speed[index]))

def random_poistion(index):
	x = random.uniform(50.0, screen_width-50.0)
	y = random.uniform(200.0, screen_height-50.0)
	temp = Gemstone(gemstone_images[0], (x,y), price[index], speed[index])

	for gemstone in gemstone_group:
		if gemstone.rect.colliderect(temp.rect) :
			(x, y) = random_poistion(index)
			break
	return (x,y)

def update_score(score):
	global curr_score
	curr_score += score

def display_score():
	'''
		세자리마다 콤마(,)를 넣는 포맷 지정
	'''
	text_curr_score = game_font.render(f"Current Score : {curr_score: ,}", True, (0,0,0))
	screen.blit(text_curr_score, (50,20))
	text_goal_score = game_font.render(f"Goal Score : {goal_score: ,}", True, (0,0,0))
	screen.blit(text_goal_score, (50,80))

def display_time(time):
	text_timer = game_font.render(f"Time : {time}", True, (0,0,0))
	screen.blit(text_timer, (1100, 50))

def display_game_over():
	game_font = pygame.font.SysFont("arialrounded", 60)
	text_game_over = game_font.render(game_result, True, (0,0,0))
	rect_game_over = text_game_over.get_rect(center=(int(screen_width/2), int(screen_height/2)))
	screen.blit(text_game_over, rect_game_over) # 화면 중앙에 표시
###################################

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("황금 캐기")
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("arialrounded", 30)

current_path = os.path.dirname(__file__) # 현재 파일 위치 반환
image_path = os.path.join(current_path, "images") # 폴더 위치 반환
background = pygame.image.load(os.path.join(image_path, "background.png"))
character = pygame.image.load(os.path.join(image_path, "person.png"))
character = pygame.transform.scale(character, (70, 70))

gemstone_images = [
	pygame.image.load(os.path.join(image_path, "small_gold.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "big_gold.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "stone.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "diamond.png")).convert_alpha()
]
gemstone_group = pygame.sprite.Group()

price = [100, 300, 10, 600] # small_gold, big_gold, stone, diamond
speed = [5, 4, 4, 7]

claw_image = pygame.image.load(os.path.join(image_path, "claw.png"))
claw = Claw(claw_image, ((screen_width//2), character.get_height()))

goal_score = 1000
curr_score = 0

game_result = None
total_time = 60
start_ticks = pygame.time.get_ticks() # 시작할 때 시간(tick)을 받아옴

###################################
# 집게 속도 변수
move_speed = 12 # 집게 발사 시 이동 스피드 (x 좌표 기준으로 증가되는 값)
return_speed = -20 # 아무것도 없이 집게가 돌아오는 스피드

# 집게 이동 변수
to_x = 0 # x좌표 기준으로 집게 이미지를 이동시킬 값 저장 변수

# 집게를 뻗어서 잡은 보석 정보
caught_gemstone = None 
###################################
setup_gemstone()

running = True
while running:
	clock.tick(60) # FPS 60 으로 설정
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			claw.self_direction(STOP) # 좌우멈춤
			to_x = move_speed # move_speed 만큼 뻗게됨 (update 에서 반영)
		
	if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
		# 집게 왼쪽/오른쪽/아래쪽 위치가 화면 밖으로 넘어가면
		to_x = return_speed
	
	if claw.offset.x < default_offset_x_claw : #원위치에 오면
		to_x = 0
		claw.set_init_state(claw.ori_direction) # 다시 시작
		
		if caught_gemstone: #잡힌 보석을 없애기 
			update_score(caught_gemstone.price) # 점수 업데이트
			gemstone_group.remove(caught_gemstone)
			caught_gemstone = None

	if not caught_gemstone: #잡힌 보석이 없으면 충돌체크
		for gemstone in gemstone_group:
			'''
				claw.rect.colliderect(gemstone.rect) : 직사각형 기준 충돌
				pygame.sprite.collide_mask(claw, gemstone) : 투명한 영역 제외 충돌 
					==> 이미지의 alpha(투명도)값 설정 필요
			'''
			if pygame.sprite.collide_mask(claw, gemstone):
				caught_gemstone = gemstone # 잡힌 보석
				'''
					잡힌 보석의 속도를 이동 속도로 설정 (원점으로 돌아가는 방향이므로 음수(-))
				'''
				to_x = -gemstone.speed
				break
	elif caught_gemstone:
		'''
			집게가 닿으면 보석 위치를 집게쪽으로 이동시킴 (집게와 같이 이동)
				==> 집게 중심좌표와 보석 중심좌표가 일직선 상에 있도록 함
		'''
		caught_gemstone.set_poisition(claw.rect.center, claw.angle)

	screen.blit(background, (0,0))
	screen.blit(character, ((screen_width/2)-35, 0))
	
	#그룹 내 모든 스프라이트를 screen 에 그림
	gemstone_group.draw(screen)
	claw.update(to_x)
	claw.draw(screen)

	# 점수 정보
	display_score()

	# 시간 계산
	elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms => s
	display_time(total_time - int(elapsed_time)) # 남은 시간 표시

	if total_time - int(elapsed_time) <= 0 :
		running = False
		# if curr_score >= goal_score:
		# 	game_result = "Mission Complete"
		# else: 
		# 	game_result = "Game Over"
		game_result = "Game Over"	
		display_game_over()

	if len(gemstone_group) == 0:
		running = False
		game_result = "Mission Complete"
		display_game_over()
	
	if curr_score >= goal_score:
		running = False
		game_result = "Mission Complete"
		display_game_over()

	pygame.display.update()

pygame.time.delay(2000)
pygame.quit()


'''
PyInstaller 패키징 방법
	pip install pyinstaller
	pyinstaller -w main.py  (pyinstaller -w {파일명})
		=> --add-data *.png 처럼 사용한 파일명 명시해야 하지만, 패키징 후 리소스 파일을 그대로 붙여넣어도 됨
		=> dist 폴더에 경로에 맞게 게임 이미지를 넣어주면 됨
		=> exe 파일 클릭 시 파이썬이 설치되어 있지 않은 곳에서도 게임 실행 가능
		=> dist 내 폴더를 압축해서 공유 가능

-w : window 모드 (터미널창 뜨지 않음) 
'''