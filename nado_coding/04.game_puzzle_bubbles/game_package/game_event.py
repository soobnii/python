import pygame
import os, random, math
from game_class import Bubble, Pointer
from game_variable import * 

# 천장 내려오는 버전

### ▼ 함수 영역####################################################

# 웹 생성 (초기 버블 셋팅) 
def setup():
	global map # 전역변수 map 사용
	
	map = [
		list(random_color_set(8)), # 문자열을 윗줄처럼 리스트 형태로 만들어줆
		list(random_color_set(7)), # / 는 버블이 위치할 수 없는 곳
		list(random_color_set(8)),
		list(random_color_set(7)),
		list("........"), # . 은 비어있는 곳
		list("......./"),
		list("........"),
		list("......../"),
		list("........"),
		list("......../"),
		list("........") # 총 11줄까지 있음
	]

	for row_idx, row in enumerate(map):
		for col_idx, _color in enumerate(row):
			if _color in [".", "/"]:
				continue
			position = get_bubble_position(row_idx, col_idx)
			image = get_bubble_image(_color)
			# 클래스로 객체 생성
			_bubble = Bubble(image, _color, position, row_idx, col_idx)
			bubble_group.add(_bubble)

def random_color_set(n):
	rowColor = []
	for i in range(0,n):
		rowColor.append(random.choice(ALL_COLORS))
	if n == 7:
		rowColor.append("/")
	return ''.join(rowColor)

