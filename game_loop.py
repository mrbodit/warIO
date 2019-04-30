import pygame


def game_loop(player1, player2, hero1, hero2, player1_moves, player2_moves, replay_string):




    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero1.fire_bullet(hero1.bullets)
                    replay_string[0] = "w"
                if event.key == pygame.K_d:
                    d_pressed = True
                if event.key == pygame.K_a:
                    a_pressed = True
                if event.key == pygame.K_s:
                    hero1.teleport()
                    replay_string[3] = "s"
                if event.key == pygame.K_EQUALS:
                    fps = fps * 2
                if event.key == pygame.K_MINUS:
                    fps = round(fps / 2)
