import pygame, serial

pygame.init()

ser = serial.Serial('/dev/tty.usbmodem1201', 9600)

font = pygame.font.Font("Myriad.ttf", 66)
font_b = pygame.font.Font("MyriadBold.ttf", 66)
font_i = pygame.font.Font("MyriadItalic.ttf", 66)
font2 = pygame.font.Font("Myriad.ttf", 86)
font2_b = pygame.font.Font("MyriadBold.ttf", 86)
projector_width, projector_height = 1280, 960
screen = pygame.display.set_mode((projector_width, projector_height), pygame.SCALED)
bg_color = (0x18, 0x23, 0x2D)

spsse_logo = pygame.image.load("spsse370.png")

audio_channel = pygame.mixer.Channel(0)
audio2_channel = pygame.mixer.Channel(1)
audio3_channel = pygame.mixer.Channel(1)
correct_snd = pygame.mixer.Sound("correct.mp3")
wrong_snd = pygame.mixer.Sound("wrong.mp3")
prompt_snd = pygame.mixer.Sound("prompt.mp3")
question_snd = pygame.mixer.Sound("question.mp3")
buzzer_snd = pygame.mixer.Sound("buzzer.mp3")

class Question:
  def __init__(self, text1, text2, text3, points1, points2, points3):
    self.text1 = text1
    self.text2 = text2
    self.text3 = text3
    self.points1 = points1
    self.points2 = points2
    self.points3 = points3

q0 = Question("N/A", "N/A", "N/A", 0, 0, 0)
q1 = Question("mačka", "pes", "korytmačk", 3, 2, 1)
q2 = Question("lavica", "strom", "dom", 15, 10, 5)
q3 = Question("nighthawk", "purple motion", "realairforce", 30, 20, 10)
q4 = Question("modrá","zelený","hnedo", 45, 30, 15)
q5 = Question("abaddon","ripcord","discord", 60, 40, 20)

questions = [q0, q1, q2, q3, q4, q5]

question_current = 1
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
			audio3_channel.play(correct_snd)
			question_1_shown = True
			if question_side == 1:
				blue_points = blue_points + questions[question_current].points1
			elif question_side == 2:
				green_points = green_points + questions[question_current].points2
			
	if keys[pygame.K_s]:
		if not question_2_shown and question_side != 0:
			audio3_channel.play(correct_snd)
			question_2_shown = True
			if question_side == 1:
				blue_points = blue_points + questions[question_current].points2
			elif question_side == 2:
				green_points = green_points + questions[question_current].points2
		
	if keys[pygame.K_d]:
		if not question_3_shown and question_side != 0:
			audio3_channel.play(correct_snd)
			question_3_shown = True
			if question_side == 1:
				blue_points = blue_points + questions[question_current].points3
			elif question_side == 2:
				green_points = green_points + questions[question_current].points3
			
	if keys[pygame.K_x]:
		audio_channel.play(wrong_snd)
		
	if (ser.inWaiting() > 0):
		data_str = ser.read(ser.inWaiting()).decode('ascii') 
		if "1" in data_str and question_reset:
			audio2_channel.play(buzzer_snd)
			question_side = 1
			question_reset = False
			print("modri")
		elif "2" in data_str and question_reset:
			audio2_channel.play(buzzer_snd)
			question_side = 2
			question_reset = False
			print("zeleni")
        
	if keys[pygame.K_p]:
		audio_channel.play(prompt_snd)
		
	if keys[pygame.K_RETURN] and not question_reset:
		audio_channel.play(question_snd)
		ser.write("0".encode())
		question_reset = True
		question_1_shown = False
		question_2_shown = False
		question_3_shown = False
		question_side = 0
		question_current = question_current + 1
	
	screen.fill(bg_color)
	
	question_num_text = font_b.render("Otázka č. "+str(question_current), True, (255, 255, 255))
	screen.blit(question_num_text, (900, 64))
	
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
	
	pygame.display.flip()
	
ser.close()
pygame.quit()