def get_bubble_position(row_idx, col_idx):
	'''
		버블 위치 구하기 (버블 센터 기준)
		// 는 나누기 몫을 가져옴 (정수화. 내림계산. ex. -0.12 => -1)
		x 좌표 : 셀 가로 크기 * col_idx + 버블가로크기//2
		y 좌표 : 셀 세로 크기 * row_idx + 버블세로크기//2
		단, row_idx 가 홀수이면 버블을 오른쪽으로 더 이동시켜야하므로
		셀 가로 크기 * col_idx + 버블가로크기//2 + 셀 가로크기 // 2
	'''
	pos_x = col_idx * CELL_SIZE + (BUBBLE_WIDTH // 2)
	pos_y = row_idx * CELL_SIZE + (BUBBLE_HEIGHT // 2) + wall_height
	if row_idx % 2 == 1 :
		pos_x += CELL_SIZE // 2 
	return pos_x, pos_y

def get_bubble_image(color):
	if color == "R":
		return bubble_images[0]
	if color == "Y":
		return bubble_images[1]
	if color == "B":
		return bubble_images[2]
	if color == "G":
		return bubble_images[3]
	if color == "P":
		return bubble_images[4]
	else:
		return bubble_images[5]
		# return bubble_images[-1] 같음

def prepare_bubbles():
	global curr_bubble, next_bubble
	if next_bubble:
		curr_bubble = next_bubble
	else:
		curr_bubble = create_bubble()
	curr_bubble.set_rect((SCREEN_WIDTH//2, 624)) # 포인터 세로 위치와 같음
	
	next_bubble = create_bubble()
	if next_bubble:
		next_bubble.set_rect((SCREEN_WIDTH//4, 688))

def create_bubble():
	color = get_random_bubble_color()
	if color:
		image = get_bubble_image(color)
		return Bubble(image, color) # 여기서 rect 설정 X. B/C next Bubble 이 current 로 바뀔 때 어차피 변경해야함

def get_random_bubble_color():
	# 쉬운 게임을 위해 현재 맵에 남아있는 색에서 뽑아주기
	colors = []
	for row in map:
		for col in row: # col 이 곧 color
			if col not in [".", "/"] and col not in colors:
				colors.append(col)
	
	if len(colors) > 0:
		return random.choice(colors)
	# random = [""]

def process_collision():
	global curr_bubble, fire, curr_fire_count
	
	''' 
		- pygame.sprite.spritecollideany
		그룹 내에 있는 것 중 충돌된 것을 가져옴
		buggle_group 과 curr_bubble 이 투명영역을 제외하고 충돌되면, 충돌한 버블을 가져옴
		이미지 가져올때 convert_alpha 사용해야함
	'''
	hit_bubble = pygame.sprite.spritecollideany(curr_bubble, bubble_group, pygame.sprite.collide_mask)
	
	'''
		curr_bubble 이 충돌한 위치 좌표를 구하여, index 구하기
		row index = y 좌표 // 셀 세로 크기
		col index = x 좌표 // 셀 가로 크기
		단, row index가 홀수인 경우, col index = (x 좌표 - (셀 가로크기//2)) // 셀 가로 크기

		버블이 천장에 닿으면, 그 위치 기준으로 배치시켜야함
	'''
	# if hit_bubble or curr_bubble.rect.top <= 0:
	if hit_bubble or curr_bubble.rect.top <= wall_height: # 천장에 부딛혔을때
		'''
			rect.center : 좌표 정보를 tuple 로 return해줌 
			앞에 * 을 붙여주면 unpacking 되어 전달됨 ==> 받을 때 (x,y) 로 받을 수 있음
		'''
		row_idx, col_idx = get_map_idx(*curr_bubble.rect.center)
		
		# 새로 쏜 버블을 위에 구한 index 에 위치시켜야함
		place_bubble(curr_bubble, row_idx, col_idx)

		remove_bubbles(row_idx, col_idx, curr_bubble.color)

		curr_bubble = None
		fire = False
		curr_fire_count -= 1

def get_map_idx(x, y):
	# row_idx = y // CELL_SIZE
	row_idx = (y - wall_height) // CELL_SIZE
	'''
		천장이 내려온후 버블이 그만큼 y좌표가 더해졌기 때문에,
		원래 row_idx 를 구하려면 y 좌표에서 천장 높이를 빼야한다.
		--
		row_idx 가 음수이면 0이어야 하고, 최대값보다 커지면 안된다. 
		공의 일부가 화면밖으로 나간 상태에서 충돌할 수 있기 때문에 설정해줘야함
	'''
	if row_idx % 2 == 1:
		col_idx = (x- (CELL_SIZE//2)) // CELL_SIZE
		if col_idx < 0:
			col_idx = 0
		elif col_idx > MAP_COl_INDEX - 1:
			col_idx = MAP_COl_INDEX - 1
	else:
		col_idx = x // CELL_SIZE
	return row_idx, col_idx

def place_bubble(bubble, row_idx, col_idx):
	# 버블을 map 에 넣어줌
	map[row_idx][col_idx] = bubble.color # color 는 클래스에서 정의함
	
	# index 기준으로 배치된 버블의 최종 position(좌표) 구해서 rect 정보 추가
	poisition = get_bubble_position(row_idx, col_idx)
	bubble.set_rect(poisition) # rect 정보 추가
	# bubble.set_map_index(row_idx, col_idx)
	bubble.row_idx = row_idx
	bubble.col_idx = col_idx

	# 다음 버블 충돌 처리를 위해 sprite 그룹에 추가
	bubble_group.add(bubble)

def remove_bubbles(row_idx, col_idx, color):
	visited.clear()
	visit(row_idx, col_idx, color)
	if len(visited) >= 3:
		remove_visited_bubbles()
		remove_hanging_bubbles() # 밑에 남아있는 버블 떨구기

def visit(row_idx, col_idx, color = None):
	# 인덱스가 맵의 범위 넘어가면 안됨
	if row_idx < 0 or row_idx > MAP_ROW_INDEX \
		or col_idx < 0 or col_idx > MAP_COl_INDEX:
		return
	# 현재 방문한 셀의 버블색이 color 와 같은지 확인
	if color and map[row_idx][col_idx] != color:
		return
	# 이미 방문한 곳이면 pass
	if (row_idx, col_idx) in visited:
		return 
	# 빈 공간이거나 버블이 존배할 수 없는 위치일 때 pass
	if map[row_idx][col_idx] in [".","/"]:
		return
	
	# 조건을 만족한 버블을 기록
	visited.append((row_idx, col_idx))
	
	#재귀함수로 탐색 (row, col) 이 순서대로 한쌍
	rows = [0,-1,-1,0,1,1] 
	if row_idx % 2 ==1:
		cols = [-1,0,1,1,1,0]
	else:
		cols = [-1,-1,0,1,0,-1]

	for i in range(len(rows)):
		visit(row_idx + rows[i], col_idx + cols[i], color)

def remove_visited_bubbles():
	# 한줄 for 문 ==> if  문을 만족하는 것만 가져와서 리스트화
	bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) in visited]
	for bubble in bubbles_to_remove:
		map[bubble.row_idx][bubble.col_idx] = "." # 화면에서 버블 삭제
		bubble_group.remove(bubble) # sprite 그룹에서 삭제

def remove_hanging_bubbles():
	visited.clear()
	for col_idx in range(MAP_COl_INDEX + 1):
		# 밑에 남아있는 버블 좌표 구하려면, 최상단인 row index 0 의 각 열에서 출발해서 찾아야한다.
		if map[0][col_idx] != ".": # 첫줄은 / 가 없음
			visit(0, col_idx) # 색이랑 상관없이 그냥 버블이 있는것만 찾으면 됨
	remove_not_visited_bubbles()

def remove_not_visited_bubbles():
	# 방문하지 않은 버블만 삭제
	bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) not in visited]
	for bubble in bubbles_to_remove:
		map[bubble.row_idx][bubble.col_idx] = "." 
		bubble_group.remove(bubble)

def draw_bubbles():
	to_x = None
	if curr_fire_count == 2:
		to_x = random.randint(-1,1) # -1 에서 1
	elif curr_fire_count == 1:
		to_x = random.randint(-4,4)

	for bubble in bubble_group:
		bubble.draw(screen, to_x)

def drop_wall():
	global wall_height, curr_fire_count
	wall_height += CELL_SIZE # 셀크기(높이) 만큼 떨어짐
	for bubble in bubble_group:
		bubble.drop_downward(CELL_SIZE) # 모든 버블도 다 위치 내림
	curr_fire_count = FIRE_COUNT

def get_lowest_bubble_bottom():
	bubble_bottoms = [b.rect.bottom for b in bubble_group]
	# bottom 이 클수록 밑에있는 것
	return max(bubble_bottoms)

def change_bubble_color():
	for bubble in bubble_group:
		bubble.image = bubble_images[-1]


### ▼ 반드시 해야하는 프레임 셋팅##################################################

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Puzzle Bobble")

clock = pygame.time.Clock()

### ▼ 전역변수 및 객체, 이미지 생성, 함수 실행 영역####################################################

# 배경 이미지
current_path = os.path.dirname(__file__) # 현재 파일 위치 반환
# parent_path = os.path.join(current_path, os.pardir) # pardir = .. 
image_path = os.path.join(current_path, "..\images") # 폴더 위치 반환

background = pygame.image.load(os.path.join(image_path, "background.png"))
wall = pygame.image.load(os.path.join(image_path, "wall.png"))

# 버블 이미지 
# convert_alpha() : 이미지의 흰배경을 투명화시킴? => 충돌 처리시 네모가 아닌 실제 버블모양기준으로 잡을 수 있음
bubble_images = [
	pygame.image.load(os.path.join(image_path, "red.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "yellow.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "blue.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "green.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "purple.png")).convert_alpha(),
	pygame.image.load(os.path.join(image_path, "black.png")).convert_alpha()
]

# 발사대 이미지
pointer_image = pygame.image.load(os.path.join(image_path, "pointer.png"))

# 발사대 생성
pointer = Pointer(pointer_image, (SCREEN_WIDTH//2, 624), 90) # 클래스로 객체 생성(가로, 세로 위치 및 각도 지정)

# sprite 그룹 생성
bubble_group = pygame.sprite.Group() 

map = [] # 맵

#to_angle = 0 # 화살표가 좌우로 움직일 각도 정보 ( → : 0도 인상태 )
'''
to_angle 만 사용할 시, 화살표키를 빠르게 누르다보면(왼->오)
두 event 가 함께 인식되서 화살표가 안움직는 현상이 발생함 (오른쪽으로 이동안함)
'''
to_angle_left = 0 # 왼쪽키를 눌렀을 때(왼쪽으로 움직일 각도 정보)
to_angle_right = 0 # 오른쪽 키를 눌렀을 때(오른쪽으로 움직일 각도 정보)
angle_spped = 1.5 # 화살표 각도 조절 속도 (화살표가 1.5도씩 움직이게 됨)

curr_bubble = None # 새로 쏠 버블
fire = False # 발사중일때만 True
next_bubble = None # 다음에 쏠 버블

visited = [] # 버블을 쏜 후 탐색 위치 기록

curr_fire_count = FIRE_COUNT #  FIRE_COUNT 번중에 남은 횟수
curr_fire_count_font = pygame.font.SysFont("arialrounded", 30)

wall_height = 0 # 천장벽 높이

is_game_over = False
game_font = pygame.font.SysFont("arialrounded", 40)
game_result = None

###################################

# 함수 실행
setup()

### ▼ 게임 러닝######################################################
running = True
while running:
	clock.tick(60) # FPS 60 으로 설정

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				# to_angle += angle_spped
				to_angle_left += angle_spped
			elif event.key == pygame.K_RIGHT:
				# to_angle -= angle_spped
				to_angle_right -= angle_spped # 음수가 됨
			elif event.key == pygame.K_SPACE:
				if curr_bubble and not fire: #쏠 버블이 있고, fire 가 false 인 경우
					fire = True
					curr_bubble.set_angle(pointer.angle) # 현재 포인터의 각도

		if event.type == pygame.KEYUP:
			# if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
			# 	to_angle = 0
			if event.key == pygame.K_LEFT:
				to_angle_left = 0
			elif event.key == pygame.K_RIGHT:
				to_angle_right = 0

	################################
	if not curr_bubble: # None 인 경우
		prepare_bubbles()

	if fire:
		process_collision() # 충돌처리 

	if curr_fire_count == 0:
		drop_wall()

	if not bubble_group:
		game_result = "Mission Complete"
		is_game_over =  True
	elif get_lowest_bubble_bottom() > len(map) * CELL_SIZE :
		# 가장 밑에있는 버블의 bottm 이 map 행(10) * 셀크기 보다 크면
		game_result = "Game Over"
		is_game_over =  True
		change_bubble_color() # 실패하면 모든 버블의 색을 검정색으로 변경

	screen.blit(background, (0,0))
	screen.blit(wall, (0, wall_height - SCREEN_HEIGHT)) # - 인만큼 화면보다 위에 있어서 보이지 않음

	# 화면 흔들기
	# bubble_group.draw(screen) # 스프라이트 그룹에 있는 모든 스프라이트를 스크린에 그려줌
	# 위 draw 함수는 sprite group 기본으로 제공해주는 함수
	draw_bubbles()

	# pointer.rotate(to_angle)
	pointer.rotate(to_angle_left + to_angle_right)
	pointer.draw(screen) # 원래 스프라이트는 draw 함수가 없는데 Pointer 클래스에서 정의해줌. screen.blit 을 사용해도 된다.
	
	# 포인터 위에 새 버블 그려야함(나중에 그리기)
	if curr_bubble:
		if fire:
			curr_bubble.move() # fire 가 false 일 때까지, 프레임마자  이동하면서 (위로 올라가면서) 그려줌

		curr_bubble.draw(screen)

	if next_bubble:
		next_bubble.draw(screen)

	if curr_fire_count:
		txt_fire_count = curr_fire_count_font.render(str(curr_fire_count), True, (255,255,255))
		rect_fire_count = txt_fire_count.get_rect(center=(SCREEN_WIDTH-20,SCREEN_HEIGHT-20))
		screen.blit(txt_fire_count, rect_fire_count)

	if is_game_over:
		txt_game_over = game_font.render(game_result, True, (255,255,255))
		rect_game_over = txt_game_over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
		screen.blit(txt_game_over, rect_game_over)
		# running = False

	pygame.display.update()

pygame.quit()
