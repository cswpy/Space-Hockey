from math import cos, sin, atan2, pi
import random

add_library('minim')
audioPlayer = Minim(this)

n, m = 400, 600
r1 = 10    # smallest possible radius
r2 = 3*r1  # biggest possible radius

class Puck:
    def __init__(self, isUP):
        self.isUP = isUP # UP or DOWN
        
        # Center the Puck when initializing
        # coordinates are absolute, i.e., using the bottom half coordinates
        if isUP:
            self.x = int(n/2)
            self.y = int(m/4)  
        else:
            self.x = int(n/2)
            self.y = int(3*m/4)  
        
        # self.eventKeys # [Up, Down, Right, Left]

    @property
    def ratio(self):
        relative = abs(self.y - m/2)
        if r1 <= relative <= m/2 - r2:
            return (relative-r1) / (m/2.0 - r1 - r2) # Why 2.0 works while 2 does not
        else:
            raise Exception
        
    @property
    def radii(self):
        r = r1 + self.ratio * (r2-r1)
        return [r, r + r1 * (1 + self.ratio)] # return [puck radius, capturing radius]
    
    @property
    def angle(self):
        return (1 - self.ratio) * (PI/2 - PI/12) + PI/12


    def draw_Puck(self):
        _ = self.radii
        
        fill(255, 0 ,0)
        if self.isUP:
            arc(self.x, self.y, 2*_[1], 2*_[1], 3*PI/2 - self.angle, 3*PI/2 + self.angle)
        else:
            arc(self.x, self.y, 2*_[1], 2*_[1], PI/2 - self.angle, PI/2 + self.angle)
        
        noStroke(); fill(0, 0, 255)
        image(img_puck, self.x - _[0], self.y - _[0], 2*_[0], 2*_[0])
        # circle(self.x, self.y, 2*_[0])
                
        stroke(0); noFill()
        circle(self.x, self.y, 2*_[1])

        
    def draw_Line(self):
        strokeWeight(1)
        noFill()
        if self.isUP:
            # (r,r)        (n-r, r)
            # (r, m/2-r)   (n-r, m/2-r)
            line(r2, r2, n-r2, r2)
            line(r2, r2, r1, m/2-r1)
            line(n-r1, m/2-r1, n-r2, r2)
            line(n-r1, m/2-r1, r1, m/2-r1)
        else:
            # (r, m/2+r)   (n-r, m/2+r)
            # (r, m-r)   (n-r, m-r)
            line(r1, m/2+r1, n-r1, m/2+r1)
            line(r1, m/2+r1, r2, m-r2)
            line(n-r2, m-r2, n-r1, m/2+r1)
            line(n-r2, m-r2, r2, m-r2)
        
    def draw(self):
        self.draw_Line()
        self.draw_Puck()
        
    def move(self, x, y):
        # if y < m/2 + r1:
        #     y = m/2 + r1
        # elif y > m - r2:
        #     y = m - r2

        # r = self.radii[0]
        # if x < r:
        #     x = r
        # elif x > n-r:
        #     x = n - r
            
        # if self.isUP:
        #     self.x = n - x
        #     self.y = m - y
        # else:
        #     self.x = x
        #     self.y = y
        
        # -------------------------
        
        if not self.isUP:
            if y < m/2 + r1:
                y = m/2 + r1
            elif y > m - r2:
                y = m - r2
    
            r = self.radii[0]
            if x < r:
                x = r
            elif x > n-r:
                x = n - r
        else:
            if y > m/2 - r1:
                y = m/2 - r1
            elif y < r2:
                y = r2
    
            r = self.radii[0]
            if x < r:
                x = r
            elif x > n-r:
                x = n - r
                
        self.x = x
        self.y = y

