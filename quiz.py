import pygame, serial, math, cv2

pygame.init()
screen = pygame.display.set_mode((1280, 960), pygame.SCALED)
clock = pygame.time.Clock()

ser = serial.Serial('/dev/tty.usbmodem11301', 9600)

font = pygame.font.Font("fonts/Myriad.ttf", 66)
font_b = pygame.font.Font("fonts/MyriadBold.ttf", 66)
font_i = pygame.font.Font("fonts/MyriadItalic.ttf", 66)
font2 = pygame.font.Font("fonts/Myriad.ttf", 86)
font2_b = pygame.font.Font("fonts/MyriadBold.ttf", 86)
blackout_color = (0, 0, 0)

#ďakujem honzai, aj keď dostal som to od teba dosrané :trol:
class AnimatedRectangle:
	def __init__(self, x, y, width, height, text, text2, text3, animation_duration):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.text2 = text2
		self.text3 = text3
		self.animation_duration = animation_duration
		self.start_time = pygame.time.get_ticks()
		self.start_time2 = pygame.time.get_ticks()
		self.text_rendered = False
		self.text_rendered2 = False
		self.tx_alpha = 0
		self.tx_alpha3 = 0
		self.tx_alpha3 = 0

	def ease_in_out_sine(self, t):
		return (1 - math.cos(t * math.pi)) / 2

	def reset(self):
		self.start_time = pygame.time.get_ticks()
		self.text_rendered = False
		self.tx_alpha = 0
		self.text_rendered2 = False
		self.tx_alpha2 = 0
		self.tx_alpha3 = 0
	
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
		
		#answer
		if self.text_rendered:
			text_surface = font2_b.render(self.text, True, (0,0,0))
			txt_surf = text_surface.copy()
			alpha_surf = pygame.Surface(txt_surf.get_size(), pygame.SRCALPHA)
			
			text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y - slide_amount + self.height / 2))
			if not self.tx_alpha >= 255:
				self.tx_alpha = min(self.tx_alpha+8, 255)
				txt_surf = text_surface.copy()
				alpha_surf.fill((255, 255, 255, self.tx_alpha))
				txt_surf.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
			
			screen.blit(txt_surf, text_rect)
			
		#points
		if self.text_rendered and current_time - self.start_time2 > 800:
			text_surface2 = font_i.render(self.text2, True, (0,0,0))
			txt_surf2 = text_surface2.copy()
			alpha_surf2 = pygame.Surface(txt_surf2.get_size(), pygame.SRCALPHA)
			
			text_rect2 = text_surface2.get_rect(center=(self.width - self.x, self.y - slide_amount + self.height / 2))
			if not self.tx_alpha2 >= 255:
				self.tx_alpha2 = min(self.tx_alpha2+8, 255)
				txt_surf2 = text_surface2.copy()
				alpha_surf2.fill((255, 255, 255, self.tx_alpha2))
				txt_surf2.blit(alpha_surf2, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
			
			screen.blit(txt_surf2, text_rect2)
			
		#number
		text_surface3 = font.render(self.text3, True, (0,0,0))
		txt_surf3 = text_surface3.copy()
		alpha_surf3 = pygame.Surface(txt_surf3.get_size(), pygame.SRCALPHA)
		
		text_rect3 = text_surface3.get_rect(center=(self.x, self.y - slide_amount + self.height / 2))
		text_rect3 = (self.x+self.x/2, text_rect3.y)
		if not self.tx_alpha3 >= 255:
			self.tx_alpha3 = min(self.tx_alpha3+8, 255)
			txt_surf3 = text_surface3.copy()
			alpha_surf3.fill((255, 255, 255, self.tx_alpha3))
			txt_surf3.blit(alpha_surf3, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
		
		screen.blit(txt_surf3, text_rect3)


class AnimatedImage:
	def __init__(self, x, y, image, animation_duration, fade_out_start):
		self.x = x
		self.y = y
		self.image = image
		self.animation_duration = animation_duration
		self.fade_out_start = fade_out_start
		self.start_time = pygame.time.get_ticks()
		self.visible = False #used for glows
		
	def cubic_bezier(self, t, p0, p1, p2, p3):
		u = 1 - t
		tt = t * t
		uu = u * u
		uuu = uu * u
		ttt = tt * t
		
		return (
			uuu * p0 +
			3 * uu * t * p1 +
			3 * u * tt * p2 +
			ttt * p3
		)
		
	def update(self):
		global wrong_pressed
		
		current_time = pygame.time.get_ticks()
		time_elapsed = current_time - self.start_time
		
		if time_elapsed >= self.animation_duration:
			time_elapsed = self.animation_duration
		
		p0 = 1.0
		p1 = 2
		p2 = 1
		p3 = 0.0
		
		scale = 1 + self.cubic_bezier(time_elapsed / self.animation_duration, p0, p1, p2, p3) * 0.5
		
		image_width, image_height = self.image.get_size()
		scaled_image = pygame.transform.scale(self.image, (image_width*scale,image_height*scale))
		
		surface = pygame.Surface((scaled_image.get_width(), scaled_image.get_height()), pygame.SRCALPHA)
		surface.blit(scaled_image, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
	
		if self.fade_out_start != 0:
			if current_time - self.start_time > self.fade_out_start:
				fade_out_duration = self.animation_duration - self.fade_out_start
				fade_out_alpha = int(((current_time - self.start_time - self.fade_out_start) / fade_out_duration) * 255)
				if fade_out_alpha > -255:
					surface.set_alpha(255 + fade_out_alpha)
				else:
					surface.set_alpha(0)
					wrong_pressed = False
		else:
			if self.visible:
				surface.set_alpha(255)
			else:
				surface.set_alpha(0)
		
		screen.blit(surface, (self.x - (surface.get_width() - image_width) / 2, self.y - (surface.get_height() - image_height) / 2))
		


spsse_logo = pygame.image.load("images/spsse370.png")

audio_channel = pygame.mixer.Channel(0)
audio2_channel = pygame.mixer.Channel(1)
audio3_channel = pygame.mixer.Channel(2)
wrong_snd = pygame.mixer.Sound("sounds/wrong.mp3")
prompt_correct_snd = pygame.mixer.Sound("sounds/prompt_with_correct.mp3")
prompt_snd = pygame.mixer.Sound("sounds/prompt.mp3")
question_snd = pygame.mixer.Sound("sounds/question.mp3")
buzzer_snd = pygame.mixer.Sound("sounds/buzzer.mp3")
transition_sound = pygame.mixer.Sound("sounds/wrong.mp3")

#otázky
animated_rect = AnimatedRectangle(40, 315, 1200, 110, "N/A", "N/A", "1.", 1000)
animated_rect2 = AnimatedRectangle(40, 470, 1200, 110, "N/A", "N/A", "2.", 1000)
animated_rect3 = AnimatedRectangle(40, 625, 1200, 110, "N/A", "N/A", "3.", 1000)

#wrong answer image
image = pygame.image.load('images/wrong.png')
animated_img = AnimatedImage(1280 / 2 - 192, 960 / 2 - 192, image, 280, 1000)
wrong_pressed = False

#text glows
blue_img = pygame.image.load('images/blue.png')
green_img = pygame.image.load('images/green.png')
blue_glow = AnimatedImage(-15, 700, blue_img, 280, 0)
green_glow = AnimatedImage(835, 700, green_img, 280, 0)

class TransitionVideo:
  def __init__(self, video_path, sound_path, duration):
    self.video_path = video_path
    self.sound_path = sound_path
    self.duration = duration
    self.video = cv2.VideoCapture(self.video_path)
    self.sound = pygame.mixer.Sound(self.sound_path)
    
videos = [TransitionVideo("images/intro.mp4","sounds/5p5_long.mp3", 20000),
		TransitionVideo("images/round_1.mp4","sounds/5p5_short.mp3", 9500),
		TransitionVideo("images/round_2.mp4","sounds/5p5_short.mp3", 9500),
		TransitionVideo("images/round_3.mp4","sounds/5p5_short.mp3", 9500),
		TransitionVideo("images/round_4.mp4","sounds/5p5_short.mp3", 9500),
		TransitionVideo("images/round_5.mp4","sounds/5p5_short.mp3", 9500),
		TransitionVideo("images/bonus.mp4","sounds/1proti1_or_extra_short.mp3", 7000)]

class Question:
  def __init__(self, name, text1, text2, text3, points1, points2, points3):
    self.name = name
    self.text1 = text1
    self.text2 = text2
    self.text3 = text3
    self.points1 = points1
    self.points2 = points2
    self.points3 = points3

questions = [Question("N/A", "N/A", "N/A", "N/A", 0, 0, 0),
			Question("Aká je obľúbená činnosť študenta SPŠSE?", "spánok", "hranie sa na mobile", "jedenie", 45, 32, 22),
			Question("Keď meškáš kvôli doprave tak kam máš ísť?", "domov", "doľava", "na hodinu", 38, 11, 2), 
			Question("Aká je najlepšia výhovorka keď príde študent neskoro do školy?", "meškala doprava", "návšteva lekára", "napadol ma yeti", 41, 23, 3),
			Question("Aké je najobľúbenejšie zvieratko študentov SPŠSE?", "mačka", "pes", "yeti", 45, 21, 3),
			Question("Čo nesmie v škole horieť?", "cigarety", "žiak", "termín na opravu známky", 31, 17, 2),
			Question("Aká trieda má dnes stužkovú?", "IV.A", "IV.B", "vy", 55, 55, 22)] #BONUSová za dvojnásobek

question_current = 0
question_side = 0
blue_points = 0
green_points = 0
blue_points_animated = 0
green_points_animated = 0
question_reset = True
questions_shown = False
question_1_shown = False
question_2_shown = False
question_3_shown = False

#bg
video = cv2.VideoCapture("images/bg.mp4")
success, video_image = video.read()

delay_duration = 0
elapsed_time = 0
transition_playing = False
transition_audio_playing = False
can_continue = False
intro_done = False
blackout = True

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
			audio3_channel.play(prompt_correct_snd)
			question_1_shown = True
			blue_points = blue_points + questions[question_current].points1
			animated_rect.text_rendered = True
			animated_rect.start_time2 = pygame.time.get_ticks()
			
	if keys[pygame.K_s]:
		if not question_2_shown and question_side != 0:
			audio3_channel.play(prompt_correct_snd)
			question_2_shown = True
			blue_points = blue_points + questions[question_current].points2
			animated_rect2.text_rendered = True
			animated_rect2.start_time2 = pygame.time.get_ticks()
		
	if keys[pygame.K_d]:
		if not question_3_shown and question_side != 0:
			audio3_channel.play(prompt_correct_snd)
			question_3_shown = True
			blue_points = blue_points + questions[question_current].points3
			animated_rect3.text_rendered = True
			animated_rect3.start_time2 = pygame.time.get_ticks()
			
	if keys[pygame.K_g]:
		if not question_1_shown and question_side != 0:
			audio3_channel.play(prompt_correct_snd)
			question_1_shown = True
			green_points = green_points + questions[question_current].points1
			animated_rect.text_rendered = True
			animated_rect.start_time2 = pygame.time.get_ticks()
			
	if keys[pygame.K_h]:
		if not question_2_shown and question_side != 0:
			audio3_channel.play(prompt_correct_snd)
			question_2_shown = True
			green_points = green_points + questions[question_current].points2
			animated_rect2.text_rendered = True
			animated_rect2.start_time2 = pygame.time.get_ticks()
		
	if keys[pygame.K_j]:
		if not question_3_shown and question_side != 0:
			audio3_channel.play(prompt_correct_snd)
			question_3_shown = True
			green_points = green_points + questions[question_current].points3
			animated_rect3.text_rendered = True
			animated_rect3.start_time2 = pygame.time.get_ticks()
			
	if keys[pygame.K_c]:
		if not question_1_shown and question_side != 0:
			audio3_channel.play(prompt_snd)
			question_1_shown = True
			animated_rect.text_rendered = True
			animated_rect.start_time2 = pygame.time.get_ticks()
			
	if keys[pygame.K_v]:
		if not question_2_shown and question_side != 0:
			audio3_channel.play(prompt_snd)
			question_2_shown = True
			animated_rect2.text_rendered = True
			animated_rect2.start_time2 = pygame.time.get_ticks()
		
	if keys[pygame.K_b]:
		if not question_3_shown and question_side != 0:
			audio3_channel.play(prompt_snd)
			question_3_shown = True
			animated_rect3.text_rendered = True
			animated_rect3.start_time2 = pygame.time.get_ticks()
			
	if (ser.inWaiting() > 0):
		data_str = ser.read(ser.inWaiting()).decode('ascii') 
		if "1" in data_str and question_reset and question_current != 0:
			audio2_channel.play(buzzer_snd)
			question_side = 1
			question_reset = False
			blue_glow.start_time = pygame.time.get_ticks()
			blue_glow.visible = True
			print("hrajú modri")
		elif "2" in data_str and question_reset and question_current != 0:
			audio2_channel.play(buzzer_snd)
			question_side = 2
			question_reset = False
			green_glow.start_time = pygame.time.get_ticks()
			green_glow.visible = True
			print("hrajú zeleni")
    
	if keys[pygame.K_x] and not wrong_pressed:
		ser.write("3".encode())
		wrong_pressed = True
		audio_channel.play(wrong_snd)
		animated_img.start_time = pygame.time.get_ticks()    
	
	if question_current == 0 or not questions_shown:
		ser.write("0".encode())
		blue_glow.visible = False
		green_glow.visible = False
		
	current_time = pygame.time.get_ticks()
	
	if keys[pygame.K_RETURN] and question_current == 0 and not transition_playing and not intro_done:
			blackout = False
			transition_audio_playing = False
			transition_playing = True
			delay_duration = current_time + videos[0].duration
			elapsed_time = 0
			print("______________________________\nPREHRÁVANÍ INTRO čas:" + str(videos[question_current].duration))
			intro_done = True
			can_continue = True
			question_reset = True
	elif keys[pygame.K_RETURN] and can_continue and not transition_playing:
		ser.write("0".encode())
		question_side = 0
		question_current = question_current + 1
		transition_audio_playing = False
		transition_playing = True
		questions_shown = False
		can_continue = False
		blue_glow.visible = False
		green_glow.visible = False
		delay_duration = current_time + videos[question_current].duration
		elapsed_time = 0
		print("______________________________\nPREHRÁVANÍ PRELÍNAČKA čas:" + str(videos[question_current].duration))
	
	if keys[pygame.K_p] and not questions_shown:
		audio_channel.play(question_snd)
		ser.write("0".encode())
		print(str(question_current)+". kolo | otázka: " + questions[question_current].name)
		print("1.: [modrí A | zelení G | bez bodov C] " + str(questions[question_current].points1) + " bodov\t | " + questions[question_current].text1)
		print("2.: [modrí S | zelení H | bez bodov V] " + str(questions[question_current].points2) + " bodov\t | " + questions[question_current].text2)
		print("3.: [modrí D | zelení J | bez bodov B] " + str(questions[question_current].points3) + " bodov\t | " + questions[question_current].text3)
		question_reset = True
		questions_shown = True
		question_1_shown = False
		question_2_shown = False
		question_3_shown = False
		can_continue = True
		animated_rect.reset()
		animated_rect.text = questions[question_current].text1
		animated_rect.text2 = str(questions[question_current].points1)
		animated_rect2.reset()
		animated_rect2.text = questions[question_current].text2
		animated_rect2.text2 = str(questions[question_current].points2)
		animated_rect3.reset()
		animated_rect3.text = questions[question_current].text3
		animated_rect3.text2 = str(questions[question_current].points3)	
		
	
	if keys[pygame.K_r]:
		ser.write("0".encode())
	
	if elapsed_time < delay_duration and transition_playing:
		elapsed_time = current_time - delay_duration
		
	if elapsed_time >= 0 and transition_playing:
		transition_playing = False
		
	success, video_image = video.read()
	if success:
		video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
		screen.blit(video_surf, (0, 0))
	
	if not success:
		video.set(cv2.CAP_PROP_POS_FRAMES, 1)
		
	if question_current == 0:
		question_num_text = font_b.render("5 proti 5", True, (255, 255, 255))
		screen.blit(question_num_text, (960, 64))
	else:
		question_num_text = font_b.render(str(question_current)+". kolo", True, (255, 255, 255))
		screen.blit(question_num_text, (960, 64))
	
	
	blue_glow.update()
	green_glow.update()
	
	blue_text = font2_b.render("Učitelia", True, (255, 255, 255))
	green_text = font2_b.render("Žiaci", True, (255, 255, 255))
	screen.blit(blue_text, (50, 783))
	screen.blit(green_text, (970, 783))
	
	if blue_points_animated != blue_points:
		blue_points_animated += 1
		
	if green_points_animated != green_points:
		green_points_animated += 1
	
	blue_points_text = font_i.render(str(blue_points_animated)+" bodov", True, (255, 255, 255))
	green_points_text = font_i.render(str(green_points_animated)+" bodov", True, (255, 255, 255))
	blue_text_rect = blue_points_text.get_rect(center=(195,895))
	screen.blit(blue_points_text, blue_text_rect)
	green_text_rect = green_points_text.get_rect(center=(1058,895))
	screen.blit(green_points_text, green_text_rect)
	
	screen.blit(spsse_logo, (40, 40))
	
	if question_current != 0 and questions_shown:
		animated_rect.update()
		animated_rect2.update()
		animated_rect3.update()
	
	animated_img.update()
	
    
	if transition_playing:
		if not transition_audio_playing:
			audio_channel.play(videos[question_current].sound)
			transition_audio_playing = True
			
		transition_success, transition_video_image = videos[question_current].video.read()
		
		if transition_success:
			transition_video_surf = pygame.image.frombuffer(transition_video_image.tobytes(), transition_video_image.shape[1::-1], "BGR")
			if elapsed_time > -1000:
				fade_out_alpha = int((elapsed_time*-255)/1000)
				transition_video_surf.set_alpha(fade_out_alpha)
			screen.blit(transition_video_surf, (0, 0))
		
	if blackout:
		screen.fill(blackout)	
		
	pygame.display.flip()
	clock.tick(60)
	
ser.close()
pygame.quit()