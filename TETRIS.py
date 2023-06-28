import pygame
import random
class shapes (object):
    #A normal grid is like :
    #[[0, 1, 2, 3 ],
     #[4, 5, 6, 7 ],
     #[8, 9 ,10,11],
     #[12,13,14,15]] 
    
    I=[[1, 5, 9, 13], [4, 5, 6, 7]]
    O=[[1, 2, 5, 6]]
    Z=[[0, 1, 5, 6], [1, 4, 5, 8]]
    S=[[1, 2, 4, 5], [1, 5, 6, 10]]
    L=[[1, 2, 6, 10], [2, 4, 5, 6], [1, 5, 9, 10], [4, 5, 6, 8]]
    J=[[1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8], [0, 4, 5, 6]]
    T=[[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]]
       
    shapeTypes=[J,O,Z,S,I,L,T]
    colors=[(0,0,255),(225,254,32),(255,0,0),(0,255,0),(80,208,255),(255,160,16),(160,32,255)]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.types = random.randint(0, len(self.shapeTypes) - 1)
        self.color = self.colors[self.types]
        self.rotation = 0 
        self.visible = True
        
        
    def state(self):
        return self.shapeTypes[self.types][self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapeTypes[self.types]) 
        
    def dontRotate(self):
        self.rotation = (self.rotation - 1) % len(self.shapeTypes[self.types]) 
    
def display():
    win.fill((0,0,0))

def setPar(fullScreen=False):
    pygame.display.init()
    global win
    if fullScreen:
       win=pygame.display.set_mode((width,height), pygame.FULLSCREEN)
    else:
        win=pygame.display.set_mode((width,height))
    pygame.display.set_caption("TETRIS")

    
def gridd():
    rct=pygame.Rect((50,0),(200,75))
    pygame.draw.rect(win,(0,0,0),rct)      
    for i in range(11):
        pygame.draw.line(win,(225,225,225),(50+i*20,75),(50+i*20,475),1)   
    for i in range(21):
        pygame.draw.line(win,(225,225,225),(50,75+i*20),(250,75+i*20),1) 

def drawShape(shape,x,y):
    for i in range(4):
        for j in range(4):
            p = i * 4 + j
            if p in shape.state():
                rct=pygame.Rect((x+j*20,y+i*20),(20,20))
                pygame.draw.rect(win, shape.color,rct)     
                
def drawColoredGrid(grid):
    for i in range(20):
        for j in range(10):
            rct=pygame.Rect((50+j*20,75+i*20),(20,20))
            pygame.draw.rect(win,grid[i][j],rct) 
            