class Ball:
    def __init__(self, PuckA, PuckB, game):
        self.x = n/2
        self.y = m/2
        
        self.lock = None # None, 'A', 'B'
        # PuckA is UP
        # PuckB is Down
        
        # (Puck, Phi, dPhi, isDanger, wasDanger, catch)
        # direction can be -1 or 1, I guess?
        self.A = [PuckA, None, None, False, False, False]
        self.B = [PuckB, None, None, False, False, False]
        self.isUp = False
        
        self.a = random.random() * 2 * pi # Angle
        self.vel = 7
        self.vel_ang = 0.1
        self.alive = True
        
        self.game = game
        
        # Velocity: If zero, then stop
        
        self.trail = []
        
    def draw(self):
        if len(self.trail) < 30:
            self.trail.append((self.x, self.y))
        else:
            self.trail.pop(0)
            self.trail.append((self.x, self.y))
            
        
        for i in range(len(self.trail)):
            fill(255 - (i+1)*255/len(self.trail))
            circle(self.trail[i][0], self.trail[i][1], 2*r1*i/len(self.trail))
            # circle(self.x, self.y, 2*r1)
        
    def createNext(self):
        return (self.x + self.vel * cos(self.a),
                self.y + self.vel * sin(self.a))
        
    def next(self):
        if not self.alive:
            return
         
        if self.y > m/2 and self.isUp == True:
            self.isUp = False
            self.B[5] = False
        elif self.y < m/2 and self.isUp == False:
            self.isUp= True
            self.A[5] = False
            
        if self.lock != None:
            if self.lock == 'A':
                self.A[1] = (self.A[1] + self.A[2]) % (2*pi)
                r = self.A[0].radii[1]
                theta = self.A[0].angle
                
                self.x = r * cos(self.A[1]) + self.A[0].x
                self.y = r * sin(self.A[1]) + self.A[0].y
                if not (r1 <= self.x < n-r1 and r1 <= self.y < m-r1):
                    self.game.score('B')
                    self.alive = False
                
                self.A[3] = (abs(self.A[1] - 3*pi/2) < theta)
                if self.A[3]: self.A[4] = self.A[3]
                
                if self.A[3] == False and self.A[4] == True:
                    self.lock = None
                    self.A[5] = True
                    if self.A[2] > 0:
                        self.a = theta
                    else:
                        self.a = pi - theta
            elif self.lock == 'B':
                self.B[1] = (self.B[1] + self.B[2]) % (2*pi)
                r = self.B[0].radii[1]
                theta = self.B[0].angle
                
                self.x = r * cos(self.B[1]) + self.B[0].x
                self.y = r * sin(self.B[1]) + self.B[0].y
                if not (r1 <= self.x < n-r1 and r1 <= self.y < m-r1):
                    self.game.score('A')
                    self.alive = False
                
                self.B[3] = (abs(self.B[1] - pi/2) < theta)
                if self.B[3]: self.B[4] = self.B[3]
                
                if self.B[3] == False and self.B[4] == True:
                    self.lock = None
                    self.B[5] = True
                    if self.B[2] > 0:
                        self.a = theta + pi
                    else:
                        self.a = -theta
                    
            return
        
        _ = self.createNext()
        
        # (Puck, Phi, dPhi, isDanger, wasDanger)
        # Vicinity of Puck B
        if self.B[5] == False and (_[0] - self.B[0].x)**2 + (_[1] - self.B[0].y)**2 <= self.B[0].radii[1]**2:
            self.lock = 'B'
            self.B[1] = atan2((self.y - self.B[0].y), self.x - self.B[0].x)
            self.B[2] = (1 if self.x > self.B[0].x else -1) * self.vel_ang
            self.B[3] = False
            self.B[4] = False
            return
        
        # Vicinity of Puck A
        if self.A[5] == False and (_[0] - self.A[0].x)**2 + (_[1] - self.A[0].y)**2 <= self.A[0].radii[1]**2:
            self.lock = 'A'
            self.A[1] = atan2((self.y - self.A[0].y), self.x - self.A[0].x)
            self.A[2] = (-1 if self.x > self.B[0].x else 1) * self.vel_ang
            self.A[3] = False
            self.A[4] = False
            return
                
        # Sides
        if not r1 <= _[0] < n - r1:
            self.a = (-self.a + pi) % (2*pi)
            self.game.Music('bounce')
        
        # Goals
        if -r1*1.5 > _[1]:
            # Up
            self.alive = False    
            self.game.score('B')
            return
        elif m + r1*1.5 < _[1]:
            # Down
            self.alive = False
            self.game.score('A')
            return
            
        self.x, self.y = self.createNext()
        