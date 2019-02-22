#
# its been 2 days and i've just gotten mouse location 
# tracking and rotating sprites. its slow working. 
# also bullets move today!
#
# day three, bullets are fully functional and guns work.
# performance is kinda bad though. cleaned up the code.
#
# day four, enemy class works and added another weapon.
# also fixed some issues with rolling.
# there are still a lot of vestigal variables that do
# not actually do anything.

import pygame, glob, sys
from pygame import *
import math
from math import *
import numpy
import random

######################################################################
######################################################################
#####CLASS AND DEFS GO HERE###########################################
######################################################################
######################################################################

object_list = [] # everything is put here so it can be drawn

# somehow sort objects by their x,y coords and render them
# from top to bottom, left to right so that lower objects
# get rendered on top. would help give the game a sense of
# depth. not sure how to do the floor yet other than with
# multiple layers

class mutant(pygame.sprite.Sprite):

    def __init__(self,x,y,health,wep_a,anim_speed,spr_idle,spr_walk):

        object_list.append(self)

        self.angle = 0
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.spritetick = 0
        self.spriteindex = 1
        self.spr_idle = spr_idle
        self.spr_walk = spr_walk
        self.health = health
        #temporary default values???
        self.level = 0
        self.sprite = 'dot_idle_0.png'
        self.state = 0
        self.super_state = 0 #super state is for active animations
        self.spr_idle_tick = 1
        #self.spr_idle_ticks = len(self.spr_idle) * 10
        self.spr_walk_tick = 1
        #self.spr_walk_ticks = len(self.spr_walk) * 10
        self.anim_speed = anim_speed
        self.wep_a = wep_a
        self.tick_passive = 0 #used for sprite index during passive animations
        self.tick_active = 0 #used for sprite index during active animations
        self.active_countdown = 0 #set to length of animation, when 0 active ends
        self.can_shoot = 1 #this determines if the player is allowed to shoot
        self.tick = 0
        self.active = 0 #this is 1 during active animations
        self.ammo_bullets = 100
        self.ammo_shells = 50
        self.ammo_bombs = 50
        self.ammo_laser = 50
        self.ammo_bolts = 50
        self.mouseup = True
        self.reload_time = 0
        self.fired = 0
        self.speed = 3
        #sepcial states can be for running a full animation just once

    def update_pos(self):

        keys = pygame.key.get_pressed() 

        if (keys[K_RIGHT]):
            self.x = self.x + self.speed #fix all this to use velocity def to clean up code

        if (keys[K_LEFT]):
            self.x = self.x - self.speed #it would have to keep the velo no lower than player.speed

        if (keys[K_DOWN]):
            self.y = self.y + self.speed

        if (keys[K_UP]):
            self.y = self.y - self.speed

        # velocity adjustments, first implemented for fish roll, later recoil
        update_velo(self) # this now works for all non angular motion


    def update_looks(self):

        keys = pygame.key.get_pressed()

        #idle code
        if not (keys[K_RIGHT])and not(keys[K_LEFT])and not(keys[K_DOWN])and not(keys[K_UP]):
            self.state = 0
            if self.active == 0:
                draw_passive(self,self.spr_idle)

        #walking code #sets state to 1 (walking) while buttons pressed
        if (keys[K_RIGHT]) or (keys[K_LEFT]) or (keys[K_DOWN]) or (keys[K_UP]):
            self.state = 1
            if self.active == 0:
                draw_passive(self,self.spr_walk)

        #draw the wep_a at same loc as the player
        self.wep_a.x = self.x + 0
        self.wep_a.y = self.y + 0
        self.wep_b.x = self.x + 0
        self.wep_b.y = self.y + 0

        mouse_spot = (the_mouse.x,the_mouse.y)
        self.looking = 0 - math.degrees(math.atan2((the_mouse.y - (self.wep_a.y + 0)),(the_mouse.x - (self.wep_a.x - 0))))
        self.wep_a.angle = self.looking 

    def update(self): 
  
        if (pygame.mouse.get_pressed()[2]) == True:
            self.ability()

        self.update_pos()
        self.update_looks()
        #self.shoot_check()
        shoot_check(self)


        self.step() # step is to be run after all non draws and before all draws cause i say so

        drawObj(self)
        drawObj(self.wep_a) #putting this second causes it to be drawn on top

