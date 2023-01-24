import pygame, sys, random, math, time
from pygame.locals import *
import json

pygame.init()

game_state = 0
paused = False
vec = pygame.math.Vector2
FPS = 60
FramePerSec = pygame.time.Clock()


# Menu
press_y = 650
scroll = 0
curtain_y = -1300

# Stats
score = 0
with open("best.txt", "r") as file:
	data = file.read()

	if data is not None:
		data = json.loads(data)
  
		values = data.get("best")

score_max = values
spd = 3
player_pos = vec(0,0)

# Movement
ACC = 1.2
FRIC = -0.10

# Screen Information
WIDTH = 360
HEIGHT = 640

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill((0,255,255))

pygame.display.set_caption("Don't Touch My Presents")

# Load Fonts
total_font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 68)
font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 40)
score_font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 26)
credit_font = pygame.font.Font("data/assets/BaiJamjuree-Bold.ttf", 12)


# Load Music
L = ["data/audio/sleigh_ride.ogg", "data/audio/merry_christmas.ogg", "data/audio/here_comes_santa.ogg"]

# Load Sounds
chop_sfx = ["data/audio/chop.wav", "data/audio/chop_2.wav", "data/audio/chop_3.wav"]
cheer_sfx = ["data/audio/cheer.wav", "data/audio/cheer_2.wav", "data/audio/cheer_3.wav", "data/audio/cheer_4.wav"]
slap_sfx = pygame.mixer.Sound("data/audio/slap.wav")
score_sfx = pygame.mixer.Sound("data/audio/score.wav")

# Load Sprites
bg = pygame.image.load("data/assets/bg.png").convert_alpha()
dotted_line = pygame.image.load("data/assets/dotted_line.png").convert_alpha()
scorebacking = pygame.image.load("data/assets/scoreboard.png").convert_alpha()
santa_hand = pygame.image.load("data/assets/santa_hand.png").convert_alpha()
title = pygame.image.load("data/menu/title.png").convert_alpha()
holding_gift = pygame.image.load("data/menu/holding_gift.png").convert_alpha()
press_key = pygame.image.load("data/menu/press_any_key.png").convert_alpha()
gift = pygame.image.load("data/assets/gift.png").convert_alpha()

pygame.display.set_icon(gift)


def sine(speed, time, how_far, overallY):
	t = pygame.time.get_ticks() / 2 % time
	x = t
	y = math.sin(t/speed) * how_far + overallY 
	y = int(y)
	return y


def background():
	global scroll
	scroll -= .5
	if scroll < -80:
		scroll = 0
	SCREEN.blit(bg,(0,scroll))


def music():
	if not pygame.mixer.music.get_busy():
		filename = random.choice(L)
		pygame.mixer.music.load(filename)
		pygame.mixer.music.play()

