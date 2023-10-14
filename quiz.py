import pygame, serial, math

pygame.init()
clock = pygame.time.Clock()

ser = serial.Serial('/dev/tty.usbmodem1201', 9600)

font = pygame.font.Font("Myriad.ttf", 66)
font_b = pygame.font.Font("MyriadBold.ttf", 66)
font_i = pygame.font.Font("MyriadItalic.ttf", 66)
font2 = pygame.font.Font("Myriad.ttf", 86)
font2_b = pygame.font.Font("MyriadBold.ttf", 86)
projector_width, projector_height = 1280, 960
screen = pygame.display.set_mode((projector_width, projector_height), pygame.SCALED)
bg_color = (0x18, 0x23, 0x2D)

#ďakujem honzai, aj keď dostal som to od teba dosrané :trol:
class AnimatedRectangle:
	def __init__(self, x, y, width, height, text, animation_duration):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.animation_duration = animation_duration
		self.start_time = pygame.time.get_ticks()
		self.text_rendered = False
		self.tx_alpha = 0

	def ease_in_out_sine(self, t):
		return (1 - math.cos(t * math.pi)) / 2

	def reset(self):
		self.start_time = pygame.time.get_ticks()
		self.text_rendered = False
		self.tx_alpha = 0
	
	def update(self):
		current_time = pygame.time.get_ticks()
		time_elapsed = current_time - self.start_time
		
		if time_elapsed >= self.animation_duration:
			time_elapsed = self.animation_duration
		
		alpha = int((time_elapsed / self.animation_duration) * 255)
		
		slide_distance = (1280 - self.width) / 2
		slide_amount = self.ease_in_out_sine(time_elapsed / self.animation_duration) * slide_distance

		surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
		pygame.draw.rect(surface, (67, 224, 234, alpha), (0, 0, self.width, self.height))
		screen.blit(surface, (self.x, self.y - slide_amount))
		
		if self.text_rendered:
			text_surface = font2_b.render(self.text, True, (0,0,0))
			txt_surf = text_surface.copy()
			alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
			
			text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y - slide_amount + self.height / 2))
			if not self.tx_alpha >= 252:
				print(self.tx_alpha)
				self.tx_alpha = max(self.tx_alpha+4, 0)
				txt_surf = text_surface.copy()
				alpha_surf.fill((255, 255, 255, self.tx_alpha))
				txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
			
			screen.blit(txt_surf, text_rect)

spsse_logo = pygame.image.load("spsse370.png")

audio_channel = pygame.mixer.Channel(0)
audio2_channel = pygame.mixer.Channel(1)
audio3_channel = pygame.mixer.Channel(1)
correct_snd = pygame.mixer.Sound("correct.mp3")
wrong_snd = pygame.mixer.Sound("wrong.mp3")
prompt_snd = pygame.mixer.Sound("prompt.mp3")
question_snd = pygame.mixer.Sound("question.mp3")
buzzer_snd = pygame.mixer.Sound("buzzer.mp3")

animated_rect = AnimatedRectangle(40, 315, 1200, 110, "N/A", 1000)
animated_rect2 = AnimatedRectangle(40, 470, 1200, 110, "N/A", 1000)
animated_rect3 = AnimatedRectangle(40, 625, 1200, 110, "N/A", 1000)


class Question:
  def __init__(self, text1, text2, text3, points1, points2, points3):
    self.text1 = text1
    self.text2 = text2
    self.text3 = text3
    self.points1 = points1
    self.points2 = points2
    self.points3 = points3

q1 = Question("mačka", "pes", "korytmačk", 3, 2, 1)
q2 = Question("lavica", "strom", "dom", 15, 10, 5)
q3 = Question("nighthawk", "purple motion", "realairforce", 30, 20, 10)
q4 = Question("modrá","zelený","hnedo", 45, 30, 15)
q5 = Question("abaddon","ripcord","discord", 60, 40, 20)

questions = [q1, q2, q3, q4, q5]

question_current = 0
question_side = 0
blue_points = 0
green_points = 0
question_reset = True
question_1_shown = False
question_2_shown = False
question_3_shown = False

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		pygame.display.toggle_fullscreen()
		
	if keys[pygame.K_a]:
		if not question_1_shown and question_side != 0:
			audio3_channel.play(prompt_snd)
			question_1_shown = True
			if question_side == 1:
				blue_points = blue_points + questions[question_current].points1
			elif question_side == 2:
				green_points = green_points + questions[question_current].points2
			animated_rect.text_rendered = True
			
	if keys[pygame.K_s]:
		if not question_2_shown and question_side != 0:
			audio3_channel.play(prompt_snd)
			question_2_shown = True
			if question_side == 1:
				blue_points = blue_points + questions[question_current].points2
			elif question_side == 2:
				green_points = green_points + questions[question_current].points2
			animated_rect2.text_rendered = True
		
	if keys[pygame.K_d]:
		if not question_3_shown and question_side != 0:
			audio3_channel.play(prompt_snd)
			question_3_shown = True
			if question_side == 1:
				blue_points = blue_points + questions[question_current].points3
			elif question_side == 2:
				green_points = green_points + questions[question_current].points3
			animated_rect3.text_rendered = True
			
	if keys[pygame.K_x]:
		audio_channel.play(wrong_snd)
		
	if (ser.inWaiting() > 0):
		data_str = ser.read(ser.inWaiting()).decode('ascii') 
		if "1" in data_str and question_reset and question_current != 0:
			audio2_channel.play(buzzer_snd)
			question_side = 1
			question_reset = False
			print("modri")
		elif "2" in data_str and question_reset and question_current != 0:
			audio2_channel.play(buzzer_snd)
			question_side = 2
			question_reset = False
			print("zeleni")
        
	if keys[pygame.K_p]:
		audio_channel.play(prompt_snd)
	
	if question_current == 0:
		ser.write("0".encode())
	
	if keys[pygame.K_RETURN] and (question_current == 0 or not question_reset):
		audio_channel.play(question_snd)
		ser.write("0".encode())
		question_reset = True
		question_1_shown = False
		question_2_shown = False
		question_3_shown = False
		animated_rect.reset()
		animated_rect.text = questions[question_current].text1
		animated_rect2.reset()
		animated_rect2.text = questions[question_current].text2
		animated_rect3.reset()
		animated_rect3.text = questions[question_current].text3
		question_side = 0
		question_current = question_current + 1
		
	screen.fill(bg_color)
	
	question_num_text = font_b.render(str(question_current)+". kolo", True, (255, 255, 255))
	screen.blit(question_num_text, (960, 64))
	
	blue_text = font2_b.render("Modrí", True, (255, 255, 255))
	green_text = font2_b.render("Zelení", True, (255, 255, 255))
	screen.blit(blue_text, (80, 783))
	screen.blit(green_text, (940, 783))
	
	blue_points_text = font_i.render(str(blue_points)+" bodov", True, (255, 255, 255))
	green_points_text = font_i.render(str(green_points)+" bodov", True, (255, 255, 255))
	blue_text_rect = blue_points_text.get_rect(center=(195,895))
	screen.blit(blue_points_text, blue_text_rect)
	green_text_rect = green_points_text.get_rect(center=(1058,895))
	screen.blit(green_points_text, green_text_rect)
	
	screen.blit(spsse_logo, (40, 40))
	
	if question_current != 0:
		animated_rect.update()
		animated_rect2.update()
		animated_rect3.update()
	
	pygame.display.flip()
	clock.tick(60)
	
ser.close()
pygame.quit()