######################################################################
######################################################################

class mut_dot(mutant): #dot is an example character used to show how to make characters

    def __init__(self,x,y):
        
        self.x = x
        self.y = y
        self.health = 8
        self.anim_speed = 5 #5 is the default animation speed. 
                            #less is faster, more is slower
        self.spr_idle = ['dot_idle_0.png','dot_idle_1.png']
        self.spr_walk = ['dot_walk_0.png','dot_walk_1.png']
        self.wep_a = wep_minigun(self) #weapons must always have an owner
        self.wep_b = wep_fists(self)
        
        mutant.__init__(self,self.x,self.y,self.health,self.wep_a,self.anim_speed,self.spr_idle,self.spr_walk)

    def ability():  #bullets that hit enemies get stored in them, 
                    #on death, they all fly out randomly
        var = 0     #program it all LATER

    def step():

        var = 0

######################################################################

class mut_fish(mutant): #fish is a real character

    def __init__(self,x,y):
        
        self.x = x
        self.y = y
        self.health = 8
        self.anim_speed = 5 
        self.spr_idle = ['fish_idle_0.png','fish_idle_1.png']
        self.spr_walk = ['fish_walk_0.png','fish_walk_1.png']
        self.wep_a = wep_rifle(self) 
        self.wep_b = wep_fists(self)
        self.rollframes = 30
        self.rolling = 0
        self.rolltime = 0
        
        mutant.__init__(self,self.x,self.y,self.health,self.wep_a,self.anim_speed,self.spr_idle,self.spr_walk)

    def ability(self): 

        keys = pygame.key.get_pressed() 
        if (self.rolling == 0) and (self.rolltime == 0): 

            if (keys[K_RIGHT]) and ((pygame.mouse.get_pressed()[2]) == True):
                self.vx = self.vx + 10

            if (keys[K_LEFT]) and ((pygame.mouse.get_pressed()[2]) == True):
                self.vx = self.vx - 10

            if (keys[K_DOWN]) and ((pygame.mouse.get_pressed()[2]) == True):
                self.vy = self.vy + 10

            if (keys[K_UP]) and ((pygame.mouse.get_pressed()[2]) == True):
                self.vy = self.vy - 10

            self.rolling = 1
            self.rolltime = 15

    def step(self):

        if self.rolltime > 0:
            
            self.rolling = 0
            self.rolltime = self.rolltime - 1
            self.angle + 15
            print(self.rolltime)

######################################################################
######################################################################

class enemy(pygame.sprite.Sprite):

    def __init__(self,x,y,health,wep_a,anim_speed,spr_idle,spr_walk):

        object_list.append(self)

        self.angle = 0
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.spritetick = 0
        self.spriteindex = 1
        self.spr_idle = spr_idle
        self.spr_walk = spr_walk
        self.health = health
        #temporary default values???
        self.level = 0
        self.sprite = 'dot_idle_0.png'
        self.state = 0
        self.super_state = 0 #super state is for active animations
        self.spr_idle_tick = 1
        self.spr_idle_ticks = len(self.spr_idle) * 10
        self.spr_walk_tick = 1
        self.spr_walk_ticks = len(self.spr_walk) * 10
        self.anim_speed = anim_speed
        self.wep_a = wep_a # enemies only get one weapon... maybe
        self.tick_passive = 0 #used for sprite index during passive animations
        self.tick_active = 0 #used for sprite index during active animations
        self.active_countdown = 0 #set to length of animation, when 0 active ends
        self.can_shoot = 1 #this determines if the enemy is allowed to shoot
        self.tick = 0
        self.active = 0 #this is 1 during active animations
        self.ammo_bullets = 100
        self.ammo_shells = 50
        self.ammo_bombs = 50
        self.ammo_laser = 50
        self.ammo_bolts = 50
        self.mouseup = True
        self.reload_time = 0
        self.fired = 0
        #sepcial states can be for running a full animation just once

    def update_pos(self):

        update_velo(self)

    def update_looks(self):

        keys = pygame.key.get_pressed()

        #idle code
        #if not (keys[K_RIGHT])and not(keys[K_LEFT])and not(keys[K_DOWN])and not(keys[K_UP]):
        if self.state == 0:
            if self.active == 0:
                draw_passive(self,self.spr_idle)

        #walking code #sets state to 1 (walking) while buttons pressed
        #if (keys[K_RIGHT]) or (keys[K_LEFT]) or (keys[K_DOWN]) or (keys[K_UP]):
        if self.state == 1:
            if self.active == 0:
                draw_passive(self,self.spr_walk)

        #draw the wep_a at same loc as the player
        self.wep_a.x = self.x + 0
        self.wep_a.y = self.y + 0
        self.wep_b.x = self.x + 0
        self.wep_b.y = self.y + 0

        mouse_spot = (the_mouse.x,the_mouse.y)
        self.looking = 0 #- math.degrees(math.atan2((the_mouse.y - (self.wep_a.y + 0)),(the_mouse.x - (self.wep_a.x - 0))))
        self.wep_a.angle = self.looking 

    def update(self): 

        self.update_pos()
        self.update_looks()
        #shoot_check(self)

        self.step() # step is to be run after all non draws and before all draws cause i say so

        drawObj(self)
        drawObj(self.wep_a) #putting this second causes it to be drawn on top

