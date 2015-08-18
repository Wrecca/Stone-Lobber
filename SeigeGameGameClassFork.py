import pygame, sys
from pygame.locals import *
from math import *
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DKRED = (71, 3, 3)
BROWN = (150, 50, 0)
DKBROWN = (102, 51, 0)
BLUE = (204, 255, 255)
GREY = (160, 160, 160)

class Shell(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 100        
        self.shell_launch_pos = (3, 683)  #was ballPos
        self.launched = False
        self.shell_pos = (3, 683)      #was s
        self.time = 0                  #was t
        self.velocity = (0, 0)         #was v
        
    def Shoot(self, update_t, initial_speed, shell_velocity):
        self.time = self.time + update_t/250.0
        accel = (0.0, 10.0)
        self.velocity =  (shell_velocity[0] + accel[0] * self.time, shell_velocity[1] + accel[1] * self.time)
        s0 = self.shell_launch_pos
        self.shell_pos = (s0[0] + shell_velocity[0] * self.time + accel[0]*self.time * self.time/2, s0[1] + shell_velocity[1] * self.time + accel[1] * self.time * self.time/2)
        self.rect.x = self.shell_pos[0]
        self.rect.y = self.shell_pos[1]
        if self.shell_pos[1] >= 700: # if hit the ground
            self.launched = False

class Eshell(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height, shell_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 100        
        self.shell_launch_pos = shell_pos  #was ballPos
        self.launched = False
        self.shell_pos = shell_pos      #was s
        self.time = 0                  #was t
        self.velocity = (0, 0)         #was v
        self.initial_speed = 100
        
    def Shoot(self, update_t, initial_speed, shell_velocity):
        self.time = self.time + update_t/250.0
        accel = (0.0, 10.0)
        self.velocity =  (shell_velocity[0] + accel[0] * self.time, shell_velocity[1] + accel[1] * self.time)
        s0 = self.shell_launch_pos
        self.shell_pos = (s0[0] + shell_velocity[0] * self.time + accel[0]*self.time * self.time/2, s0[1] + shell_velocity[1] * self.time + accel[1] * self.time * self.time/2)
        self.rect.x = self.shell_pos[0]
        self.rect.y = self.shell_pos[1]
        if self.shell_pos[1] >= 700: # if hit the ground
            self.launched = False

    


class Earth(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x_startPos, y_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_startPos
        self.rect.y = y_pos

    def update(self):
        self.rect.y += 1


class Rock(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        self.rect.y += 5


class Tree(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        self.rect.y += 20


class Fort(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x_pos, y_pos, fort_length):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.top_level = y_pos
        self.height = height
        self.length = fort_length
        self.destroyed_segments = 0
        self.winner = False

    def update(self):
        self.rect.y += 3
               

class Foundation(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self):
        self.rect.y += 3

class Base(pygame.sprite.Sprite):

    def __init__(self, color, width, height, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.destroyed_segments = 0
        self.loser = False

    def update(self):
        self.rect.y += 3




class Game(object):

    def __init__(self):

        self.game_over = False
        self.lost = False

        self.ground_seg_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()
        self.layer_group = pygame.sprite.LayeredUpdates()
        self.fort_hit_list = pygame.sprite.Group()
        self.base_hit_list = pygame.sprite.Group()
        
        ground_surface = 690        
        ground_depth = 0
        fort_build_elev = 0
        place_rock = False
        place_tree_t = False
        place_tree_s = False

        self.base_build_elev = 678
        self.base_hit_points = 0

        fort_x_start = random.randint(900,1600)     ## Creates random #s to build the fort.
        fort_size = random.randint(10,30)
        fort_height = random.randint(30,40)
        
        self.fort_destroyed = fort_size             ## To determine what % of fort to be destroyed before next game.
        self.fort_hit_points = 0
        
        counter = fort_size * 2                     ## More stuff to build the fort.
        found_build = False
        self.fort_build_elev = 0

        self.shell_velocity = 0
        self.shell_initial_speed = 100
        self.shell_angle = 45

        self.enemy_shell_velocity = 0        
        self.enemy_shell_angle = 45                
        self.shell = Shell(BLACK,5,5)
        
        self.enemy_shell = Eshell(BLACK,3,3,(fort_x_start, self.fort_build_elev - fort_height))
        self.layer_group.add(self.enemy_shell)
        self.enemy_shell.shell_pos = (fort_x_start, self.fort_build_elev - fort_height)
        self.enemy_shell_launch_ready = False
        self.enemy_barage_begins = False
        self.wait_for_hit = 0

        self.enemy_dialed_in = False
         

        ## ---------Builds the proceedural background--------------- 

        for x_pos in range(1700):
            
            terr_decider = random.randint(0,2)
            crazy_number = random.randint(0,1)
            size_number = random.randint(0,3)
            tree_maker = random.randint(0,1)
                              
            if terr_decider == 0:
                if crazy_number == 0:
                    ground_surface -= size_number
                    ground_depth += size_number
                elif crazy_number == 1:
                    ground_surface -= size_number
                    ground_depth += size_number
                    place_rock = True
            elif terr_decider == 1:
                ground_surface = ground_surface
                ground_depth = ground_depth
            elif terr_decider == 2:
                if crazy_number == 0:
                    ground_surface += size_number
                    ground_depth -= size_number
                    if tree_maker == 0:
                        place_tree_t = True
                    elif tree_maker == 1:
                        place_tree_s = True                
                elif crazy_number == 1:
                    ground_surface += size_number
                    ground_depth -= size_number
            if ground_surface > 690:
                ground_surface -= size_number
                ground_depth += size_number
                
            if place_rock == True:
                self.rock = Rock(BLACK, 3, 3, x_pos, ground_surface-2)
                self.ground_seg_list.add(self.rock)
                self.all_sprites_list.add(self.rock)
                place_rock = False        
            elif place_tree_t == True:
                self.tree_t = Tree(GREEN, 2, 10, x_pos, ground_surface-10)
                self.ground_seg_list.add(self.tree_t)
                self.all_sprites_list.add(self.tree_t)
                place_tree_t = False
            elif place_tree_s == True:
                self.tree_s = Tree(GREEN, 2, 5, x_pos, ground_surface-5)
                self.ground_seg_list.add(self.tree_s)
                self.all_sprites_list.add(self.tree_s)
                place_tree_s = False

            if found_build == True:
                self.foundation = Foundation(BROWN, 6, 25, x_pos - 3, ground_surface-5)
                self.ground_seg_list.add(self.foundation)
                self.layer_group.add(self.foundation)
                self.layer_group.move_to_front(self.foundation)
                counter -= 1
                if counter < 1:
                    found_build = False

            if fort_x_start == x_pos:
                self.fort_build_elev = ground_surface
                found_build_elev = ground_surface + 30
                found_build = True
                self.enemy_shell.shell_launch_pos = (fort_x_start, self.fort_build_elev - fort_height)
                self.enemy_shell.shell_pos = (fort_x_start, self.fort_build_elev - fort_height)
                

            self.ground_seg = Earth(BROWN, 4, ground_depth, x_pos, ground_surface)
            
            self.ground_seg_list.add(self.ground_seg)
            self.all_sprites_list.add(self.ground_seg)
            self.layer_group.add(self.ground_seg)
            self.layer_group.move_to_front(self.ground_seg)

        ##  This buiulds the fort.
            
        flip_flop = True    

        for fort_cycle in range(fort_size):
            self.fort = Fort(GREY, 2, fort_height + 30, fort_x_start , self.fort_build_elev - fort_height, fort_size)
            self.fort_hit_list.add(self.fort)
            self.layer_group.add(self.fort)
            self.layer_group.move_to_back(self.fort)
            
            fort_cycle += 1
            fort_x_start += 2
            if flip_flop == True:
                self.fort_build_elev += 2
                flip_flop = False
            elif flip_flop == False:
                self.fort_build_elev -= 2
                flip_flop = True

        ##  This buiulds the player's base.

        base_flip_flop = True

        base_x_start = 0

        for base_cycle in range(17):
            self.base = Base(DKBROWN, 2, 20, base_x_start , self.base_build_elev)
            self.base_hit_list.add(self.base)
            self.layer_group.add(self.base)
            self.layer_group.move_to_back(self.base)
            
            base_cycle += 1
            base_x_start += 2
            if flip_flop == True:
                self.base_build_elev += 4
                flip_flop = False
            elif flip_flop == False:
                self.base_build_elev -= 4
                flip_flop = True





    def process_events(self, updated_time):         ## This is the where we process stuff done on the keyboard and 
                                                    ## refresh our Shoot functions.


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over or self.lost:
                    self.__init__()


            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.shell.shell_launch_pos = (3, 683)
                    self.shell.shell_pos = self.shell.shell_launch_pos
                    self.shell.time = 0
                    self.shell.launched = True
                    self.shell_velocity = (self.shell_initial_speed * cos(radians(self.shell_angle)),
                                           - self.shell_initial_speed * sin(radians(self.shell_angle)))
 

        keystate = pygame.key.get_pressed()

        if keystate[K_a]: # rotate conterclockwise
            self.shell_angle += 1
            if self.shell_angle > 90:
                self.shell_angle = 90

        if keystate[K_d]: # rotate clockwise
            self.shell_angle -= 1
            if self.shell_angle < 0:
                self.shell_angle = 0

        if keystate[K_w]: # increase initial speed
            self.shell_initial_speed += 1

        if keystate[K_s]: # decrease initial speed
            self.shell_initial_speed -= 1

        if keystate[K_r]: # restarts the game
            self.game_over = True

        if keystate[K_l]: # TEST shoots an enemy shell
            self.enemy_shell.shell_pos = self.enemy_shell.shell_launch_pos
            self.enemy_shell.time = 0
            self.enemy_shell.launched = True

        if self.enemy_shell.launched:
            self.enemy_shell.Shoot(updated_time, self.enemy_shell.initial_speed, self.enemy_shell_velocity)

        if self.shell.launched:
            self.shell.Shoot(updated_time, self.shell_initial_speed, self.shell_velocity)
                              
        if self.enemy_barage_begins == True:
            self.wait_for_hit += 1
            print(self.wait_for_hit)
            print(self.enemy_shell.initial_speed)

            if self.wait_for_hit > 150:
                print(self.enemy_shell.shell_pos[0])
                if self.enemy_shell.shell_pos[0] > 17:
                    self.enemy_shell.initial_speed += 1
                    self.enemy_shell_velocity = ((self.enemy_shell.initial_speed) * cos(radians(180 - self.enemy_shell_angle)),
                                                - (self.enemy_shell.initial_speed) * sin(radians(180 - self.enemy_shell_angle)))
                    self.enemy_shell.shell_pos = self.enemy_shell.shell_launch_pos
                    self.enemy_shell.time = 0
                    self.enemy_shell.launched = True
                    self.wait_for_hit = 0

                elif self.enemy_shell.shell_pos[0] < 0:
                    self.enemy_shell.initial_speed -= 1
                    self.enemy_shell_velocity = ((self.enemy_shell.initial_speed) * cos(radians(180 - self.enemy_shell_angle)),
                                                - (self.enemy_shell.initial_speed) * sin(radians(180 - self.enemy_shell_angle)))
                    
                    self.enemy_shell.shell_pos = self.enemy_shell.shell_launch_pos
                    self.enemy_shell.time = 0
                    self.enemy_shell.launched = True
                    self.wait_for_hit = 0

                elif self.enemy_shell.shell_pos[0] < 17 and self.enemy_shell.shell_pos[0] > 0:
                    self.enemy_shell.shell_pos = self.enemy_shell.shell_launch_pos
                    self.enemy_shell.time = 0
                    self.enemy_shell.launched = True
                    self.wait_for_hit = 0
                     

 
        return False


    def run_logic(self):                            ## This is where the game decides stuff. The logical brain is here.
                                                    ## The Sprite lists are checked for collisions and it checks for game states.
        if not self.game_over:
           
            shell_hit_list = pygame.sprite.spritecollide(self.shell, self.ground_seg_list, False)   ## This is where all the 
            fort_hit_list = pygame.sprite.spritecollide(self.shell, self.fort_hit_list, False)      ## list checking happens.
            base_hit_list = pygame.sprite.spritecollide(self.enemy_shell, self.base_hit_list, False)
            enemy_shell_hit_list = pygame.sprite.spritecollide(self.enemy_shell, self.ground_seg_list, False)

            for stuff_hit in shell_hit_list:
                stuff_hit.update()
                print(stuff_hit)

            for enemy_stuff_hit in enemy_shell_hit_list:
                enemy_stuff_hit.update()
                print(enemy_stuff_hit)

            for base_hit in base_hit_list:
                base_hit.update()
                print(base_hit)
                self.base_hit_points += 1
                print(self.fort_hit_points)
                if self.base_hit_points > 5:
                    self.lost = True



            for fort_hit in fort_hit_list:          ## This whole chunk below is the fort collision logic.
                fort_hit.update()

                self.fort_hit_points += 1
                print(fort_hit)
                print(self.fort_hit_points)
                print("Fort hit -------------------------------------")
                print(self.enemy_shell.initial_speed)

                if self.fort_hit_points > 3 and self.enemy_dialed_in == False:
                    self.enemy_dialed_in = True
                    
                    self.enemy_shell.initial_speed = self.shell_initial_speed - 12
                    self.enemy_shell_angle = self.shell_angle
                    print(self.enemy_shell.initial_speed)
                    self.enemy_shell_velocity = ((self.enemy_shell.initial_speed) * cos(radians(180 - self.enemy_shell_angle)),
                                                - (self.enemy_shell.initial_speed) * sin(radians(180 - self.enemy_shell_angle)))

                    self.enemy_barage_begins = True


                if self.fort_hit_points > self.fort_destroyed * 3:
                    self.fort.winner = True




                    
                
            if self.fort.winner == True:
                self.game_over = True

            


            



    def display_frame(self, screen):            ## This is where the frames are processed and movement is illusioned
                                                ##  onto the screen. In fact <screen> is passed here so it knows how to process your screen.
        SCREEN_WIDTH = 1700
        SCREEN_HEIGHT = 850

        screen.fill(BLUE)

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("You destroyed the enemy's castle, mouseclick the screen to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if self.lost:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Oh No. The enemy zeroed in on your location and destroyed your siege engines. Click screen to try again.", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])


        self.ground_seg_list.draw(screen)
        self.layer_group.draw(screen)
        pygame.draw.rect(screen,DKRED,(0,690,1700,150))

        if self.shell.shell_pos[1] < 695:
            screen.blit(self.shell.image, self.shell.shell_pos)

        if self.enemy_shell.shell_pos[1] < 695:
            screen.blit(self.enemy_shell.image, self.enemy_shell.shell_pos)


        font = pygame.font.Font(None, 25)    
        text_ang = font.render("ANGLE = %d                             " % self.shell_angle, 1, (10, 10, 10), GREY)
        text_ang_pos = (0, 700)
        text_vm = font.render("INITIAL SPEED = %.1f m/s        " % self.shell_initial_speed, 1, (10, 10, 10), GREY)
        text_vm_pos = (0, 720)
        text_vx = font.render("SHELL VELOCITY X = %.1f m/s     " % self.shell.velocity[0], 1, (10, 10, 10), GREY)
        text_vx_pos = (0, 740)
        text_vy = font.render("SHELL VELOCITY Y = %.1f m/s    " % self.shell.velocity[1], 1, (10, 10, 10), GREY)
        text_vy_pos = (0, 760)
        text_x = font.render("SHELL POSITION X = %.1f m      " % self.shell.shell_pos[0], 1, (10, 10, 10), GREY)
        text_x_pos = (0, 780)
        text_y = font.render("SHELL POSITION Y = %.1f m   " % self.shell.shell_pos[1], 1, (10, 10, 10), GREY)
        text_y_pos = (0, 800)
        text_t = font.render("Time = %.1f s                                " % self.shell.time, 1, (10, 10, 10), GREY)
        text_t_pos = (0, 820)        
        text_instruct = font.render("  PRESS W TO INCREASE VELOCITY /// S TO DECREASE VELOCITY /// PRESS R TO RESTART   ", 1, (10, 10, 10), GREY)
        text_instruct_pos = (600, 760)
        text_instruct2 = font.render("  PRESS A TO INCREASE ANGLE /// D TO DECREASE ANGLE /// CLICK X TO QUIT      ", 1, (10, 10, 10), GREY)
        text_instruct2_pos = (600, 790)


        screen.blit(text_instruct2, text_instruct2_pos)
        screen.blit(text_instruct, text_instruct_pos)
        screen.blit(text_t, text_t_pos)
        screen.blit(text_vx, text_vx_pos)
        screen.blit(text_vy, text_vy_pos)
        screen.blit(text_vm, text_vm_pos)
        screen.blit(text_x, text_x_pos)
        screen.blit(text_y, text_y_pos)
        screen.blit(text_ang, text_ang_pos)


        
        pygame.display.flip()


def main():
    
    pygame.init()

    FPS = 30
    clock = pygame.time.Clock() 
    
    screen_width = 1700
    screen_height = 850

    screen = pygame.display.set_mode([screen_width, screen_height])

    fpsClock = pygame.time.Clock()

    done = False

    game = Game()
 

    while not done:
 
        updated_time = fpsClock.tick(FPS)
        
        done = game.process_events(updated_time)
 
     
        game.run_logic()
 
        game.display_frame(screen)
 
       
        clock.tick(20)
 
  
    pygame.quit()



if __name__ == "__main__":
    main()













