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

import math
import threading
from random import random

"""Just go to the bottom of the file"""

class Rect:

    def __init__(self, pos, size):
        self.x, self.y = pos
        self.w, self.h = size

    def colliderect(self, other):

        if (self.w == 0 or self.h == 0 or other.w == 0 or other.h == 0):
            return False

        return (min(self.x, self.x + self.w) < max(other.x, other.x + other.w) and
                min(self.y, self.y + self.h) < max(other.y, other.y + other.h) and
                max(self.x, self.x + self.w) > min(other.x, other.x + other.w) and
                max(self.y, self.y + self.h) > min(other.y, other.y + other.h))


class fRect:
    '''
    pygame's Rect class can only be used to represent whole integer vertices, so we create a rectangle class that can have floating point coordinates
    '''

    def __init__(self, pos, size):
        self.pos = (pos[0], pos[1])
        self.size = (size[0], size[1])

    def move(self, x, y):
        return fRect((self.pos[0]+x, self.pos[1]+y), self.size)

    def move_ip(self, x, y, move_factor=1):
        self.pos = (self.pos[0] + x*move_factor, self.pos[1] + y*move_factor)

    def get_rect(self):
        return Rect(self.pos, self.size)

    def copy(self):
        return fRect(self.pos, self.size)

    def intersect(self, other_frect):
        # two rectangles intersect iff both x and y projections intersect
        for i in range(2):
            if self.pos[i] < other_frect.pos[i]:  # projection of self begins to the left
                if other_frect.pos[i] >= self.pos[i] + self.size[i]:
                    return 0
            elif self.pos[i] > other_frect.pos[i]:
                if self.pos[i] >= other_frect.pos[i] + other_frect.size[i]:
                    return 0
        return 1  # self.size > 0 and other_frect.size > 0