######################################################################
######################################################################

# more enemy stuff will go here

class nme_bandit(enemy):

    def __init__(self,xin,yin):
        
        self.x = xin
        self.y = yin
        self.health = 8
        self.anim_speed = 5 
        self.spr_idle = ['nme_bandit_idle_0.png','nme_bandit_idle_1.png']
        self.spr_walk = ['nme_bandit_walk_0.png','nme_bandit_walk_1.png']
        self.wep_a = wep_flakgun(self) 
        self.wep_b = wep_fists(self)
        self.rollframes = 30
        self.rolling = 0
        self.rolltime = 0
        
        enemy.__init__(self,self.x,self.y,self.health,self.wep_a,self.anim_speed,self.spr_idle,self.spr_walk)

    def step(self):

        var = 1

######################################################################
######################################################################

#held weapons
class weapon(pygame.sprite.Sprite):

    def __init__(self,x,y,ammo_type,ammo_cost,reload_time,owner):

        self.x = x
        self.y = y
        self.angle = 0 #this can stay
        self.cooldown = 0

    def update(self):
        var = 0 # this is equivalent to 'do nothing'

######################################################################
######################################################################

class wep_fists(weapon):

    def __init__(self,owner):
        self.owner = owner # owner doesn't do anything but might be needed later for team checking
        self.sprite = 'wep_fists.png' # sprite for the weapon while being held
        self.ammo_type = 1 # 1 is bullet, 2 is shell, 3 is explode, 4 is bolt, 5 is laser
        self.ammo_cost = 0
        self.reload_time = 0 # this is how many frames the reload takes
        self.x = 0 # these both gotta be any number. 0 works
        self.y = 0
        weapon.__init__(self,self.x,self.y,self.ammo_type,self.ammo_cost,self.reload_time,self.owner)

    def fire(self):
        var = 0 # the fists are actually just empty hands. you cant do anything with them

######################################################################

class wep_rifle(weapon):

    def __init__(self,owner):

        self.owner = owner
        self.sprite = 'wep_rifle.png'
        self.ammo_type = 1
        self.ammo_cost = 1
        self.reload_time = 15
        self.x = 0
        self.y = 0
        self.auto = 0
        weapon.__init__(self,self.x,self.y,self.ammo_type,self.ammo_cost,self.reload_time,self.owner)

    def fire(self): # in here is the fun part. define what happens when the gun fires :)

        xin = self.x
        yin = self.y
        ain = self.angle

        self.cooldown = self.reload_time
        random_1 = random.randrange(-7,7) # the bigger the difference the larger the spread.
        bullet_shot_1 = proj_nme_bullet_1(xin,yin, 0 - ain + random_1)

######################################################################

