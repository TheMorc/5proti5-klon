import pygame

pygame.init()

font = pygame.font.Font("Myriad.ttf", 36)
projector_width, projector_height = 1024, 768
screen = pygame.display.set_mode((projector_width, projector_height))
bg_color = (0x18, 0x23, 0x2D)

spsse_logo = pygame.image.load("spsse.png")

audio_channel = pygame.mixer.Channel(0)
correct_snd = pygame.mixer.Sound("correct.mp3")
wrong_snd = pygame.mixer.Sound("wrong.mp3")
prompt_snd = pygame.mixer.Sound("prompt.mp3")
question_snd = pygame.mixer.Sound("question.mp3")
buzzer_snd = pygame.mixer.Sound("buzzer.mp3")

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_a]:
		audio_channel.play(correct_snd)
		
	if keys[pygame.K_b]:
		audio_channel.play(correct_snd)
		
	if keys[pygame.K_c]:
		audio_channel.play(correct_snd)
		
	if keys[pygame.K_x]:
		audio_channel.play(wrong_snd)
		
	if keys[pygame.K_p]:
		audio_channel.play(prompt_snd)
		
	if keys[pygame.K_q]:
		audio_channel.play(question_snd)
	
	screen.fill(bg_color)
	
	text = font.render("Hello, Pygame!", True, (255, 255, 255))
	screen.blit(text, (200, 200, 50, 50))
	
	# Draw an image
	screen.blit(spsse_logo, (300, 300))
	
	pygame.display.flip()

pygame.quit()

