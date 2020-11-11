#   PongAIvAI
#   Authors: Michael Guerzhoy and Denis Begun, 2014-2020.
#   http://www.cs.toronto.edu/~guerzhoy/
#   Email: guerzhoy at cs.toronto.edu
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version. You must credit the authors
#   for the original parts of this code.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Parts of the code are based on T. S. Hayden Dennison's PongClone (2011)
#   http://www.pygame.org/project-PongClone-1740-3032.html



import pygame, sys, time, random, os
from pygame.locals import *

import math

#rgb values
white = [255, 255, 255]
black = [0, 0, 0]
clock = pygame.time.Clock()

class fRect:
    '''
    pygame's Rect class can only be used to represent whole integer vertices, so we create a rectangle class that can have floating point coordinates
    '''
    def __init__(self, pos, size):
        self.pos = (pos[0], pos[1])
        self.size = (size[0], size[1])

    def move(self, x, y):
        return fRect((self.pos[0]+x, self.pos[1]+y), self.size)

    #same as move but can take in an extra parameter(move_factor)
    #I think move_factor represents velocity(?)
    def move_ip(self, x, y, move_factor = 1):
        self.pos = (self.pos[0] + x*move_factor, self.pos[1] + y*move_factor)

    def get_rect(self):
        return Rect(self.pos, self.size)

    def copy(self):
        return fRect(self.pos, self.size)

    # checks if two rectangles intersect iff both x and y projections intersect
    def intersect(self, other_frect):
        for i in range(2):
            if self.pos[i] < other_frect.pos[i]: # projection of self begins to the left
                if other_frect.pos[i] >= self.pos[i] + self.size[i]:
                    return 0
            elif self.pos[i] > other_frect.pos[i]:
                if self.pos[i] >= other_frect.pos[i] + other_frect.size[i]:
                    return 0
        return 1 #self.size > 0 and other_frect.size > 0