class wep_shotgun(weapon):

    def __init__(self,owner):

        self.owner = owner
        self.sprite = 'wep_shotgun.png'
        self.ammo_type = 2
        self.ammo_cost = 1
        self.reload_time = 30
        self.x = 0
        self.y = 0
        self.auto = 0
        weapon.__init__(self,self.x,self.y,self.ammo_type,self.ammo_cost,self.reload_time,self.owner)

    def fire(self): # in here is the fun part. define what happens when the gun fires :)

        xin = self.x
        yin = self.y
        ain = self.angle

        self.cooldown = self.reload_time
        random_0 = random.randrange(5,10)
        random_1 = random.randrange(-5,5)
        random_2 = random.randrange(-10,-5)
        bullet_shot_0 = proj_shell_1(xin,yin, 0 - ain + random_0)
        bullet_shot_1 = proj_shell_1(xin,yin, 0 - ain + random_1)
        bullet_shot_2 = proj_shell_1(xin,yin, 0 - ain + random_2) # for some reason the angle needs to be negative???

######################################################################

class wep_flakgun(weapon):

    def __init__(self,owner):

        self.owner = owner
        self.sprite = 'wep_flakgun.png'
        self.ammo_type = 2
        self.ammo_cost = 4
        self.reload_time = 45
        self.x = 0
        self.y = 0
        self.auto = 0
        weapon.__init__(self,self.x,self.y,self.ammo_type,self.ammo_cost,self.reload_time,self.owner)

    def fire(self): # in here is the fun part. define what happens when the gun fires :)

        xin = self.x
        yin = self.y
        ain = self.angle

        self.cooldown = self.reload_time
        random_2 = random.randrange(-3,3)

        bullet_shot_2 = proj_flak_1(xin,yin, 0 - ain + random_2) # for some reason the angle needs to be negative???

######################################################################

class wep_minigun(weapon):

    def __init__(self,owner):

        self.owner = owner
        self.sprite = 'wep_minigun.png'
        self.ammo_type = 1
        self.ammo_cost = 1
        self.reload_time = 1
        self.x = 0
        self.y = 0
        self.auto = 1
        weapon.__init__(self,self.x,self.y,self.ammo_type,self.ammo_cost,self.reload_time,self.owner)

    def fire(self): # in here is the fun part. define what happens when the gun fires :)

        xin = self.x
        yin = self.y
        ain = self.angle

        self.cooldown = self.reload_time
        random_0 = random.randrange(-5,10)
        random_1 = random.randrange(-5,5)
        random_2 = random.randrange(-10,-5)
        #bullet_shot_0 = proj_shell_1(xin,yin, 0 - ain + random_0)
        bullet_shot_1 = proj_bullet_1(xin,yin, 0 - ain + random_1)
        #bullet_shot_2 = proj_shell_1(xin,yin, 0 - ain + random_2) # for some reason the angle needs to be negative???

######################################################################

class wep_double_minigun(weapon):

    def __init__(self,owner):

        self.owner = owner
        self.sprite = 'wep_minigun.png'
        self.ammo_type = 1
        self.ammo_cost = 2
        self.reload_time = 1
        self.x = 0
        self.y = 0
        self.auto = 1
        weapon.__init__(self,self.x,self.y,self.ammo_type,self.ammo_cost,self.reload_time,self.owner)

    def fire(self): # in here is the fun part. define what happens when the gun fires :)

        xin = self.x
        yin = self.y
        ain = self.angle
        
        self.cooldown = self.reload_time
        random_0 = random.randrange(0,5)
        random_1 = random.randrange(-5,5)
        random_2 = random.randrange(-5,0)
        bullet_shot_0 = proj_bullet_1(xin,yin, 0 - ain + random_0)
        #bullet_shot_1 = proj_bullet_1(xin,yin, 0 - ain + random_1)
        bullet_shot_2 = proj_bullet_1(xin,yin, 0 - ain + random_2) # for some reason the angle needs to be negative???

######################################################################

class wep_triple_minigun(weapon):

    def __init__(self,owner):

        self.owner = owner
        self.sprite = 'wep_minigun.png'
        self.ammo_type = 1
        self.ammo_cost = 3
        self.reload_time = 1
        self.x = 0
        self.y = 0
        self.auto = 1
        weapon.__init__(self,self.x,self.y,self.ammo_type,self.ammo_cost,self.reload_time,self.owner)

    def fire(self): # in here is the fun part. define what happens when the gun fires :)

        xin = self.x
        yin = self.y
        ain = self.angle

        self.cooldown = self.reload_time
        random_0 = random.randrange(5,10)
        random_1 = random.randrange(-3,3)
        random_2 = random.randrange(-10,-5)
        bullet_shot_0 = proj_bullet_1(xin,yin, 0 - ain + random_0)
        bullet_shot_1 = proj_bullet_1(xin,yin, 0 - ain + random_1)
        bullet_shot_2 = proj_bullet_1(xin,yin, 0 - ain + random_2) # for some reason the angle needs to be negative???


