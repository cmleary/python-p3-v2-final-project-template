import pygame
import os
import random
import button
import time
from helpers import (
    exit_program,
    # helper_1,
    initialize,
    create_player,
    get_all_players,
    get_player_by_id,
    delete_player
 )
from models import Score


def game(player):

    pygame.init()

    clock = pygame.time.Clock()
    fps = 60

    bottom_panel = 150
    screen_width = 800
    screen_height = 400 + bottom_panel

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Work-in-progress')

    current_brawler = 1
    total_brawlers = 3
    cooldown = 0
    action_wait_time = 90
    attack = False
    potion = False
    potion_effect = 18
    clicked = False
    game_over = 0

    font = pygame.font.SysFont('Times New Roman', 26, bold = True, italic = True)

    red = (255, 0, 0)
    green = (0, 255, 0)

    #Graphics set up
    background_img = pygame.image.load('lib/img/Background/background.png').convert_alpha()
    panel_img = pygame.image.load('lib/img/Icons/panel.png').convert_alpha()
    potion_img = pygame.image.load('lib/img/Icons/potion.png').convert_alpha()
    restart_img = pygame.image.load('lib/img/Icons/restart.png').convert_alpha()
    victory_img = pygame.image.load('lib/img/Icons/victory.png').convert_alpha()
    defeat_img = pygame.image.load('lib/img/Icons/defeat.png').convert_alpha()


    #text
    def txt(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw_bg():
        screen.blit(background_img, (0, 0))

    def draw_panel():
        screen.blit(panel_img, (0, screen_height - bottom_panel))
        txt(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
        for count, i in enumerate(DA_list):
            txt(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)

    #bread and butter
    class Brawler():
        def __init__(self, x, y, name, max_hp, attack, potions):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = attack
            self.start_potions = potions
            self.potions = potions
            self.alive = True
            self.animation_list = []
            self.frame_index = 0
            self.animations = 0 #values for animations 
            self.update_time = pygame.time.get_ticks()
            
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'lib/img/{self.name}/Idle/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f'lib/img/{self.name}/Attack/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'lib/img/{self.name}/Hurt/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
            temp_list = []
            for i in range(7):
                img = pygame.image.load(f'lib/img/{self.name}/Death/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.animations][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)


        def update(self):
            animation_cooldown = 100
            self.image = self.animation_list[self.animations][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.animations]):
                if self.animations == 3:
                    self.frame_index = len(self.animation_list[self.animations]) - 1
                else:
                    self.idle()
        
        def idle(self):
            self.animations = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def attack(self, target):
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            target.hurt()
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.death()
            damage_text = Hurt_txt(target.rect.centerx, target.rect.y, str(damage), red)
            damage_text_group.add(damage_text)
            
            self.animations = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def hurt(self):
            self.animations = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def death(self):
            self.animations = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


        def reset (self):
            self.alive = True
            self.potions = self.start_potions
            self.hp = self.max_hp
            self.frame_index = 0
            self.animations = 0
            self.update_time = pygame.time.get_ticks()


        def draw(self):
            screen.blit(self.image, self.rect)



    class HealthBar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp


        def draw(self, hp):
            self.hp = hp
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))



    class Hurt_txt(pygame.sprite.Sprite):
        def __init__(self, x, y, damage, colour):
            pygame.sprite.Sprite.__init__(self)
            self.image = font.render(damage, True, colour)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.counter = 0

        def update(self):
            self.rect.y -= 1
            self.counter += 1
            if self.counter > 30:
                self.kill()


    damage_text_group = pygame.sprite.Group()
    #(posx, posy, name/call, health, attack, healings)
    knight = Brawler(200, 260, 'Knight', 40, 10, 2)
    D_Analyst1 = Brawler(550, 270, 'Data Analyst', 20, 6, 1)
    D_Analyst2 = Brawler(700, 270, 'Data Analyst', 20, 6, 1)

    DA_list = []
    DA_list.append(D_Analyst1)
    DA_list.append(D_Analyst2)

    knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
    DAnalyst1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, D_Analyst1.hp, D_Analyst1.max_hp)
    DAnalyst2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, D_Analyst2.hp, D_Analyst2.max_hp)


    potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
    restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

    run = True
    while run:

        clock.tick(fps)

        draw_bg()

        draw_panel()
        knight_health_bar.draw(knight.hp)
        DAnalyst1_health_bar.draw(D_Analyst1.hp)
        DAnalyst2_health_bar.draw(D_Analyst2.hp)

        knight.update()
        knight.draw()
        for D_analyst in DA_list:
            D_analyst.update()
            D_analyst.draw()

        #draw the damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        attack = False
        potion = False
        target = None
        
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, D_analyst in enumerate(DA_list):
            if D_analyst.rect.collidepoint(pos):
                
                pygame.mouse.set_visible(False)
                
                #screen.blit(sword_img, pos)
                if clicked == True and D_analyst.alive == True:
                    attack = True
                    target = DA_list[count]
        if potion_button.draw():
            potion = True
        #show number of potions remaining
        txt(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)


        if game_over == 0:
            #player action
            if knight.alive == True:
                if current_brawler == 1:
                    cooldown += 1
                    if cooldown >= action_wait_time:
                        #look for player action
                        #attack
                        if attack == True and target != None:
                            knight.attack(target)
                            current_brawler += 1
                            cooldown = 0
                        #potion
                        if potion == True:
                            if knight.potions > 0:
                                #check if the potion would heal the player beyond max health
                                if knight.max_hp - knight.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = knight.max_hp - knight.hp
                                knight.hp += heal_amount
                                knight.potions -= 1
                                damage_text = Hurt_txt(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_brawler += 1
                                cooldown = 0
            else:
                game_over = -1


            #enemy action
            for count, D_analyst in enumerate(DA_list):
                if current_brawler == 2 + count:
                    if D_analyst.alive == True:
                        cooldown += 1
                        if cooldown >= action_wait_time:
                            #check if D_analyst needs to heal first
                            if (D_analyst.hp / D_analyst.max_hp) < 0.5 and D_analyst.potions > 0:
                                #check if the potion would heal the D_analyst beyond max health
                                if D_analyst.max_hp - D_analyst.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = D_analyst.max_hp - D_analyst.hp
                                D_analyst.hp += heal_amount
                                D_analyst.potions -= 1
                                damage_text = Hurt_txt(D_analyst.rect.centerx, D_analyst.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_brawler += 1
                                cooldown = 0
                            #attack
                            else:
                                D_analyst.attack(knight)
                                current_brawler += 1
                                cooldown = 0
                    else:
                        current_brawler += 1

            #if all brawlers have had a turn then reset
            if current_brawler > total_brawlers:
                current_brawler = 1


        #check if all D_analysts are dead
        alive_D_analysts = 0
        for D_analyst in DA_list:
            if D_analyst.alive == True:
                alive_D_analysts += 1
        if alive_D_analysts == 0:
            game_over = 1


        #check if game is over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (250, 50))
                score = knight.hp
                Score.create(player.id, score)
                pygame.time.delay(5000)
                pygame.quit()
            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
            if restart_button.draw():
                knight.reset()
                for D_analyst in DA_list:
                    D_analyst.reset()
                current_brawler = 1
                cooldown
                game_over = 0



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                score = 0
                Score.create(player.id, score)
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()

    pygame.quit()



def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice in ["l", "L"]:
            player = create_player()

            game(player)
        elif choice in ["r", "R"]:
            get_all_players()
        elif choice in ["r1", "R1"]:
            get_player_by_id()
        elif choice in ["d", "D"]:
            delete_player()
        elif choice in ["g", "G"]:
            game()
        else:
            print("Invalid choice")
            keyboard_input = input("* Press any key and then press 'return' to continue *\n")


def menu():
    os.system('clear')
    print("Please select an option:")
    print("L - Record player name and play game for score")
    print("R - Get all player info")
    print("R1 - Get info for 1 player and their score")
    print("D - Delete a player")
    print("0 - Exit the program")



if __name__ == "__main__":
    initialize()
    main()
