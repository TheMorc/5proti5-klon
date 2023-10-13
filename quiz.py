import pygame

pygame.init()

font = pygame.font.Font(None, 36)
projector_width, projector_height = 1024, 768
projector_screen = pygame.display.set_mode((projector_width, projector_height))

spsse_logo = pygame.image.load("spsse.png")

correct_snd = pygame.mixer.Sound("correct.wav")
wrong_snd = pygame.mixer.Sound("wrong.wav")
prompt_snd = pygame.mixer.Sound("prompt.wav")
buzzer_snd = pygame.mixer.Sound("buzzer.wav")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
        correct_snd.play()

	#18232D
    projector_screen.fill((255, 255, 255))
    
    pygame.display.flip()

pygame.quit()