class Paddle:
    def __init__(self, pos, size, speed, max_angle, facing, timeout):
        self.frect = fRect((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        self.speed = speed
        self.size = size
        self.facing = facing # note that facing = 1 refers to facing to the right
        self.max_angle = max_angle
        self.timeout = timeout

    def factor_accelerate(self, factor):
        self.speed = factor*self.speed

    # as describes, moves the paddle
    def move(self, enemy_frect, ball_frect, table_size):
        direction = self.move_getter(self.frect.copy(), enemy_frect.copy(), ball_frect.copy(), tuple(table_size))
        #direction = timeout(self.move_getter, (self.frect.copy(), enemy_frect.copy(), ball_frect.copy(), tuple(table_size)), {}, self.timeout)
        if direction == "up":
            self.frect.move_ip(0, -self.speed)
        elif direction == "down":
            self.frect.move_ip(0, self.speed)

        to_bottom = (self.frect.pos[1]+self.frect.size[1])-table_size[1]

        if to_bottom > 0:
            self.frect.move_ip(0, -to_bottom)
        to_top = self.frect.pos[1]
        if to_top < 0:
            self.frect.move_ip(0, -to_top)

    # function is never called so don't worry about it
    def get_face_pts(self):
        return ((self.frect.pos[0] + self.frect.size[0]*self.facing, self.frect.pos[1]),
                (self.frect.pos[0] + self.frect.size[0]*self.facing, self.frect.pos[1] + self.frect.size[1]-1)
                )

    # gets the angle between the center points of self (paddle) and another rectangle
    # angle varies linearly from -22.5 to 22.5 degrees based on the height
    def get_angle(self, y): # y represents the center y point of the "other" rect
        center = self.frect.pos[1]+self.size[1]/2 # center y point of paddle
        rel_dist_from_c = ((y-center)/self.size[1]) # unsure how this part works....
        rel_dist_from_c = min(0.5, rel_dist_from_c)
        rel_dist_from_c = max(-0.5, rel_dist_from_c)
        sign = 1-2*self.facing # takes into account which side the paddle is facing

        return sign*rel_dist_from_c*self.max_angle*math.pi/180 #return in radians


class Ball:
    def __init__(self, table_size, size, paddle_bounce, wall_bounce, dust_error, init_speed_mag):
        rand_ang = (.4+.4*random.random())*math.pi*(1-2*(random.random()>.5))+.5*math.pi #starting random angle
        #rand_ang = -110*math.pi/180
        speed = (init_speed_mag*math.cos(rand_ang), init_speed_mag*math.sin(rand_ang))
        pos = (table_size[0]/2, table_size[1]/2)
        #pos = (table_size[0]/2 - 181, table_size[1]/2 - 105)
        self.frect = fRect((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        self.speed = speed
        self.size = size
        self.paddle_bounce = paddle_bounce # how much the ball accelerates when it hits the paddle (1.20)
        self.wall_bounce = wall_bounce # how much the ball accelerates when it hits the wall (1.00)
        self.dust_error = dust_error # 0 for our purposes
        self.init_speed_mag = init_speed_mag
        self.prev_bounce = None # the previous paddle that hit the ball

    #keep in mind that the pos(x,y) of the ball refers to the upper left corner
    #thus this function gets the actual center position
    def get_center(self):
        return (self.frect.pos[0] + .5*self.frect.size[0], self.frect.pos[1] + .5*self.frect.size[1])

    #magnitude of the speed of the ball
    def get_speed_mag(self):
        return math.sqrt(self.speed[0]**2+self.speed[1]**2)

    #function never gets called so I think we can ignore
    def factor_accelerate(self, factor):
        self.speed = (factor*self.speed[0], factor*self.speed[1])

    #this function moves the position of the ball as described but also handles collisions
    def move(self, paddles, table_size, move_factor):

        moved = 0 # honestly should be a bool but basically just checks if a collision has occured 

        walls_Rects = [Rect((-100, -100), (table_size[0]+200, 100)),
                       Rect((-100, table_size[1]), (table_size[0]+200, 100))]

        # think of wall_rects as two rectangles "sandwhiching" the game 
        # whenever the ball hits a rectangle it bounces off of it hence creating the borders of the game
    #   ---------------------
    #   |                   | <-- upper rectangle (wall)
    #   ---------------------
    #   
    #   |                   |
    #   |       O <--ball   | <-- paddle (can also think of as a wall)
    #   |                   |
    #   
    #   ---------------------
    #   |                   | <-- lower rectangle (wall)
    #   ---------------------

        #loops through the "wall" rectangles        
        for wall_rect in walls_Rects:
            if self.frect.get_rect().colliderect(wall_rect): #checks if there's collision between wall and ball
                # note this^ might be confusing to those who haven't learnt classes / object oriented programming yet
                # all you have to know is that get_rect() returns the pos and size of the "ball" and that
                # colliderect checks if the rectangle returned by get_rect() is in collision with another rectangle
                # which in this case is "wall_rect"

                #----------------------------------------------

                # ngl the part below kinda is a mind f***
                # basically when the ball hits a wall, it actually goes into the wall a bit (think about the imperfections between frames)
                # so we find the distance that the ball has travelled inside the wall and we correct it
                # by adding that distance to its theoretical path
                
                # below is what Guerzhoy wrote:
                # if we didn't take care of not driving the ball into a wall by backtracing above it could have happened that
                # we would end up inside the wall here due to the way we do paddle bounces
                # this happens because we backtrace (c++) using incoming velocity, but correct post-factum (c--) using new velocity
                # the velocity would then be transformed by a wall hit, and the ball would end up on the dark side of the wall

                c = 0 #rough representation of how far the ball travelled inside the wall
                while self.frect.get_rect().colliderect(wall_rect): 
                    self.frect.move_ip(-.1*self.speed[0], -.1*self.speed[1], move_factor) #we move the ball until it's no longer hitting the wall
                    c += 1 # this basically tells us how far the ball has traveled into the wall
                
                #ignore everything after the 1 because self.dust_error is always 0 for our purposes
                r1 = 1+2*(random.random()-.5)*self.dust_error
                r2 = 1+2*(random.random()-.5)*self.dust_error

                #reverses the y component of the speed of the ball (think of what happens when a ball hits the wall)
                self.speed = (self.wall_bounce*self.speed[0]*r1, -self.wall_bounce*self.speed[1]*r2)

                #now we use the C value calculated earlier and add that distance to the path it "should've"
                #taken had it hit the wall perfectly
                while c > 0 or self.frect.get_rect().colliderect(wall_rect):
                    self.frect.move_ip(.1*self.speed[0], .1*self.speed[1], move_factor) 
                    c -= 1 # move by roughly the same amount as the ball had traveled into the wall
                moved = 1
                #print "out of wall, position, speed: ", self.frect.pos, self.speed

        for paddle in paddles:
            if self.frect.intersect(paddle.frect): #checks if the ball is in collision with a paddle

                # if the ball is behind the paddle (but still in collision) we do nothing
                # I think this represents when the ball hits the upper edge (?), in which case the paddle won't
                # stop the ball from scoring
                if (paddle.facing == 1 and self.get_center()[0] < paddle.frect.pos[0] + paddle.frect.size[0]/2) or \
                (paddle.facing == 0 and self.get_center()[0] > paddle.frect.pos[0] + paddle.frect.size[0]/2):
                    continue
    

                c = 0 # same idea as the c value for walls, represents how far the ball has travelled inside the paddle
                
                # once again Guerzhoy uses backtracking to get a more accurate final trajectory of the ball
                # in collision with a paddle
                while self.frect.intersect(paddle.frect) and not self.frect.get_rect().colliderect(walls_Rects[0]) and not self.frect.get_rect().colliderect(walls_Rects[1]):
                    self.frect.move_ip(-.1*self.speed[0], -.1*self.speed[1], move_factor)
                    c += 1

                # angle between paddle and ball (?)
                theta = paddle.get_angle(self.frect.pos[1]+.5*self.frect.size[1])
            
                v = self.speed
                # converts some of the x-velocity to y-velocity or vice versa by using theta
                v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                             math.sin(theta)*v[0]+math.cos(theta)*v[1]]

                v[0] = -v[0] #reverses the x-velocity
                # same thing as a few lines above now with a converted velocity
                v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                              math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]


                # Bona fide hack: enforce a lower bound on horizontal speed and disallow back reflection
                if  v[0]*(2*paddle.facing-1) < 1: # ball is not traveling (a) away from paddle (b) at a sufficient speed
                    v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1) # transform y velocity so as to maintain the speed
                    v[0] = (2*paddle.facing-1) # note that minimal horiz speed will be lower than we're used to, where it was 0.95 prior to increase by *1.2

                # a bit hacky, prevents multiple bounces from accelerating the ball too much
                # this part accelerates the ball with each hit....
                # not exactly sure how the if statement works and why it's even there (?)
                if not paddle is self.prev_bounce:
                    self.speed = (v[0]*self.paddle_bounce, v[1]*self.paddle_bounce)
                else:
                    self.speed = (v[0], v[1])
                self.prev_bounce = paddle
                #print "transformed speed: ", self.speed

                # backtracking part as explained earlier
                while c > 0 or self.frect.intersect(paddle.frect):
                    #print "move_ip()"
                    self.frect.move_ip(.1*self.speed[0], .1*self.speed[1], move_factor)
                    #print "ball position forward trace: ", self.frect.pos
                    c -= 1
                #print "pos final: (" + str(self.frect.pos[0]) + "," + str(self.frect.pos[1]) + ")"
                #print "speed x y: ", self.speed[0], self.speed[1]

                moved = 1
                #print "out of paddle, speed: ", self.speed

        if not moved: #basically if no collision has occured
            self.frect.move_ip(self.speed[0], self.speed[1], move_factor)
            #print "moving "
        #print "poition: ", self.frect.pos


#manual keyboard control of paddle
def directions_from_input(paddle_rect, other_paddle_rect, ball_rect, table_size):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        return "up"
    elif keys[pygame.K_DOWN]:
        return "down"
    else:
        return None


#so that our code does not exceed a certain time limit
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''From:
    http://code.activestate.com/recipes/473878-timeout-function-using-threading/'''
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                self.result = default

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        print("TIMEOUT")
        return default
    else:
        return it.result


#where pygame displays all the objects, not really useful for our purposes
def render(screen, paddles, ball, score, table_size):
    screen.fill(black)

    pygame.draw.rect(screen, white, paddles[0].frect.get_rect())
    pygame.draw.rect(screen, white, paddles[1].frect.get_rect())

    pygame.draw.circle(screen, white, (int(ball.get_center()[0]), int(ball.get_center()[1])),  int(ball.frect.size[0]/2), 0)


    pygame.draw.line(screen, white, [screen.get_width()/2, 0], [screen.get_width()/2, screen.get_height()])

    score_font = pygame.font.Font(None, 32)
    screen.blit(score_font.render(str(score[0]), True, white), [int(0.4*table_size[0])-8, 0])
    screen.blit(score_font.render(str(score[1]), True, white), [int(0.6*table_size[0])-8, 0])

    pygame.display.flip()


#this function checks if a point has been scored
def check_point(score, ball, table_size):
    #point scored on left side
    if ball.frect.pos[0]+ball.size[0]/2 < 0:
        score[1] += 1
        ball = Ball(table_size, ball.size, ball.paddle_bounce, ball.wall_bounce, ball.dust_error, ball.init_speed_mag)
        return (ball, score)
    #point scored on right side
    elif ball.frect.pos[0]+ball.size[0]/2 >= table_size[0]:
        ball = Ball(table_size, ball.size, ball.paddle_bounce, ball.wall_bounce, ball.dust_error, ball.init_speed_mag)
        score[0] += 1
        return (ball, score)

    return (ball, score)


def game_loop(screen, paddles, ball, table_size, clock_rate, turn_wait_rate, score_to_win, display):
    score = [0, 0]

    while max(score) < score_to_win:
        old_score = score[:]
        ball, score = check_point(score, ball, table_size)
        paddles[0].move(paddles[1].frect, ball.frect, table_size)
        paddles[1].move(paddles[0].frect, ball.frect, table_size)
        
        inv_move_factor = int((ball.speed[0]**2+ball.speed[1]**2)**.5) #sqrt(ball.speed[0] ^ 2 + ball.speed[1] ^ 2)
        # If the speed is high enough, we move the ball in small steps (I think)
        if inv_move_factor > 0:
            for i in range(inv_move_factor):
                ball.move(paddles, table_size, 1./inv_move_factor)
        else:
            ball.move(paddles, table_size, 1)

        #print("BALL SPEED: ", ball.speed)
        
        if not display:
            continue
        # if a point has been scored
        if score != old_score:
            font = pygame.font.Font(None, 32)
            if score[0] != old_score[0]:
                screen.blit(font.render("Left scores!", True, white, black), [0, 32])
            else:
                screen.blit(font.render("Right scores!", True, white, black), [int(table_size[0]/2+20), 32])

            pygame.display.flip()
            clock.tick(turn_wait_rate)

        # renders all the objects
        render(screen, paddles, ball, score, table_size)

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_q]:
            return

        clock.tick(clock_rate)

    #once the game has ended
    font = pygame.font.Font(None, 64)
    if score[0] > score[1]:
        screen.blit(font.render("Left wins!", True, white, black), [24, 32])
    else:
        screen.blit(font.render("Right wins!", True, white, black), [24, 32])
    pygame.display.flip()
    clock.tick(2)

    pygame.event.pump()
    while any(pygame.key.get_pressed()):
        pygame.event.pump()
        clock.tick(30)

    print(score)
    # return