def main_menu():
	global press_y

	best_score = score_font.render("Best: " + str(score_max), True, (0, 0, 0))
	best_score_rect = best_score.get_rect(center=(WIDTH//2, 220))
	SCREEN.blit(best_score, best_score_rect)

	y = sine(200.0, 1280, 10.0, 100)
	SCREEN.blit(title, (0, y))
	SCREEN.blit(holding_gift, (0, 320))

	if press_y > 460:
		press_y = press_y * 0.99
  
	press_key_rect = press_key.get_rect(center=(WIDTH//2, 500))
	SCREEN.blit(press_key, press_key_rect)


def scoreboard():
	y = sine(200.0, 1280, 10.0, 40)
	show_score = font.render(str(score), True, (0, 0, 0))
	score_rect = show_score.get_rect(center=(WIDTH//2, y+30))
	SCREEN.blit(scorebacking, (113, y))
	SCREEN.blit(show_score, score_rect)


def game_over():
	global game_state
	game_state = 0
	time.sleep(0.5)


def play_game():
	global game_state
	global score
	global spd
	game_state = 1
	score = 0
	spd = 3


class Hand(pygame.sprite.Sprite):
	def __init__(self, hand_side):
		super().__init__()
		self.new_spd = random.uniform(2.5, 3)
		self.new_y = 0
		self.offset_x = 0
		self.new_x = sine(100.0, 1280, 20.0, self.offset_x)
		self.side = hand_side
		self.can_score = True

		if self.side == 1:
			self.image = pygame.image.load("data/assets/left_hand.png").convert_alpha()
			self.rect = self.image.get_rect()
			self.mask = pygame.mask.from_surface(self.image)
			self.offset_x = random.randint(-50, 120)
			self.new_y = -320
		elif self.side == 0:
			self.image = pygame.image.load("data/assets/right_hand.png").convert_alpha()
			self.rect = self.image.get_rect()
			self.mask = pygame.mask.from_surface(self.image)
			self.offset_x = random.randint(260, 380)
			self.new_y = -40

	def move(self, rand_x, rand_xx):
		self.new_x = sine(100.0, 620, 20.0, self.offset_x)
		self.new_y += self.new_spd
		self.rect.center = (self.new_x, self.new_y)

		if self.rect.top > player_pos.y - 35 and self.can_score:
			global score
			score += 1
			self.can_score = False
			pygame.mixer.Sound.play(score_sfx)
			if score % 5 == 0:
				filename = random.choice(cheer_sfx)
				cheer = pygame.mixer.Sound(filename)
				pygame.mixer.Sound.play(cheer)

		if (self.rect.top > HEIGHT):
			self.rect.bottom = 0
			# Play Kung Fu Sound
			self.new_spd = random.uniform(0.5, 8)
			if self.side == 1:
				self.offset_x = random.randint(-50, 120)
				self.new_y = -320
			elif self.side == 0:
				self.offset_x = random.randint(260, 380)
				self.new_y = -40
			if self.new_spd >= 6:
				self.new_spd = 8
				filename = random.choice(chop_sfx)
				chop = pygame.mixer.Sound(filename)
				pygame.mixer.Sound.play(chop)
			self.can_score = True


	def draw(self, surface):
		# SCREEN.blit(dotted_line, (0, self.rect.y + 53))
		surface.blit(self.image, self.rect)

	def reset(self, side):
			self.new_spd = random.uniform(0.5, 8)
			self.can_score = True
			if self.side == 1:
				self.offset_x = random.randint(-50, 120)
				self.new_y = -320
				self.new_x = 0
			elif self.side == 0:
				self.offset_x = random.randint(260, 380)
				self.new_y = -40
				self.new_x = 0


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("data/assets/gift.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.pos = vec((180,550))
		self.vel = vec(0,0)
		self.acc = vec(0,0)

	def update(self):
		self.acc = vec(0,0)

		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_LEFT]:
			self.acc.x = -ACC
		if pressed_keys[K_RIGHT]:
			self.acc.x = +ACC
		if pressed_keys[K_UP]:
			self.acc.y = -ACC
		if pressed_keys[K_DOWN]:
			self.acc.y = +ACC

		self.acc.x += self.vel.x * FRIC
		self.acc.y += self.vel.y * FRIC
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		global player_pos
		player_pos = self.pos

		if self.pos.x > WIDTH:
			self.pos.x = WIDTH
		if self.pos.x < 0:
			self.pos.x = 0
		if self.pos.y > HEIGHT:
			self.pos.y = HEIGHT
		if self.pos.y < 200:
			self.pos.y = 200
		self.rect.center = self.pos

	def draw(self, surface):
		SCREEN.blit(santa_hand, (self.rect.x - 25, self.rect.y -25))
		surface.blit(self.image, self.rect)

	def reset(self):
		self.pos = vec((180,550))
		self.vel = vec(0,0)
		self.acc = vec(0,0)


# Sprite Setup
P1 = Player()
H1 = Hand(0)
H2 = Hand(1)

#Sprite Groups
hands = pygame.sprite.Group()
hands.add(H1)
hands.add(H2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(H1)
all_sprites.add(H2)


def main():
	global game_state
	global paused
	while game_state != 2:
		# Main Menu
		while game_state == 0:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					play_game()
			background()
			main_menu()
			music()
			pygame.display.update()
			FramePerSec.tick(FPS)

		# Gameplay
		while game_state == 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			if not paused:
				P1.update()
				H1.move(260,380)
				H2.move(-50,100)
			background()
			P1.draw(SCREEN)
			H1.draw(SCREEN)
			H2.draw(SCREEN)
			scoreboard()

			if pygame.sprite.spritecollide(P1, hands, False, pygame.sprite.collide_mask):
				global score_max
				if score > score_max:
					score_max = score
     
					with open("best.txt", "r") as file:
						data = file.read()
					
						if data is not None:
							data = json.loads(data)

							data["best"] = score
							
							with open("best.txt", "w") as file:
								file.write(json.dumps(data))
				
            
				pygame.mixer.Sound.play(slap_sfx)
				time.sleep(0.5)
				P1.reset()
				H1.reset(0)
				H2.reset(1)
				game_over()
			music()
			pygame.display.update()
			FramePerSec.tick(FPS)
main()