import pygame, math

# 보석 클래스
class Gemstone(pygame.sprite.Sprite):
	def __init__(self, image, position, price, speed):
		super().__init__()
		self.image = image
		self.rect = image.get_rect(center=position)

		self.price = price
		self.speed = speed
	
	def set_poisition(self, claw_position, claw_angle):
		radi_angle = math.radians(claw_angle)
		r = self.rect.size[0] // 2 # 반지름 = width/2
		gemstone_to_x = r * math.cos(radi_angle)
		gemstone_to_y = r * math.sin(radi_angle)
		self.rect.center = (claw_position[0] + gemstone_to_x, claw_position[1] + gemstone_to_y)

# 집게 클래스
class Claw(pygame.sprite.Sprite):
	def __init__(self, image, position):
		super().__init__()
		self.image = image
		self.rect = image.get_rect(center=position)

		self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
		self.position = position

		self.direction = LEFT # 집게 이동 방향
		self.angle_speed = 2.5  # 집게의 각도 변경 폭 (좌우 이동 속도)
		self.angle = 10 # 최초 각도 정의 (천장-오른쪽 끝)

		self.ori_image = image

	def draw(self, screen): # 스프라이트 그룹 없이 draw 사용하기 위함
		screen.blit(self.image, self.rect)
		# 화면기준 중심점부터 헌재 중심점(offset 으로 이동한 중심점). 두께 5 
		# pygame.draw.circle(screen, (255,0,0), self.position, 3) # 중심점 표시
		pygame.draw.line(screen, (0,0,0), self.position, self.rect.center, 5) # 직선 그리기

	def update(self, to_x):
		'''
			Sprite 클래스의 Update 
			: 이미지 여러개를 리스트에 담고 반복해서 움직이는 것처럼 보이게해주는데 쓰임
			=> 여기서는 이 용도로 쓰이지 않음
		'''
		# 각도 조정
		if self.direction == LEFT : #왼쪽 방향이면 각도가 커지는 것
			self.angle += self.angle_speed
		elif self.direction == RIGHT : # 오른쪽 방향이면 각도가 작아지는 것
			self.angle  -= self.angle_speed
		
		if self.angle > 170: # 왼쪽 최대 각도 벗어나면
			self.angle = 170
			self.self_direction(RIGHT)
		elif self.angle < 10:
			self.angle = 10
			self.self_direction(LEFT)

		if self.direction != STOP:
			self.ori_direction = self.direction
			
		'''
			이미지가 회전되면서 각도가 변하므로, x 좌표기준으로 뻗어나갈 때 아래쪽으로 내려가게 됨
		'''
		self.offset.x += to_x # 집게가 멈추었을 때 각도기준으로 to_x만큼씩 뻗어나감

		# 회전 처리
		self.rotate()

		# 이미지 위치 이동
		# rect_center = self.position + self.offset
		# self.rect = self.image.get_rect(center = rect_center)

	def rotate(self):
		# pygame.transform.rotate() 보다 아래가 매끄러움
		# 시계방향이어야 하므로 마이너스(-)를 붙어야 함 (기본이 시계 반대방향)
		self.image = pygame.transform.rotozoom(self.ori_image, -self.angle, 1)
		offset_rotated = self.offset.rotate(self.angle) # offset 데이터를 각도만큼 회전시킨 새 offset 을 구함
		self.rect = self.image.get_rect(center = self.position + offset_rotated)

	def self_direction(self, direction):
		self.direction = direction

	def set_init_state(self, ori_dircetion):
		self.offset.x = default_offset_x_claw
		# self.angle = 10
		self.direction = ori_dircetion


LEFT = -1 # 집게 왼쪽 방향
RIGHT = 1 # 집게 오른쪽 방향
STOP = 0 # 집게 멈춤

default_offset_x_claw = 40 # 중심점을부터 집게까지의 기본 x 간격
# to_x = 0 # x좌표 기준으로 집게 이미지를 이동시킬 값 저장 변수

# # 속도 변수
# move_speed = 12 # 집게 발사 시 이동 스피드 (x 좌표 기준으로 증가되는 값)
# return_speed = -20 # 아무것도 없이 집게가 돌아오는 스피드
