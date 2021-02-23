import tkinter as tk
import random
import math

class snake:
    """Snake Class"""

    def __init__(self,framesize=200, startlength =3,sspeed = 100,sinc=2):
        self.framesz = framesize
        self.score = 0
        self.insz = startlength 
        self.startxy = [100,100]
        self.bcrash = False
        self.alive = False
        self.speed = sspeed #update time
        self.tinc = sinc
        self.rectangles = []
        self.turns = []
        self.tstsz = 2
        self.add = False
        self.ss=(10,10)
        self.sz =10
        self.sn = []
        self.snt = []
        self.l=len(self.sn)
        self.dir = "u"
        self.root =tk.Tk()
        self.root.title("Python")
        self.lscore = tk.StringVar()
        self.lscore.set("Score: 0 Speed:"+str(self.speed))
        self.frame = tk.Canvas(self.root, width=self.framesz , height= self.framesz, bg = 'white')
        self.frame.bind("<Up>", self.up)
        self.frame.bind("<Down>", self.down)
        self.frame.bind("<Right>", self.right)
        self.frame.bind("<Left>", self.left)
        self.frame.bind("<space>", self.space)
        self.frame.bind("<Escape>", self.esc)
        self.frame.bind("<Button-1>", self.callback)
        self.frame.pack()
        self.lbl_score= tk.Label(self.root,textvariable = self.lscore)
        self.lbl_score.pack()
        self.__spawn()
        self.root.mainloop()

    def __spawn(self):
        
        for n in range(self.insz):
            self.sn.append([self.startxy[0],self.startxy[1]+self.ss[1]*n])

        for item in self.sn:
            self.rectangles.append(self.frame.create_rectangle(item[0],item[1],item[0]+self.sz,item[1]+self.sz,fill = 'green',outline='black'))
        #while (self.sn.count([self.fx,self.fy]) != 0):
        self.fx,self.fy = math.ceil(random.randint(self.sz,self.framesz-self.sz)/self.sz)*self.sz,math.ceil(random.randint(self.sz,self.framesz-self.sz)/self.sz)*self.sz
        self.food = self.frame.create_oval(self.fx,self.fy,self.fx+self.sz,self.fy+self.sz,fill = 'red') 
        self.__step()
        self.frame.focus_set()

    def __food(self):
        """Spawn Food"""
        while (self.sn.count([self.fx,self.fy]) != 0):
            self.fx,self.fy = math.ceil(random.randint(self.sz,self.framesz-self.sz)/self.sz)*self.sz,math.ceil(random.randint(self.sz,self.framesz-self.sz)/self.sz)*self.sz
        self.frame.coords(self.food, self.fx,self.fy,self.fx+self.sz,self.fy+self.sz)       

    
    def __step(self):
        if self.alive:
            self.snt= [x[:] for x in self.sn] #DeepCopy list
            
            if len(self.turns) > 0:
                if self.turns[0] == "u" and self.dir != "d":
                    self.dir = self.turns[0]
                if self.turns[0] == "d" and self.dir != "u":
                    self.dir = self.turns[0]
                if self.turns[0] == "l" and self.dir != "r":
                    self.dir = self.turns[0]
                if self.turns[0] == "r" and self.dir != "l":
                    self.dir = self.turns[0]
                self.turns.pop(0)

            if not self.add:
                self.snt.pop()
            else:
                if len(self.rectangles) %2 ==0:
                    self.rectangles.append(self.frame.create_rectangle(self.snt[-1][0],self.snt[-1][1],self.snt[-1][0]+self.sz,self.snt[-1][1]+self.sz,fill = 'black',outline='blue'))
                else:
                    self.rectangles.append(self.frame.create_rectangle(self.snt[-1][0],self.snt[-1][1],self.snt[-1][0]+self.sz,self.snt[-1][1]+self.sz,fill = 'black',outline='green'))
                if self.speed > 10:
                    self.speed -= self.tinc
                self.score += 1
                self.lscore.set("Score: {} Speed: {}".format(str(self.score),str(self.speed)))
                self.add = False
                
                    
            if self.dir =="r":
                if self.bcrash:
                    pass
                
                if self.sn[0][0] == self.framesz - self.sz:
                    self.sn[0][0] = 0
                else:
                    self.sn[0][0] += self.ss[0]
            if self.dir =="l":
                if self.sn[0][0] == 0:
                        self.sn[0][0] = self.framesz - self.sz
                else:
                    self.sn[0][0] -= self.ss[0]              
            if self.dir == "u":
                if self.sn[0][1] == 0:
                    self.sn[0][1] = self.framesz - self.sz
                else:   
                    self.sn[0][1] -= self.ss[1]
            if self.dir == "d":
                if self.sn[0][1] == self.framesz - self.sz:
                    self.sn[0][1] = 0
                else:   
                    self.sn[0][1] += self.ss[1]

            self.sn[1:]= self.snt[0:]

            for idx,item in enumerate(self.rectangles):
                self.frame.coords(item,self.sn[idx][0],self.sn[idx][1],self.sn[idx][0]+self.sz,self.sn[idx][1]+self.sz)#(self.rectangles[0],0,self.ss[1]*-1)

            collision = self.sn.count(self.sn[0])
            food = self.sn.count([self.fx,self.fy])
            if food > 0:
                self.__food()
                self.add= True
            if collision > 1:
                self.alive = False
                self.lscore.set("Crashed! Score: {}".format(str(self.score)))
                #print("Crashed")  
        
        
            #self.frame.coords(self.rectangles[0],50,50,200,200)#(self.rectangles[0],0,self.ss[1]*-1)
        self.root.after(self.speed, self.__step)

    def up(self,event):
        if ((self.dir != "u")) and  (len(self.turns) < self.tstsz):
            self.turns.append("u")       
    def down(self,event):
        if ((self.dir != "d")) and (len(self.turns) < self.tstsz):
            self.turns.append("d") 
    def right(self,event):
        if ((self.dir != "r"))  and (len(self.turns) < self.tstsz):
            self.turns.append("r") 
    def left(self,event):
        if ((self.dir != "l"))  and (len(self.turns) < self.tstsz):
            self.turns.append("l")
    def space(self,event):
        #self.__spawn()
        if self.alive:
            self.alive = False
        else:
            self.alive = True
    def esc(self,event):
        self.sn.clear()
        self.rectangles.clear()
        self.__spawn()

    def callback(self,event):
        self.frame.focus_set()
        #self.add =True
        #self.step()
        #print("clicked at", event.x, event.y)



snake = snake(framesize=250,sinc=1)

