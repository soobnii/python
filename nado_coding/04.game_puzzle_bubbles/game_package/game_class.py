import pygame
import math
from game_variable import SCREEN_WIDTH

class Bubble(pygame.sprite.Sprite): # Sprite 상속
	def __init__(self, image, color, position=(0,0), row_idx=-1, col_idx = -1): 
		# current_bubble 은 position 과 index 설정할 필요 없으므로 그냥 default 값 부여

		super().__init__() # 상속받은 init 메소드 호출
		# Sprite 상속받으면 image와 rect 는 반드시 필요
		self.image = image
		self.color = color
		self.rect = image.get_rect(center = position) # 중심위치 설정
		self.radius = 18
		self.row_idx = row_idx
		self.col_idx = col_idx

	def set_rect(self, position):
		self.rect = self.image.get_rect(center = position)

	def draw(self, screen, to_x=None):
		_rect = self.rect
		if to_x: # to_x가 0이어도 해당 조건음 false 임. if 0 은 false
			_rect = (_rect.x + to_x, _rect.y)
		screen.blit(self.image, _rect)

	def set_angle(self, angle):
		self.angle = angle # 새로운 멤버변수 angle
		'''
			발사대 각도에 따라 어느 좌표로 움직일지 계산해야 하는데, 이때 삼각함수를 사용함
			삼각함수를 사용하기 위해는 Math 라이브러리 사용.
			Math 라이브러리 사용을 위해서는 호도법 (1pi. 2pi..) 으로 바꾸어줘야함
			math.radians(90) = 3.141592.../2
			math.radians(180) = 3.141592... = pi
		'''
		self.radi_angle = math.radians(self.angle) # 각도를 호도법으로 변경
	
	def move(self):
		'''
			삼각함수 : 빗변이 r, 각도가 Θ
			x = r * cos Θ
			y = r * sin Θ
			=> 이동할 x, y 좌표 구할 수 있음
			=> r 이 클수록 이동 속도가 빠름
		'''
		to_x = self.radius * math.cos(self.radi_angle)
		# XY 그래프는 원래 위로 갈수록 + 이지만, pygame 에서는 - 이므로 음수화시켜야 위로 이동함
		to_y = self.radius * math.sin(self.radi_angle) * -1 

		# self.rect : 위에서 현재 버블의 rect 를 설정해줌
		self.rect.x += to_x
		self.rect.y += to_y

		# 버블이 벽에 부딪혀서 다시 반대로 튕겨지는 경우 (180-각도 로 각도만 변경해줌)
		if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
			self.set_angle(180 - self.angle)

	# def set_map_index(self, row_idx,col_idx):
	# 	self.row_idx = row_idx
	# 	self.col_idx = col_idx

	def drop_downward(self, height): # height = cell size
		self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery + height))


# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
	def __init__(self, image, position, angle): # 최초값은 90 (90도를 가리킴 ↑)
		super().__init__()
		self.image = image
		self.rect = image.get_rect(center = position)
		self.angle = angle # rotate 에서 사용하기위해 멤버변수 설정
		
		'''
			image 는 각도가 변할때마다 업데이트 되는 이미지이며,
			ori_image 각도변화가 없는 원본 이미지로, 해당 이미지기준으로 각도가 변하는것이다.
			1.5도 변함 => 1.5도 변함 => 원본 이미지에서 3도가 변해야함. 
			원본 이미지 안쓰면, 이미 각도가 변한 이미지에서 추가로 변하는 것이므로 총 4.5도가 변하는 것 
		'''
		self.ori_image = image
		self.position = position

	def draw(self, screen):
		screen.blit(self.image, self.rect) # image 를 rect 정보에 맞추어서 그려줌
		# 빨간색 원을 3의 두께로 position 위치(중심위치)에 그리기 (중심점 test)
		# pygame.draw.circle(screen, (255,0,0), self.position, 3)

	def rotate(self, angle):
		self.angle += angle

		# 각도 최소, 최대값 설정
		if self.angle > 170: 
			self.angle = 170
		elif self.angle < 10:
			self.angle = 10

		# 회전 및 이미지 확대/축소(scale) 메소드 (회전각도 : 시계반대방향이 기본, scale 이 1이면 변화없는것)
		self.image = pygame.transform.rotozoom(self.ori_image, self.angle, 1)
		# 이미지 rect 가 계속 바뀔것이므로, 최초 센터포지션을 중심으로 rect 정보를 고정시켜놓아야함
		self.rect = self.image.get_rect(center = self.position)
