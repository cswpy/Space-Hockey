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
        circle(self.x, self.y, 2*_[0])
                
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