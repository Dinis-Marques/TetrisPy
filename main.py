import pygame, sys
from game import Game
from colors import Colors
import button
import time

pygame.init()

title_font = pygame.font.Font(None, 80)
mid_font = pygame.font.Font(None, 40)
text_font = pygame.font.Font(None, 25)

tetris_text = title_font.render("TETRITHON", True, Colors.white)
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score" , True, Colors.white)
next_surface = title_font.render("Next" , True, Colors.white)
game_over_surface = title_font.render("GAME OVER!", True, Colors.white)
want_to_join = text_font.render("Congratulations, you are able to join the Top 10!", True, Colors.white)
want_to_join_pt2 = text_font.render("Do you want to?", True, Colors.white)
write_user = text_font.render("Please, insert your beautiful username!", True, Colors.white)
warning_user = text_font.render("Your name must only have 3 characters! Example: AAA", True, Colors.white)
game_over_audio = pygame.mixer.Sound("TetrisPy\sounds\game_over.ogg")

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500,620))
pygame.display.set_caption("Tetrithon")

clock = pygame.time.Clock()


GAME_UPDATE = pygame.USEREVENT
speed = 0
hard_drop = False


menu_img = pygame.image.load('TetrisPy\imgs/menu_btn.png').convert_alpha()
start_img = pygame.image.load('TetrisPy\imgs/start_btn.png').convert_alpha()
exit_img = pygame.image.load('TetrisPy\imgs/exit_btn.png').convert_alpha()
easy_img = pygame.image.load('TetrisPy\imgs/easy_btn.png').convert_alpha()
medium_img = pygame.image.load('TetrisPy\imgs/medium_btn.png').convert_alpha()
hard_img = pygame.image.load('TetrisPy\imgs/hard_btn.png').convert_alpha()
restart_img = pygame.image.load('TetrisPy\imgs/restart_btn.png').convert_alpha()
game_over_img = pygame.image.load('TetrisPy\imgs/game_over.png').convert_alpha()
yes_img = pygame.image.load('TetrisPy\imgs/yes_btn.png').convert_alpha()
no_img = pygame.image.load('TetrisPy\imgs/no_btn.png').convert_alpha()
insert_user_img = pygame.image.load('TetrisPy\imgs/insert_user_box.png').convert_alpha()
top10_img = pygame.image.load('TetrisPy\imgs/top10_btn.png').convert_alpha()

sound_img = pygame.image.load('TetrisPy\imgs/sound_btn.png').convert_alpha()
no_sound_img = pygame.image.load('TetrisPy\imgs/nosound_btn.png').convert_alpha()

back_img = pygame.image.load('TetrisPy\imgs/back_btn.png').convert_alpha()

paused_text_img = pygame.image.load('TetrisPy\imgs/game_paused.png').convert_alpha()
resume_img = pygame.image.load('TetrisPy\imgs/resume_btn.png').convert_alpha()

insert_user_img = pygame.transform.scale(insert_user_img, (250, 100))
game_over_img = pygame.transform.scale(game_over_img, (400, 100))  
paused_text_img  = pygame.transform.scale(paused_text_img , (400, 100))  
easy_img = pygame.transform.scale(easy_img, (170, 90)) 
medium_img = pygame.transform.scale(medium_img, (170, 90))  
hard_img = pygame.transform.scale(hard_img, (170, 90))

menu_button = button.Button(149, 205, menu_img, 0.8)
menu_button_top10 = button.Button(149, 460, menu_img, 0.8)
start_button = button.Button(145, 200, start_img, 0.8)
exit_button = button.Button(160, 440, exit_img, 0.8)
exit_button_restart = button.Button(162, 415, exit_img, 0.8)
easy_button = button.Button(30, 320, easy_img, 0.8)
medium_button = button.Button(180, 320, medium_img, 0.8)
hard_button = button.Button(330, 320, hard_img, 0.8)
restart_button = button.Button(149, 310, restart_img, 0.8)
yes_button = button.Button(50, 310, yes_img, 0.8)
no_button = button.Button(270, 310, no_img, 0.8)
top10_btn = button.Button(145, 320, top10_img, 0.8)
sound_btn = button.Button(50, 500, sound_img, 0.8)
nosound_btn = button.Button(50, 500, no_sound_img, 0.8)
resume_btn = button.Button(140, 200, resume_img, 0.8)
restart_button_pause = button.Button(140, 310, restart_img, 0.8)
menu_button_pause = button.Button(140, 420, menu_img, 0.8)
back_button = button.Button(140, 480, back_img, 0.8)

menu_principal = True
game_started = False
choosing_level = False
game_isover = False
can_user_write = False
click_block_time = 0
accepted_user = False
choosing_top10 = False
paused = False
music_playing = False
can_show_top10 = False
game_over_played = False

wrote = False
user_name = ''

sound_state = 'SOUND'
current_mode = None
current_top10 = None
def load_top10(mode):
    top10 = []
    with open(f'TetrisPy\score\{mode}top10.txt', 'r') as file:
        for line in file:
            name, score = line.strip().split(',')

            top10.append((name, int(score)))

    top10.sort(key=lambda x:x[1], reverse=True)

    return top10

