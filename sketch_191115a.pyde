from math import cos, sin, pi

n, m = 400, 600
r1 = 10
r2 = 3*r1
theta = 0

ball_p = [n/2, m/2]
ball_v = pi/4
ball_s = 1.5

def drawOutline():
    # (r,r)        (n-r, r)
    # (r, m/2-r)   (n-r, m/2-r)
    line(r2, r2, n-r2, r2)
    line(r2, r2, r1, m/2-r1)
    line(n-r1, m/2-r1, n-r2, r2)
    line(n-r1, m/2-r1, r1, m/2-r1)
         
    # (r, m/2+r)   (n-r, m/2+r)
    # (r, m-r)   (n-r, m-r)
    line(r1, m/2+r1, n-r1, m/2+r1)
    line(r1, m/2+r1, r2, m-r2)
    line(n-r2, m-r2, n-r1, m/2+r1)
    line(n-r2, m-r2, r2, m-r2)

class Puck:
    def __init__(narrowPoint, widePoint, eventsKeys):
        pass
    

        
        

def setup():
    size(n, m)
    frameRate(200)
    # noCursor()


def draw():
    global r, theta, ball_v
    # theta += 0.01
    background(255)
    
    # Model Ball
    ball_p[0] += ball_s * cos(ball_v) 
    ball_p[1] += ball_s * sin(ball_v)
    
    if not r1 < ball_p[0] < n - r1:
        ball_v *= -1
        ball_v += pi
        ball_v %= 2*pi
    if not r1 < ball_p[1] < m - r1:
        ball_v *= -1
        ball_v %= 2*pi
    
    circle(ball_p[0], ball_p[1], 2*r1)
    
    
    strokeWeight(3)
    line(0, m/2, n, m/2)
    
    strokeWeight(1)
    fill(0)
    ratio = (abs(mouseY - m/2 - r1) if mouseY > m/2 + r1 else 0) / (m/2.0 - r1 - r2) # Why 2.0 works while 2 does not
    ratio = (ratio if ratio <= 1 else 1)
    r = r1 + ratio * (r2-r1)


    x, y = None, None
    
    # r, n-r
    if mouseX < r:
        x = r
    elif mouseX > n-r:
        x = n-r
    else:
        x = mouseX
        
    if mouseY < m/2 + r:
        y = m/2 + r
        fill(255, 0, 0)
    elif mouseY > m - r:
        y = m - r
        fill(255, 255, 0)
    else:
        y = mouseY
        fill(255, 0, 255)
    circle(x, y, 2*r)
    noFill()

    R = r + r1 * (1+ratio)
    circle(x, y, 2*R)

    # circle(x+cos(theta)*R, y+sin(theta)*R , 2*r1)
    drawOutline()
    

 
