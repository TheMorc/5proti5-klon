import pygame, serial

pygame.init()

ser = serial.Serial('/dev/tty.usbmodem1201', 9600)

font = pygame.font.Font("MyriadBold.ttf", 66)
font2 = pygame.font.Font("Myriad.ttf", 86)
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
  def __init__(self, text1, text2, text3):
    self.text1 = text1
    self.text2 = text2
    self.text3 = text3

q1 = Question("mačka", "pes", "korytmačka")
q2 = Question("lavica", "strom", "dom")
q3 = Question("nighthawk", "purple motion", "realairforce")
q4 = Question("modrá","zelený","hnedo")
q5 = Question("abaddon","ripcord","discord")

questions = [q1, q2, q3, q4, q5]

question_side = 0
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
		if not question_1_shown:
			audio3_channel.play(correct_snd)
			question_1_shown = True
			
	if keys[pygame.K_s]:
		if not question_2_shown:
			audio3_channel.play(correct_snd)
			question_2_shown = True
		
	if keys[pygame.K_d]:
		if not question_3_shown:
			audio3_channel.play(correct_snd)
			question_3_shown = True
			
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
		
	if keys[pygame.K_RETURN]:
		audio_channel.play(question_snd)
		ser.write("0".encode())
		question_reset = True
		question_1_shown = False
		question_2_shown = False
		question_3_shown = False
		question_side = 0
	
	screen.fill(bg_color)
	
	text = font.render("Otázka č.1", True, (255, 255, 255))
	screen.blit(text, (900, 64))
	
	# Draw an image
	screen.blit(spsse_logo, (40, 40))
	
	pygame.display.flip()
	
ser.close()
pygame.quit()

