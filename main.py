import graphics
import logic

game_run = True

logic.play_game()

while game_run:
    for event in graphics.pygame.event.get():
        if event.type == graphics.pygame.QUIT:
            game_run = False
    
    graphics.pygame.display.flip()