class Paddle:
    def __init__(self, pos, size, speed, max_angle,  facing):
        self.frect = fRect((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        self.speed = speed
        self.size = size
        self.facing = facing
        self.max_angle = max_angle

    def factor_accelerate(self, factor):
        self.speed = factor*self.speed

    def move(self, enemy_frect, ball_frect, table_size):
        direction = self.move_getter(
            self.frect.copy(), enemy_frect.copy(), ball_frect.copy(), tuple(table_size))
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

    def get_face_pts(self):
        return ((self.frect.pos[0] + self.frect.size[0]*self.facing, self.frect.pos[1]),
                (self.frect.pos[0] + self.frect.size[0]*self.facing,
                 self.frect.pos[1] + self.frect.size[1]-1)
                )

    def get_angle(self, y):
        center = self.frect.pos[1]+self.size[1]/2
        rel_dist_from_c = ((y-center)/self.size[1])
        rel_dist_from_c = min(0.5, rel_dist_from_c)
        rel_dist_from_c = max(-0.5, rel_dist_from_c)
        sign = 1-2*self.facing

        return sign*rel_dist_from_c*self.max_angle*math.pi/180


class Ball:
    def __init__(self, table_size, size, paddle_bounce, wall_bounce, dust_error, init_speed_mag):
        rand_ang = (.4+.4*random())*math.pi * \
            (1-2*(random() > .5))+.5*math.pi
        #rand_ang = -110*math.pi/180
        speed = (init_speed_mag*math.cos(rand_ang),
                 init_speed_mag*math.sin(rand_ang))
        pos = (table_size[0]/2, table_size[1]/2)
        #pos = (table_size[0]/2 - 181, table_size[1]/2 - 105)
        self.frect = fRect((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        self.speed = speed
        self.size = size
        self.paddle_bounce = paddle_bounce
        self.wall_bounce = wall_bounce
        self.dust_error = dust_error
        self.init_speed_mag = init_speed_mag
        self.prev_bounce = None

    def get_center(self):
        return (self.frect.pos[0] + .5*self.frect.size[0], self.frect.pos[1] + .5*self.frect.size[1])

    def get_speed_mag(self):
        return math.sqrt(self.speed[0]**2+self.speed[1]**2)

    def factor_accelerate(self, factor):
        self.speed = (factor*self.speed[0], factor*self.speed[1])

    def move(self, paddles, table_size, move_factor):
        moved = 0
        walls_Rects = [Rect((-100, -100), (table_size[0]+200, 100)),
                       Rect((-100, table_size[1]), (table_size[0]+200, 100))]

        for wall_rect in walls_Rects:
            if self.frect.get_rect().colliderect(wall_rect):
                c = 0
                # print "in wall. speed: ", self.speed
                while self.frect.get_rect().colliderect(wall_rect):
                    self.frect.move_ip(-.1 *
                                       self.speed[0], -.1*self.speed[1], move_factor)
                    c += 1  # this basically tells us how far the ball has traveled into the wall
                r1 = 1+2*(random()-.5)*self.dust_error
                r2 = 1+2*(random()-.5)*self.dust_error

                self.speed = (
                    self.wall_bounce*self.speed[0]*r1, -self.wall_bounce*self.speed[1]*r2)
                while c > 0 or self.frect.get_rect().colliderect(wall_rect):
                    self.frect.move_ip(.1 *
                                       self.speed[0], .1*self.speed[1], move_factor)
                    c -= 1  # move by roughly the same amount as the ball had traveled into the wall
                moved = 1
                # print "out of wall, position, speed: ", self.frect.pos, self.speed

        for paddle in paddles:
            if self.frect.intersect(paddle.frect):
                if (paddle.facing == 1 and self.get_center()[0] < paddle.frect.pos[0] + paddle.frect.size[0]/2) or \
                        (paddle.facing == 0 and self.get_center()[0] > paddle.frect.pos[0] + paddle.frect.size[0]/2):
                    continue

                c = 0

                while self.frect.intersect(paddle.frect) and not self.frect.get_rect().colliderect(walls_Rects[0]) and not self.frect.get_rect().colliderect(walls_Rects[1]):
                    self.frect.move_ip(-.1 *
                                       self.speed[0], -.1*self.speed[1], move_factor)

                    c += 1
                theta = paddle.get_angle(
                    self.frect.pos[1]+.5*self.frect.size[1])

                v = self.speed

                v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                     math.sin(theta)*v[0]+math.cos(theta)*v[1]]

                v[0] = -v[0]

                v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                     math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]

                # Bona fide hack: enforce a lower bound on horizontal speed and disallow back reflection
                # ball is not traveling (a) away from paddle (b) at a sufficient speed
                if v[0]*(2*paddle.facing-1) < 1:
                    # transform y velocity so as to maintain the speed
                    v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1)
                    # note that minimal horiz speed will be lower than we're used to, where it was 0.95 prior to increase by *1.2
                    v[0] = (2*paddle.facing-1)

                # a bit hacky, prevent multiple bounces from accelerating
                # the ball too much
                if not paddle is self.prev_bounce:
                    self.speed = (v[0]*self.paddle_bounce,
                                  v[1]*self.paddle_bounce)
                else:
                    self.speed = (v[0], v[1])
                self.prev_bounce = paddle
                # print "transformed speed: ", self.speed

                while c > 0 or self.frect.intersect(paddle.frect):
                    # print "move_ip()"
                    self.frect.move_ip(.1 *
                                       self.speed[0], .1*self.speed[1], move_factor)
                    # print "ball position forward trace: ", self.frect.pos
                    c -= 1
                # print "pos final: (" + str(self.frect.pos[0]) + "," + str(self.frect.pos[1]) + ")"
                # print "speed x y: ", self.speed[0], self.speed[1]

                moved = 1
                # print "out of paddle, speed: ", self.speed

        # if we didn't take care of not driving the ball into a wall by backtracing above it could have happened that
        # we would end up inside the wall here due to the way we do paddle bounces
        # this happens because we backtrace (c++) using incoming velocity, but correct post-factum (c--) using new velocity
        # the velocity would then be transformed by a wall hit, and the ball would end up on the dark side of the wall

        if not moved:
            self.frect.move_ip(self.speed[0], self.speed[1], move_factor)
            # print "moving "
        # print "poition: ", self.frect.pos


def check_point(score, ball, table_size):
    if ball.frect.pos[0]+ball.size[0]/2 < 0:
        score[1] += 1
        ball = Ball(table_size, ball.size, ball.paddle_bounce,
                    ball.wall_bounce, ball.dust_error, ball.init_speed_mag)
        return (ball, score)
    elif ball.frect.pos[0]+ball.size[0]/2 >= table_size[0]:
        ball = Ball(table_size, ball.size, ball.paddle_bounce,
                    ball.wall_bounce, ball.dust_error, ball.init_speed_mag)
        score[0] += 1
        return (ball, score)

    return (ball, score)


def game_loop(paddles, ball, table_size, score_to_win):
    score = [0, 0]

    while max(score) < score_to_win:
        ball, score = check_point(score, ball, table_size)
        paddles[0].move(paddles[1].frect, ball.frect, table_size)
        paddles[1].move(paddles[0].frect, ball.frect, table_size)

        inv_move_factor = int((ball.speed[0]**2+ball.speed[1]**2)**.5)
        if inv_move_factor > 0:
            for i in range(inv_move_factor):
                ball.move(paddles, table_size, 1./inv_move_factor)
        else:
            ball.move(paddles, table_size, 1)

    return(score)
    # return


def play(ai1, ai2):
    table_size = (440, 280)
    paddle_size = (10, 70)
    ball_size = (15, 15)
    paddle_speed = 1
    max_angle = 45

    paddle_bounce = 1.2
    wall_bounce = 1.00
    dust_error = 0.00
    init_speed_mag = 2
    score_to_win = 5000

    paddles = [Paddle((20, table_size[1]/2), paddle_size, paddle_speed, max_angle,  1),
               Paddle((table_size[0]-20, table_size[1]/2), paddle_size, paddle_speed, max_angle, 0)]

    ball = Ball(table_size, ball_size, paddle_bounce,
                wall_bounce, dust_error, init_speed_mag)

    paddles[0].move_getter = ai1
    paddles[1].move_getter = ai2

    round1 = game_loop(paddles, ball, table_size, score_to_win)

    ball = Ball(table_size, ball_size, paddle_bounce,
                wall_bounce, dust_error, init_speed_mag)

    paddles[0].move_getter, paddles[1].move_getter = paddles[1].move_getter, paddles[0].move_getter

    round2 = game_loop(paddles, ball, table_size, score_to_win)

    return round1, round2


if __name__ == "__main__":
    from chaser_ai import pong_ai as ai1 ## !!!
    from ted_ai import pong_ai as ai2

    results = play(ai1, ai2)
    """ 
    play(ai1, ai2) returns a tuple of 2 lists, each list being representing a round with 2 numbers:
    ([wins for ai1, wins for ai2],
    [wins for ai2, wins for ai1])
    """
    # comment this part out if you are parsing results automatically
    names = [" Your AI", "Other AI"]
    print("\n    ".join(["Round 1:"] + [names[i] + ": " + str(results[0][i]) for i in range(2)]))
    names.reverse()
    print("\n    ".join(["Round 2:"] + [names[i] + ": " + str(results[1][i]) for i in range(2)]))