######################################################################
######################################################################

class projectile(pygame.sprite.Sprite):

    def __init__(self,x,y,team,speed,angle,spr_fly,spr_hit):

        object_list.append(self)
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.team = team
        self.speed = speed
        self.angle = angle
        self.spr_fly = spr_fly
        self.spr_hit = spr_hit
        self.sprite = spr_fly
        self.collision = 0

    def update(self):

        self.life = self.life - 1

        if self.collision == 0:
            self.sprite = self.spr_fly

        if self.collision == 1:
            self.sprite = self.spr_hit

        if self.life == 0:
            self.sprite = self.spr_hit

        self.x = self.x + (cos(((math.pi * self.angle)/180)) * self.speed)
        self.y = self.y + (sin(((math.pi * self.angle)/180)) * self.speed)

        self.step()

        drawObj(self)

        if self.collision == 1:
            object_list.remove(self)
            self.kill()

        if self.life == 0:
            object_list.remove(self)
            self.kill()

######################################################################
######################################################################

class proj_bullet_1(projectile):

    def __init__(self,x,y,angle):

        self.x = x
        self.y = y
        self.team = 0 # 0 is the player team???
        self.speed = 20 # 10 is the default bullet speed???
        self.angle = angle # get from the angle of the gun at the moment of shooting
        self.spr_fly = 'proj_bullet_1_fly_0.png'
        self.spr_hit = 'proj_bullet_1_hit_0.png'
        self.life = 60

        projectile.__init__(self,self.x,self.y,self.team,self.speed,self.angle,self.spr_fly,self.spr_hit)

    def step(self):
        
        x = 1

######################################################################

class proj_nme_bullet_1(projectile):

    def __init__(self,x,y,angle):

        self.x = x
        self.y = y
        self.team = 1 # 1 is the bandit team???
        self.speed = 7 
        self.angle = angle # get from the angle of the gun at the moment of shooting
        self.spr_fly = 'proj_nme_bullet_1_fly_0.png'
        self.spr_hit = 'proj_nme_bullet_1_hit_0.png'
        self.life = 60

        projectile.__init__(self,self.x,self.y,self.team,self.speed,self.angle,self.spr_fly,self.spr_hit)

    def step(self):
        
        x = 1

######################################################################

class proj_shell_1(projectile):

    def __init__(self,x,y,angle):

        self.x = x
        self.y = y

        self.team = 0 # 0 is the player team???
        self.speed = 30 # 10 is the default bullet speed??? 10 is slow
        self.angle = angle # get from the angle of the gun at the moment of shooting
        self.spr_fly = 'proj_bullet_1_fly_0.png'
        self.spr_hit = 'proj_bullet_1_hit_0.png'
        self.life = 10

        projectile.__init__(self,self.x,self.y,self.team,self.speed,self.angle,self.spr_fly,self.spr_hit)

    def step(self): # THIS IS IN HERE SO THAT SHELLS SLOW DOWN AS THEY MOVE

        self.speed = self.speed - 3 #RIGHT HERE

######################################################################

class proj_flak_1(projectile):

    def __init__(self,x,y,angle):

        self.x = x
        self.y = y

        self.team = 0 # 0 is the player team???
        self.speed = 30 # 10 is the default bullet speed??? 10 is slow
        self.angle = angle # get from the angle of the gun at the moment of shooting
        self.spr_fly = 'proj_bullet_1_fly_0.png'
        self.spr_hit = 'proj_bullet_1_hit_0.png'
        self.life = 15

        projectile.__init__(self,self.x,self.y,self.team,self.speed,self.angle,self.spr_fly,self.spr_hit)

    def step(self): 

        self.speed = self.speed - 2 #RIGHT HERE

        if (self.speed == 0) or (self.life == -1):

            xin = self.x
            yin = self.y
            ain = 0 - self.angle

            random_0 = random.randrange(15,25)
            random_1 = random.randrange(5,15)
            random_2 = random.randrange(-5,5)
            random_3 = random.randrange(-15,-5)
            random_4 = random.randrange(-25,-15)
            bullet_shot_0 = proj_shell_1(xin,yin, 0 - ain + random_0)
            bullet_shot_1 = proj_shell_1(xin,yin, 0 - ain + random_1)
            bullet_shot_2 = proj_shell_1(xin,yin, 0 - ain + random_2)
            bullet_shot_3 = proj_shell_1(xin,yin, 0 - ain + random_3)
            bullet_shot_4 = proj_shell_1(xin,yin, 0 - ain + random_4)

