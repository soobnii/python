import pygame, random

# 9*5, 한 칸당 120*120
# 숫자 개수 = (레벨 // 3) + 5 , min(숫자개수, 20) : 최대개수가 20

def display_start_screen():
	pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)
	
	msg = game_font.render(f"{curr_level}", True, WHITE)
	msg_rect = msg.get_rect(center=start_button.center)
	screen.blit(msg, msg_rect)

def display_game_screen():
	global hidden
	if not hidden:
		# 게임 경과 시간 = (현재시간 - 시작버튼 클릭 시간) / 1000 : ms => s 
		elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
		
		elapsed_time_font = game_font.render(str(int(elapsed_time)), True, GRAY)
		screen.blit(elapsed_time_font, (0,0))

		if elapsed_time > display_time:
			hidden = True
		
	for idx, rect_btn in enumerate(number_buttons, start=1):
		if hidden:
			# 사각형 버튼 그리기
			pygame.draw.rect(screen, WHITE, rect_btn)
		else:
			# 실제 숫자 텍스트
			cell_text = game_font.render(str(idx), True, WHITE)
			# 텍스트 중앙을 btn 중앙으로 맞춤
			text_rect = cell_text.get_rect(center = rect_btn.center)
			screen.blit(cell_text, text_rect)
	
def check_buttons(button_position): # 클릭한 버튼 확인
	global start, start_ticks
	'''
		A.collidepoint(B) : A 정보(rectangle)내에 B 좌표가 포함되는지 확인 
	''' 
	if start: # 게임이 시작했으면 (시작버튼이 아니면)
		check_number_buttons(button_position)
	elif start_button.collidepoint(button_position):
		start = True
		# 현재 시간 저장 (타이머 시작)
		start_ticks = pygame.time.get_ticks()		

def setup(level):
	# 얼마동안 숫자를 보여줄지
	global display_time
	display_time = 5 - (level//3)
	display_time = max(display_time, 1)

	# 보여줄 숫자 개수
	number_count = (level//3) + 5
	number_count = min(number_count, 20)	
	shuffle_grid(number_count)

def shuffle_grid(number_count):
	rows = 5; columns = 9
	cell_size = 130; button_size = 110
	screen_left_margin = 55; screen_top_margin = 20
	'''
		한줄 for 문으로 grid 생성
		[
			[0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0],
				.....
		]
	'''
	grid = [ [0 for col in range(columns)] for row in range(rows) ]
	
	num = 1 # 숫자는 1부터 number_count 까지 1씩 증가
	while num <= number_count:
		row_idx = random.randrange(0,rows) # 0부터 rows 미만
		col_idx = random.randrange(0,columns)
		if grid[row_idx][col_idx] == 0:
			grid[row_idx][col_idx] = num
			num += 1

			# 현재 셀 위치 기준으로 x, y 위치를 구함
			center_x = screen_left_margin + (col_idx * cell_size) + (cell_size/2)
			center_y = screen_top_margin + (row_idx * cell_size) + (cell_size/2)
			# 숫자 버튼 그리기
			button = pygame.Rect(0, 0, button_size, button_size)
			button.center = (center_x, center_y)

			number_buttons.append(button)

def check_number_buttons(position):
	global hidden, start, curr_level
	for button in number_buttons:
		# 클릭한 버튼과 숫자 버튼 위치 비교
		if button.collidepoint(position):
			if button == number_buttons[0]:
				# 클릭한 버튼이 가장 첫번째 인덱스 버튼이어야 함
				# 계속 DELETE 되므로 항상 0번째 인덱스와 비교
				del number_buttons[0]
				if not hidden:
					hidden = True
			else: # 잘못된 숫자 클릭
				game_over()
			break

	# 모든 숫자를 맞추면 레벨업
	if len(number_buttons) == 0:
		start = False
		hidden = False
		curr_level += 1
		setup(curr_level)
 
def game_over():
	global running
	running = False

	msg = game_font.render(f"Your level is {curr_level}", True, WHITE)
	msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))
	screen.fill(BLACK)
	screen.blit(msg, msg_rect)

###################################

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("기억력 테스트")
game_font = pygame.font.Font(None, 120)

###################################
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (50,50,50)

start_button = pygame.Rect(0,0,120,120) # RECT 객체 생성
start_button.center = (120, screen_height - 120) # 중심값 설정

start = False
number_buttons = []
curr_level = 1
hidden = False # 숫자 숨김 여부
display_time = None # 숫자 보여주는 시간 (레벨에 따라 달라짐)
start_ticks = None # 시간 계산을 위함 (현재 시간 정보 저장)
###################################
setup(curr_level)
running = True
while running:

	click_position = None

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONUP: # 마우스 클릭
			click_position = pygame.mouse.get_pos() # 클릭한 좌표

	# 화면 전체를 검정색으로 칠함
	screen.fill(BLACK)

	if start:
		display_game_screen() # 게임 화면 표시
	else:
		# 시작 버튼 표시 : 반지름값(120/2), 두께 5
		display_start_screen() # 시작 화면 표시

	if click_position:
		check_buttons(click_position)
		
	pygame.display.update()

pygame.time.delay(3000)
pygame.quit()