def touching (shape,grid,x,y):
    for i in shape.state():
        if grid[(-76+y)//20+i//4][(x-70)//20+i%4+1]!=(0,0,0):# or grid[(-76+y)//20+1][(x-50)//20+i%4]!=(0,0,0):
            return True
    return False

def fixate(shape, grid, x, y):
    for i in shape.state():
        grid[(-76+y)//20+i//4-1][(x-50)//20+i%4]=shape.color   

def drop(shape, grid,x,y):
    pass    
        
def checkLeft(shape, x, y):
    for i in shape.state():
        if x+(i%4)*20<=50 or grid[(-76+y)//20+i//4][(x-70)//20+i%4]!=(0,0,0):
            return False
    return True

def checkRight(shape, x, y):
    for i in shape.state():
        if x+(i%4)*20>=230:
            return False
        if grid[(-76+y)//20+i//4][(x-70)//20+i%4+2]!=(0,0,0):
            return False
    return True

def checkLine(grid):
    l=[]
    for i in range(19,2,-1):
        if ((0,0,0) in grid[i])==False:
            l.append(i)
        elif grid[i]==[(0,0,0)]*10:
            break
        try:
            if l[0]-i>4:
                break
        except:
            continue
    return(l)

def clearLines(grid,l):
    n=0
    for i in l: 
        grid.pop(i+n)
        grid.insert(0,[(0,0,0)]*10)
        n+=1
        
def lost(grid):
    for i in grid[20::]:
        if i!=[(0,0,0)]*10:
            return True
    return False
    
def displayText(textToShow, xy, color, size, center,secondC=(0,0,0)):
    pygame.init()
    font = pygame.font.SysFont('comicsans', size)
    text = font.render(textToShow,True,color,secondC)
    if center:
        textRect = text.get_rect()
        textRect.center = xy
        win.blit(text,textRect)
    else:
        win.blit(text,xy)

def getHighscore():
    file=open("Data/"+'scores.txt','r')
    n=int(file.readline())
    file.close()
    return n

def setHighscore(score):
    file=open("Data/"+'scores.txt','w')
    file.write(str(score))
    file.close()

def game(level=0):
    highScore=getHighscore()
    score=0    
    black=(0,0,0)
    global grid
    grid=[[black for _ in range(10)] for _ in range(20)]
    grid+=[[black for _ in range(10)] for _ in range(4)]
    velocity=20
    x,initx = 110,110
    y,inity = 76,56
    fall=True
    clock=pygame.time.Clock()
    run=True
    pause=False
    Lost=False
    losCount=0
    currentShape=shapes(x,y)
    nextShape= shapes(x,y)
    speed=0
    sensitivity=0
    fallTime=0.25-level*0.03
    while run:
        display()
        pygame.draw.line(win,(225,225,225),(width//3*2,0),(width//3*2,height),10)   
        rct=pygame.Rect((30,73),(240,420))
        pygame.draw.rect(win,(60,60,60),rct)           
        drawColoredGrid(grid)
        #level=(score//50)/2+1
        
        displayText('Next ',(width//7*5,height//16),(128,128,128),60,False)        
        displayText('Score: ',(width//7*5,height//16*9),(255,128,128),30,False)
        displayText(str(score),(width//7*6,height//16*11),(255,225,255),40,True)
        displayText('High score: ',(width//7*5,height//8*6),(255,128,128),30,False)
        displayText(str(highScore),(width//7*6,height//8*7),(255,225,255),40,True)        
        
        if level==0:
            displayText('Easy',(width//7*6,height//16*8),(50,255,50),30,True)
        elif level==1:
            displayText('Meduim',(width//7*6,height//2),(0,100,255),30,True)
        elif level==2:
            displayText('Hard',(width//7*6,height//2),(200,100,0),30,True)          
        
        rawtime=clock.get_rawtime()
        if not pause:
            speed+=rawtime
            sensitivity+=rawtime
        clock.tick()
        
        if not (fall or Lost) :
            nextShape= shapes(x,y)
            fall=True
            
        drawShape(nextShape, width//6*5-40,height//16*5-20)
        drawShape(currentShape, x, y)
            
        keys= pygame.key.get_pressed()
       
        if fall: 
            if speed/1000>fallTime:
                speed=0
                y+=velocity
                if y+(currentShape.state()[-1]*5)>475 or touching(currentShape,grid,x,y):
                    fixate(currentShape,grid,x,y)
                    l=checkLine(grid)
                    score+=10*len(l)*(level+1)
                    score+=level+1  
                    
                    clearLines(grid,l)
                    if lost(grid):
                        pause=True
                        Lost=True
                    x,y=initx,inity-(nextShape.state()[-1]//4)*20
                    currentShape=nextShape
                    fall=False  
                    
            if sensitivity/1000>0.1:#-level*0.01:   
                sensitivity=0
                if keys[pygame.K_LEFT]:
                    if checkLeft(currentShape,x,y):
                        x-=velocity
                if keys[pygame.K_RIGHT]:
                    if checkRight(currentShape,x,y):
                        x+=velocity
                if keys[pygame.K_DOWN]:
                    if not(y+(currentShape.state()[-1]*5)>=456 or touching(currentShape,grid,x,y-20)):
                        y=min(y+velocity,456)
                        if y+(currentShape.state()[-1]*5)>475 or touching(currentShape,grid,x,y):
                            y-=20
                
                if keys[pygame.K_UP]:# and fallCount%2==0:
                    currentShape.rotate()
                    if not(checkRight(currentShape,x-20,y) and checkLeft(currentShape,x+20,y)):
                        currentShape.dontRotate()
                        
                if keys[pygame.K_SPACE]and y>=60:
                    while y+(currentShape.state()[-1]*5)<=455 and  not touching(currentShape,grid,x,y+20):
                        y+=20
                    
                if keys[pygame.K_ESCAPE]:
                    # pause=True
                    run=gameMenu()
        if not run:
            break
                    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()     
                quit()
        gridd()   
        if Lost:
            losCount+=rawtime
            displayText('Game Over',(width//2,height//2),(255,225,255),100,True) 
            if losCount>=1500:
                run=False
        pygame.display.update()
        
    if score>highScore:
        setHighscore(score)
            
    if Lost:
        home()
    elif menu and not run:
        mainMenu(level)    

def mainMenu(level=0,pause=False):
    background=pygame.image.load("Data/"+'wall.jpg')    
    background = pygame.transform.scale(background, (600, 350))
    clock=pygame.time.Clock()
    black=(0,0,0)
    shade=(100,100,100)
    global menu
    menu=True
    pos=0
    sensitivity=0
    while menu:
        display()
        rawtime=clock.get_rawtime()
        sensitivity+=rawtime        
        clock.tick()
        l=[black]*3
        l[pos]=shade
        win.blit(background, (0,-20))  
        displayText('Made by Mohamed Krichen',(width//2,height-40),(60,60,60),20,False)
        displayText('Start a new game',(width//2,height//6*3),(0,200,200),40,True,l[0])
        displayText('Difficulity:',(width//5*2,height//6*4),(0,200,200),40,True,l[1])
        displayText('Exit',(width//2,height//6*5),(200,0,0),40,True,l[2])
        if level==0:
            displayText('Easy',(width//4*3,height//6*4),(50,255,50),30,True)
        elif level==1:
            displayText('Meduim',(width//4*3,height//6*4),(0,100,255),30,True)
        elif level==2:
            displayText('Hard',(width//4*3,height//6*4),(200,100,0),30,True)   
            
        keys= pygame.key.get_pressed()
        if sensitivity/1000>0.12:   
            sensitivity=0        
            if keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]:
                pos=(pos+1)%len(l)
                
            if keys[pygame.K_UP] or keys[pygame.K_LEFT]:
                pos=(pos-1)%len(l)   
                
            if keys[pygame.K_RETURN] and pos==0:#new game
                menu=False
                game(level)
            
            if keys[pygame.K_RETURN] and pos==1:
                level=(level+1)%3
                
            if keys[pygame.K_RETURN] and pos==2:
                pygame.quit()     
                quit()      
            
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()     
                quit()
        
        pygame.display.update()

def gameMenu():
    clock=pygame.time.Clock()
    black=(0,0,0)
    shade=(100,100,100)
    gmenu=True
    l=[black]*2
    pos=0
    sensitivity=0
    while gmenu: 
        display()
        rawtime=clock.get_rawtime()
        sensitivity+=rawtime        
        clock.tick()
        l=[black]*2
        l[pos]=shade
        displayText('Continue',(width//2,height//2-30),(0,200,200),40,True,l[0])
        displayText('Back to main menu',(width//2,height//2+30),(0,200,200),40,True,l[1])
        keys= pygame.key.get_pressed()
        if sensitivity/1000>0.12:   
            sensitivity=0        
            if keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]:
                pos=(pos+1)%len(l)
                
            if keys[pygame.K_UP] or keys[pygame.K_LEFT]:
                pos=(pos-1)%len(l)   
                
            if keys[pygame.K_RETURN] and pos==0:#continue
                return True
            
            if keys[pygame.K_RETURN] and pos==1:
                return False                     
            
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()     
                quit()
        
        pygame.display.update()    
    
def home():
    clock = pygame.time.Clock()
    home=True
    while home:
        display()
        displayText('Press any key to start',(width//2,height//2),(155,155,155),50,True)  
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()     
                quit()
            if event.type == pygame.KEYDOWN:
                home=False
                # mainMenu()
        
        pygame.display.update() 
        # clock.tick(10)


width,height=600,600
fullScreen=False
setPar(fullScreen)
home()
while True:
    mainMenu()