######################################################################
######################################################################

def shoot_check(obj):
    
    if (pygame.mouse.get_pressed()[0]) == False:
        obj.mouseup = True

    if obj.wep_a.cooldown == 0:
        if obj.wep_a.auto == 0:
            if obj.mouseup == True:
                if (pygame.mouse.get_pressed()[0]) == True:
                    obj.wep_a.fire()
                    obj.fired = 1
                    obj.mouseup = False
        if obj.wep_a.auto == 1:
            if obj.mouseup == True:
                if (pygame.mouse.get_pressed()[0]) == True:
                    obj.wep_a.fire()
                    obj.fired = 0
                    obj.mouseup = True

    if obj.wep_a.cooldown > 0:
        obj.wep_a.cooldown = obj.wep_a.cooldown - 1

######################################################################

def update_velo(obj): # this code calculate velo but keeps it sane with a x/2 scheme
                      # update this to be all inclusive for bullets and all objects
                      # and include collision detection
    if obj.vx > 0:
        obj.x = obj.x + (obj.vx / 2)
        obj.vx = obj.vx - 1
    if obj.vx < 0:
        obj.x = obj.x + (obj.vx / 2)
        obj.vx = obj.vx + 1
    if obj.vy > 0:
        obj.y = obj.y + (obj.vy / 2)
        obj.vy = obj.vy - 1
    if obj.vy < 0:
        obj.y = obj.y + (obj.vy / 2)
        obj.vy = obj.vy + 1

######################################################################

def draw_passive(self,spr_list):

        self.tick_passive = 1 + self.tick_passive

        if self.tick_passive > len(spr_list * self.anim_speed):
            self.tick_passive = 0
        self.sprite = spr_list[int((self.tick_passive - 1)/self.anim_speed)]

######################################################################

def draw_active(self,spr_list,anim_speed):

    self.sprite = spr_list[self.tick_active]
    #write code here to iterate thru the sprite list
    #at the specified speed. do it later thought.

    #also, getting hurt will be an animation with
    #sprites but it will be passive. there will
    #also be a draw effect which will flash the
    #entity white for 2 frames no matter what
    #scratch that. there will be no animation,
    #just the flashy bit.

######################################################################

def drawObj(obj):

    orig_rect = (pygame.image.load(obj.sprite)).get_rect()
    rot_image = pygame.transform.rotate((pygame.image.load(obj.sprite)), obj.angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    
    screen.blit(rot_image,(obj.x,obj.y)) #all the nonsense above enables rotating

######################################################################

######################################################################
######################################################################
####RANDOM INITIALIZATION STUFF UNDER HERE############################
######################################################################
######################################################################

pygame.init() #starts pygame
screen = pygame.display.set_mode((512,512)) #sets resoltion
clock = pygame.time.Clock()
crashed = False
flags = DOUBLEBUF

######################################################################

class mouse_obj(): #this has to be placed after the screen is initialized

    def __init__(self): # make a cursor at some point with this class

        self.x = (pygame.mouse.get_pos())[0]
        self.y = (pygame.mouse.get_pos())[1]

    def update(self):

        self.x = (pygame.mouse.get_pos())[0]
        self.y = (pygame.mouse.get_pos())[1]

######################################################################

the_mouse = mouse_obj() # here's good

player = mut_fish(100,100) 
#makes a mut of type dot, at 100,100

test9129038 = nme_bandit(150,150)

######################################################################
######################################################################
######################################################################
######################################################################
######################################################################

while not crashed:

    screen.fill((130,105,90))#makes the background fill brown :/

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
    # at some point menu selection and drawing needs to be implemented

    for obj in object_list:
        obj.update()

    the_mouse.update()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
quit()

######################################################################
######################################################################
######################################################################
######################################################################
######################################################################

#END OF CODE#