def salvar_top10(top10, mode):
    with open(f'TetrisPy\score\{mode}top10.txt', 'w') as file:
        for name, score in top10:
            file.write(f"{name},{score}\n")
game = Game()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and can_user_write == True:
            if event.key == pygame.K_BACKSPACE:
                user_name = user_name[:-1]
            elif event.key == pygame.K_RETURN:
                can_user_write = False
                if wrote == False and user_name != '':
                    top10 = load_top10(current_mode)
                    top10.append((user_name.upper(), game.score))
                    top10.sort(key=lambda x: x[1], reverse=True)
                    top10 = top10[:10]
                    salvar_top10(top10, current_mode)
                    wrote = True
                    accepted_user = False
                    user_name = ''
            else:
                if len(user_name) < 3 and event.unicode != ' ':
                    user_name += event.unicode
        if event.type == pygame.KEYDOWN and menu_principal == False and game_started == True:
            if event.key == pygame.K_p and game.game_over == False:
                if paused == True:
                    paused = False
                elif paused == False:
                    paused = True


            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
            if event.key == pygame.K_SPACE and game.game_over == False:
                game.hard_drop()
        if event.type == GAME_UPDATE and game.game_over == False and menu_principal == False and paused == False:
            game.move_down() 
    if game.game_over == True:
        if game_over_played == False:
            game_over_audio.play()
            game_over_played = True
        if wrote == False:
            top10 = load_top10(current_mode)
            if len(top10) < 10 or game.score > top10[-1][1]:
                can_user_write = True  
            else:
                clicked_no = True
                can_user_write = False
                wrote = True
        screen.fill((Colors.dark_blue))
        

        if can_user_write == True and accepted_user == False:
            screen.blit(want_to_join, (50, 100))
            screen.blit(want_to_join_pt2, (190, 140))
            score_value = title_font.render(f'Score: {str(game.score)}', True, Colors.white)
            screen.blit(score_value, (200, 180))
            if yes_button.draw(screen):
                allow_typing = True
                accepted_user = True
                screen.fill((Colors.dark_blue))
            if no_button.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
                can_user_write = False
                wrote = True
                click_block_time = pygame.time.get_ticks()
                pygame.event.clear()
        elif accepted_user == True:
            screen.fill((Colors.dark_blue))
            screen.blit(write_user, (100, 100))
            screen.blit(warning_user, (30, 140))
            screen.blit(insert_user_img, ((140, 240)))
            name_surface = title_font.render(user_name.upper(), True, Colors.white)
            screen.blit(name_surface, (236, 295))
        elif wrote == True:
            screen.fill(Colors.dark_blue)
            screen.blit(game_over_img, (55, 80))
            score_value = title_font.render(str(game.score), True, Colors.white)
            screen.blit(score_value, (250, 40))
            if menu_button.draw(screen):
                pygame.mixer.music.stop()                         
                pygame.mixer.music.load(f"TetrisPy\sounds\musica.ogg")
                pygame.mixer.music.play(-1) 
                pygame.time.set_timer(GAME_UPDATE, 0)
                menu_principal = True
                choosing_level = False
                game.game_over = False
                wrote = False
                music_reset = False
                game_over_played = False
            if restart_button.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
                pygame.mixer.music.stop()                         
                pygame.mixer.music.load(f"TetrisPy\sounds\{current_mode}_song.ogg")
                pygame.mixer.music.play(-1) 
                game = Game()
                pygame.time.set_timer(GAME_UPDATE, speed)
                menu_principal = False
                game_over_played = False
                game.game_over = False
                choosing_level = False
                wrote = False
                music_reset = False
                click_block_time = pygame.time.get_ticks()
            if exit_button_restart.draw(screen):
                run = False
    elif game.game_over == True and music_reset == False:
        game.set_na_music()
        music_reset = True
    elif paused:
        screen.fill(Colors.dark_blue)
        screen.blit(paused_text_img, (60, 40))
        score_value = mid_font.render(f'Current Score: {str(game.score)}', True, Colors.white)
        screen.blit(score_value, (145, 140))
        if resume_btn.draw(screen):
            paused = False
        if sound_state == 'SOUND':
            if sound_btn.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
                game.set_vol(0)
                game.rotate_sound.set_volume(0)
                sound_state = 'NOSOUND'
                click_block_time = pygame.time.get_ticks()
        if sound_state == 'NOSOUND':
            if nosound_btn.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
                game.set_vol(1)
                sound_state = 'SOUND'
                click_block_time = pygame.time.get_ticks()
        if restart_button_pause.draw(screen):
            pygame.mixer.music.stop()                         
            pygame.mixer.music.load(f"TetrisPy\sounds\{current_mode}_song.ogg")
            pygame.mixer.music.play(-1) 
            game = Game()
            paused = False
            game_started = True
            menu_principal = False
            choosing_level = False
            game.game_over = False
            wrote = False
            user_name = ''
            music_reset = False
            accepted_user = False
            can_user_write = False
            pygame.time.set_timer(GAME_UPDATE, speed)
            click_block_time = pygame.time.get_ticks()
        if menu_button_pause.draw(screen):
            pygame.mixer.music.stop()                         
            pygame.mixer.music.load("TetrisPy\sounds\musica.ogg")
            pygame.mixer.music.play(-1) 
            game = Game()
            paused = False
            music_reset = False
            game_started = False
            menu_principal = True
            choosing_level = False
            game.game_over = False
            wrote = False
            user_name = ''
            accepted_user = False
            can_user_write = False
            pygame.time.set_timer(GAME_UPDATE, speed)
            click_block_time = pygame.time.get_ticks()
    elif menu_principal:
        if music_playing == False:
            pygame.mixer.music.stop()                         
            pygame.mixer.music.load("TetrisPy\sounds\musica.ogg")
            pygame.mixer.music.play(-1) 
            music_playing = True
        screen.fill((Colors.dark_blue))
        screen.blit(tetris_text, (85, 100))
        if start_button.draw(screen):
            choosing_level = True
            menu_principal = False 
        if top10_btn.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
            choosing_top10 = True
            menu_principal = False
            click_block_time = pygame.time.get_ticks()
        if sound_state == 'SOUND':
            if sound_btn.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
                game.set_vol(0)
                game.rotate_sound.set_volume(0)
                sound_state = 'NOSOUND'
                click_block_time = pygame.time.get_ticks()
        if sound_state == 'NOSOUND':
            if nosound_btn.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
                game.set_vol(1)
                sound_state = 'SOUND'
                click_block_time = pygame.time.get_ticks()
        if exit_button.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
            click_block_time = pygame.time.get_ticks()
            run = False 
    elif choosing_level == True:
        screen.fill(Colors.dark_blue)
        choose_surface = title_font.render("Choose The Level!", True, Colors.white)
        screen.blit(choose_surface, (125, 130))
        if easy_button.draw(screen):
            print("EASY mode selected")            
            current_mode = 'easy'
            pygame.mixer.music.stop()                         
            pygame.mixer.music.load(f"TetrisPy\sounds\{current_mode}_song.ogg")
            pygame.mixer.music.play(-1) 
            speed = 250
            game = Game()
            pygame.time.set_timer(GAME_UPDATE, speed)
            game_started = True
            game_over_played = False
            choosing_level = False
        if medium_button.draw(screen):
            print("MEDIUM mode selected")
            current_mode = 'medium'
            pygame.mixer.music.stop()                         
            pygame.mixer.music.load(f"TetrisPy\sounds\{current_mode}_song.ogg")
            pygame.mixer.music.play(-1) 
            speed = 175
            game = Game()
            pygame.time.set_timer(GAME_UPDATE, speed)
            game_started = True
            game_over_played = False
            choosing_level = False
        if hard_button.draw(screen):
            print("HARD mode selected")
            current_mode = 'hard'
            pygame.mixer.music.stop()                         
            pygame.mixer.music.load(f"TetrisPy\sounds\{current_mode}_song.ogg")
            pygame.mixer.music.play(-1) 
            speed = 130
            game = Game()
            pygame.time.set_timer(GAME_UPDATE, speed)
            game_started = True
            game_over_played = False
            choosing_level = False
        
            
    elif choosing_top10 == True:
        screen.fill(Colors.dark_blue)
        screen.blit(title_font.render("TOP 10", True, Colors.white), (205, 50))
        screen.blit(text_font.render("Please, select one of the 3 modes!", True, Colors.white), (120, 100))
        if easy_button.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
            current_top10 = 'easy'
            choosing_top10 = False
            can_show_top10 = True
            click_block_time = pygame.time.get_ticks()
        if medium_button.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
            current_top10 = 'medium'
            choosing_top10 = False
            can_show_top10 = True
            click_block_time = pygame.time.get_ticks()
        if hard_button.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
            current_top10 = 'hard'
            choosing_top10 = False
            can_show_top10 = True
            click_block_time = pygame.time.get_ticks()
        if back_button.draw(screen) and pygame.time.get_ticks() - click_block_time > 300:
            current_top10 = None
            choosing_top10 = False
            menu_principal = True
            click_block_time = pygame.time.get_ticks()
    elif can_show_top10 == True:
        screen.fill(Colors.dark_blue)
        screen.blit(title_font.render(f'TOP 10 - {current_top10.capitalize()}', True, Colors.white), (157, 50))

        top10 = load_top10(current_top10)
        y_offset = 120
        for i, (name, score) in enumerate(top10):
            names = text_font.render(f"{i + 1}. {name} - {score}", True, Colors.white)
            screen.blit(names, (210, y_offset))
            y_offset += 35
        if back_button.draw(screen):
            can_show_top10 = False
            choosing_top10 = True
    elif game_started == True:
        if sound_state == 'NOSOUND':
            game.set_vol(0)
        score_value = title_font.render(str(game.score), True, Colors.white)
        screen.fill(Colors.dark_blue)       
        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (375, 180, 50, 50))
        if game.game_over == True:
            screen.blit(game_over_surface, (320, 450, 50, 50))
        
        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value, score_value.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))

        
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)
    pygame.display.update()
    clock.tick(60)
pygame.quit()