# Mohamed Abdalla
# ID: 19106978

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import math
import numpy as np

textures = None
sky= (0.0, 1.0, 1.0); grass =(0.3, 1, 0)
circles =[
    ((-420,240), 22, (1.0, 0.9, 0.0)), #sun
    ((470, 40 ), 17, (1.0, 0.0, 0.0)), # red
    ((470,  5 ), 17, (1.0, 1.0, 0.0)), # yellow
    ((470,-30 ), 17, (0.0, 1.0, 0.0)), # green
]
vertices = 100
stop = False; day=True; led=False
x_pos = [0,0] ; x_plane = 0 ; y_plane = 0

def myInit():
    gluOrtho2D(-500, 500, -300, 300)    

def load_textures():

    global textures
    texture_paths = {
        0: "C:/Users/Dell/Downloads/Computer Graphics/Lab/Assignment3/Buildings4.png",
        1: "C:/Users/Dell/Downloads/Computer Graphics/Lab/Assignment3/lights.png",
        2: "C:/Users/Dell/Downloads/Computer Graphics/Lab/Assignment3/Right people (Day).png",
        3: "C:/Users/Dell/Downloads/Computer Graphics/Lab/Assignment3/Left people (Day).png",
        4: "C:/Users/Dell/Downloads/Computer Graphics/Lab/Assignment3/Rocket.png",
        5: "C:/Users/Dell/Downloads/Computer Graphics/Lab/Assignment3/LED.png"
    }
    
    textures = glGenTextures(10)    
    for texture_id, path in texture_paths.items():
        glBindTexture(GL_TEXTURE_2D, textures[texture_id])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image = Image.open(path).convert("RGBA")
        flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = flipped_image.tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, flipped_image.width, flipped_image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glColor3f(*sky) #light Blue color (Sky/Day)
    glRectf(-500, 300 , 500 , 80) #(left,up,right,down)
    
    glColor3f(*grass) #light Green color (Grass/Day)
    glRectf(-500, 80 , 500 , -300)

    glColor3f(0.5, 0.5, 0.5) #light Gray color (Pavment/Traffic light)
    glRectf(-500, -100 , 500 , -300)
    
    glColor3f(0.2, 0.2, 0.2) #Dark Gray color (Road)
    glRectf(-500, -185, 500 , -300)
    
    cloud_move()
        
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 1.0, 1)
    
    for texture_id in range (6):
            
        if day and (texture_id == 1 or texture_id == 4) :
            continue # skip the lights
        y=0    
        if texture_id==2:
            x=x_pos[0]*0.5
        elif texture_id==3:
            x=-x_pos[0]*0.8
        elif texture_id==4:
            x=-x_plane*2.5
            y=y_plane +0.8

        elif texture_id == 5 and not led:
            continue 
                
        if texture_id==2 or texture_id==3 or texture_id == 4:
            glPushMatrix()
            glTranslatef(x,y, 0)    

        glBindTexture(GL_TEXTURE_2D, textures[texture_id])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(-550, -350)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(550, -350)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(550, 350)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(-550, 350)
        glEnd()

        if texture_id==2 or texture_id==3 or texture_id == 4:
            glPopMatrix()
        
    glDisable(GL_TEXTURE_2D)
    
    if not day:
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   
        glColor4f(1,1,.7,.4) # Creamy color
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(-235, -45) # Center point
        for i in range(vertices+1):
            angle = i * 2.0 * math.pi / vertices
            x = -220 + 50 * math.cos(angle)
            y = -160 + 10 * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
    glDisable(GL_BLEND)

    glColor3f(0.5, 0.5, 0.5) #light Gray color (Traffic light)
    glRectf(450, 60 , 490 , -50)

    for Center, Radius, circle_color in circles:
        glColor3f(*circle_color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(Center[0], Center[1])
        for i in range(vertices+1):
            angle = i * 2.0 * math.pi / vertices
            x = Center[0] + Radius * math.cos(angle)
            y = Center[1] + Radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
        
    plane_move()
    
    glLineWidth(10) # Increase line size
    glBegin(GL_LINES)
    glColor3f(0.6, 0.2, 0.1) #Brown color 
    glVertex2f(470, -50) # ^ (Traffic Light's Stick)
    glVertex2f(470, -170) # v

    glColor3f ( 0 , 0 , 0 ) #Black color 
    glVertex2f(-250 , -50 ) # ^ (lantren's Stick)
    glVertex2f(-250 , -170) # v
    glColor3f (1,1,1) # White
    glVertex2f(-235 , -50 ) # ^ (lantren's Lamp)
    glVertex2f(-235 , -80 ) # v
    glEnd()
    
    glBegin(GL_TRIANGLES)
    glColor3f (0 , 0 , 0) #Black color for (lantren's head)
    glVertex2f(-255, -50) #Right point
    glVertex2f(-230, -50) #Left  point
    glVertex2f(-242, -35) #upper point
    glEnd()   
    
    lower_move()
    glutSwapBuffers()
    
def cloud_move():
    if day:
        glPushMatrix()
        glTranslatef(x_pos[0]*0.3,0, 0)    
        ####------Cloud------####    
        Cloud =[
        ####-Right cloud-####
        ((260, 210), 27), # main
        ((235, 210), 20), # left
        ((285, 210), 20), # right
        ####-Left cloud-####
        ((-260, 230), 30), # main
        ((-230, 230), 24), # left
        ((-290, 230), 24) # right
        ]
        for Center, Radius in Cloud:
            glColor3f(1,1, .9) # White
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(Center[0], Center[1])
            for i in range(vertices+1):
                angle = i * 2.0 * math.pi / vertices
                x = Center[0] + Radius * math.cos(angle)
                y = Center[1] + Radius * math.sin(angle)
                glVertex2f(x, y)
            glEnd()
        glPopMatrix()

def plane_move():
    if day:    
        glPushMatrix()
        glTranslatef(x_plane, y_plane, 0.0)
        ####------Plane------####
        glColor3f(1, 0, .1) #red
        glBegin(GL_POLYGON) # Plane
        glVertex2f(135, 255) # (nos fo2)
        glVertex2f(90, 255) #up left(front)
        glVertex2f(60, 240) #down left(front)
        glVertex2f(140, 240) #down right
        glVertex2f(180, 265) #right wing
        glVertex2f(130, 265) #left wing
        glEnd()
        glPopMatrix()
    
def lower_move():    
    glPushMatrix()
    glTranslatef(x_pos[1], 0, 0 )
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if not day: 
        #######---HeadLights---#######
        glColor4f(1,1,.7,.4) ## Creamy
        glBegin(GL_TRIANGLES) 
        ##-BUS-##
        glVertex2f(430, -265) # t7t shmal
        glVertex2f(570, -210) # fo2 ymeen
        glVertex2f(600, -280) # t7t ymeen
        
        glVertex2f(430, -240) # fo2 shmal
        glVertex2f(570, -210) # fo2 ymeen
        glVertex2f(600, -280) # t7t ymeen
        ###############################
        ##-Orange Car-##
        glVertex2f(160, -210) # fo2 ymeen
        glVertex2f(190, -280) # t7t ymeen
        glVertex2f(0, -250) # t7t shmal
        
        glVertex2f(0, -230) # fo2 shmal
        glVertex2f(160, -210) # fo2 ymeen
        glVertex2f(190, -280) # t7t ymeen
        ###############################
        ##-Blue Car-##
        glVertex2f(-265, -230) # fo2 shmal
        glVertex2f(-130, -210) # fo2 ymeen
        glVertex2f(-100, -280) # t7t ymeen

        glVertex2f(-130, -210) # fo2 ymeen
        glVertex2f(-100, -280) # t7t ymeen
        glVertex2f(-265, -250) # t7t shmal
                
        glEnd()
    glDisable(GL_BLEND)
    
    ####------Bus------####
    glBegin(GL_POLYGON)
    glColor3f(0.5, 0, 0.7) # Purple
    glVertex2f(410, -120) # fo2 ymeen
    glVertex2f(150, -120) # fo2 shmal
    glColor3f ( 1, .5, .6) ## color
    glVertex2f(150, -270) # t7t shmal
    glVertex2f(450, -270) # t7t ymeen  
    glColor3f(0.5, 0, 0.7) # Purple
    glVertex2f(450, -180) # nos ymeen
    glEnd()
    #################################
    glBegin(GL_POLYGON) # BUS's window
    glColor3f ( 1, 1, .9) # White
    glVertex2f(400, -125) # fo2 ymeen
    glVertex2f(160, -125) # fo2 shmal
    glVertex2f(160, -180) # t7t shmal
    glVertex2f(440, -180) # t7t ymeen 
    glEnd()    
    
    ####------Orange Car------####
    glBegin(GL_POLYGON)
    glColor3f (1,0.3, 0.2) # Pale Orange
    glVertex2f(-30 , -200) # nos ymeen
    glVertex2f(-50 , -140) # fo2 ymeen
    glVertex2f(-130, -140) # fo2 shmal
    glVertex2f(-180, -200) # nos shmal (back)
    glColor3f ( .5, .2, 1) ## color
    glVertex2f(-180, -265) # t7t shmal
    glVertex2f( 20 , -265) # t7t ymeen  
    glColor3f (1,0.3, 0.2) # Pale Orange
    glVertex2f( 20 , -210) # nos ymeen (front)
    glEnd()
    #################################
    glBegin(GL_POLYGON) # Orange Car's window
    glColor3f ( 0 , 0 , 0) # Black
    glVertex2f(-40 , -200) # nos ymeen
    glVertex2f(-55 , -150) # fo2 ymeen
    glVertex2f(-128, -150) # fo2 shmal
    glVertex2f(-170, -200) # nos shmal (back)   
    glEnd()

    ####------Blue Car------####    
    glBegin(GL_POLYGON)
    glColor3f ( .1, .2, 1) # Blue
    glVertex2f(-290, -200) # nos ymeen
    glVertex2f(-320, -155) # fo2 ymeen
    glVertex2f(-410, -155) # fo2 shmal
    glVertex2f(-440, -200) # nos shmal
    glVertex2f(-480, -205) # nos shmal (back)
    glColor3f ( .4, .8, .5) ## color
    glVertex2f(-490, -260) # t7t shmal 
    glVertex2f(-240, -260) # t7t ymeen 
    glColor3f ( .1, .2, 1) # Blue
    glVertex2f(-240, -210) # nos ymeen (front)
    glEnd()
    #################################
    glBegin(GL_POLYGON) ## Blue Car's Window
    glColor3f ( 0 , 0 , 0) # Black
    glVertex2f(-300, -200) # nos ymeen
    glVertex2f(-325, -160) # fo2 ymeen
    glVertex2f(-405, -160) # fo2 shmal
    glVertex2f(-430, -200) # nos shmal
    glEnd()
    
    Tyres =[
    ####-Blue car-####
    ((-300, -260), 20) , ((-420, -260), 20),
    ####-Orange car-####
    ((-30 , -265), 20) , ((-130, -265), 20),
    ####-Purple Bus-####
    (( 370, -270), 25) , (( 230, -270), 25)
    ]
    for Center, Radius in Tyres:
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(Center[0], Center[1])
        for i in range(vertices+1):
            angle = i * 2.0 * math.pi / vertices
            x = Center[0] + Radius * math.cos(angle)
            y = Center[1] + Radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
    glPopMatrix()

def update_move():
    global x_pos, x_plane, y_plane

    if not stop: 
        x_pos[1] += 2.5  # for cars
        if x_pos[1] >= 1000:
            x_pos[1] = -950 # Reset the position to the left edge of the window

    x_pos[0] += 1 # for clouds
    if x_pos[0] >=1000 :
        x_pos[0] = -950  #Reset position of cars & clouds to the left edge of the window
    
    x_plane -= 0.8 # for plane
    y_plane += 0.03
    if x_plane<=-720 or y_plane>= 100:
        x_plane = 500
        y_plane = -60 #Reset position of the plane on window
    
    glutPostRedisplay()    
    
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(1000, 700)
glutInitWindowPosition(200, 20)
glutCreateWindow("CITY DESIGN")

myInit()
glutDisplayFunc(display)
glutIdleFunc(update_move) 
load_textures()

def keyboard(key, x, y):
    global sky, grass, stop, day,led
    if key == b'r':
        circles[1] =((470, 40), 17, (1.0, 0.0, 0.0)) # red
        circles[3] =((470, -30), 17, (0, 0.1, 0)) # Black
        stop= True
    elif key == b'g':
        circles[1] =((470, 40), 17, (0.2, 0, 0)) # Black
        circles[3] =((470, -30), 17, (0.0, 1.0, 0.0)) # green
        stop= False
    elif key == b'b':
        circles[0] =((-420, 240), 28, (1.0, 0.9, 1.0)) # moon
        sky=(0.0, 0.0, 0.3) ; grass=(0.3, 0.6, 0)
        day = False
    elif key == b'w':
        circles[0] =((-420, 240), 22, (1.0, 0.9, 0.0)) # sun
        sky=(0.0, 1.0 , 1.0) ; grass=(0.3,   1, 0)
        day = True
    elif key == b'+':
        led=True
    elif key == b'-':
        led=False

    glutPostRedisplay()

glutKeyboardFunc(keyboard)
glutMainLoop()