def init_game():
    table_size = (440, 280)
    paddle_size = (10, 70)
    ball_size = (15, 15)
    paddle_speed = 1
    max_angle = 45

    paddle_bounce = 1.2
    wall_bounce = 1.00
    dust_error = 0.00
    init_speed_mag = 2
    timeout = 0.0003
    clock_rate = 80
    turn_wait_rate = 3
    score_to_win = 10


    screen = pygame.display.set_mode(table_size)
    pygame.display.set_caption('PongAIvAI')

    paddles = [Paddle((20, table_size[1]/2), paddle_size, paddle_speed, max_angle,  1, timeout),
               Paddle((table_size[0]-20, table_size[1]/2), paddle_size, paddle_speed, max_angle, 0, timeout)]
    ball = Ball(table_size, ball_size, paddle_bounce, wall_bounce, dust_error, init_speed_mag)

    import chaser_ai, bot_ai
    
    paddles[0].move_getter = chaser_ai.pong_ai
    paddles[1].move_getter = bot_ai.pong_ai #chaser_ai.pong_ai
    
    # note that the game loop is run twice to simulate the AIs playing either side
    game_loop(screen, paddles, ball, table_size, clock_rate, turn_wait_rate, score_to_win, 1)
    
    screen.blit(pygame.font.Font(None, 32).render(str('SWITCHING SIDES'), True, white), [int(0.6*table_size[0])-8, 0])
    
    pygame.display.flip()
    clock.tick(4)
    
    paddles[0].move_getter, paddles[1].move_getter = paddles[1].move_getter, paddles[0].move_getter
    
    game_loop(screen, paddles, ball, table_size, clock_rate, turn_wait_rate, score_to_win, 1)
    
    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    init_game()