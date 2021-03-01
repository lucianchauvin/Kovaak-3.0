#### Made by Lucian Chauvin (dont take my code and say its yours cunt)####
####                       lucianchauvin@gmail.com                    ####

from tkinter import*
import random, math, pyglet

with open('settings.txt') as f:
    data = f.read()
    data = data.split("\n")
    for x in range(len(data)):
        data[x] = data[x].split(' ')

count = 0
smulti = float(data[0][1])
radius = int(data[1][1])
bgc = data[2][1]
lc = data[3][1]
tc = data[4][1]
soundf = data[5][1]
vol = float(data[6][1])
linestat = data[7][1] == 'True'
linestatdashed = data[8][1] == 'True'
fullscreen = data[9][1] == 'True'


game = Tk()
game.title("Kovaak 3.0 - Made by Lucian Chauvin")
icon = PhotoImage(file="crosshairs/plus.png")
game.iconphoto(False, icon)
if fullscreen:
    width = game.winfo_screenwidth()
    height = game.winfo_screenheight()
else:
    width = int(data[10][1])
    height = int(data[10][2])
game.resizable(0, 0)
game.wm_attributes('-fullscreen',fullscreen)
game.minsize(width,height)

crossimage = PhotoImage(file=data[11][1])

class Circle():
    def __init__(self):
        self.pos  = [random.randint(15,width-15),random.randint(15,height-15)]
        self.circle = c.create_oval(self.pos[0]-radius, self.pos[1]+radius,self.pos[0]+radius,
                                    self.pos[1]-radius, fill=tc, tag='target')
    def move(self,dmxy):
        self.pos = [self.pos[0]+dmxy[0],self.pos[1]+dmxy[1]]
        c.delete(self.circle)
        self.circle = c.create_oval(self.pos[0] - radius, self.pos[1] + radius, self.pos[0] + radius,
                                    self.pos[1] - radius, fill=tc, tag='target')

def motion(event):
    if linestat:
        if linestatdashed:
            c.delete(line[0])
            l = c.create_line(width / 2, height / 2, clist[0].pos[0], clist[0].pos[1], fill=lc, dash=True,
                              tag='target')
            line[0] = l
        else:
            c.delete(line[0])
            l = c.create_line(width/2,height/2, clist[0].pos[0],clist[0].pos[1], fill=lc, tag='target')
            line[0] = l
    global mxy
    mxy = ()

    mxy = [event.x, event.y]
    dmxy = [((width/2)-mxy[0])*smulti,((height/2)-mxy[1])*smulti]

    for x in clist:
        x.move(dmxy)

    if mxy[0] != width/2 or mxy[1] != height/2:
        game.event_generate('<Motion>', warp=True, x=(width/2), y=(height/2))

    c.tag_raise(crosshair)


def click(event):
    global count, countt
    for x in clist:
        if math.sqrt((((width/2)-x.pos[0])**2)+(((height/2)-x.pos[1])**2)) < radius:
            sound()
            count +=1
            c.delete(countt)
            countt = c.create_text(20+(10*(len(str(count))-1)), 20, fill=tc, font='Times 20 bold', text=str(count))
            clist.remove(x)
            for y in c.find_withtag("target"):
                c.delete(y)
            clist.append(Circle())
            c.update()
            if linestat:
                if linestatdashed:
                    c.delete(line[0])
                    l = c.create_line(width / 2, height / 2, clist[0].pos[0], clist[0].pos[1], fill=lc, dash=True,
                                      tag='target')
                    line[0] = l
                else:
                    c.delete(line[0])
                    l = c.create_line(width / 2, height / 2, clist[0].pos[0], clist[0].pos[1], fill=lc, tag='target')
                    line[0] = l
                c.tag_lower(line[0])

def sound():
    splayer = pyglet.media.Player()
    s = pyglet.media.load(soundf)
    splayer.queue(s)
    splayer.volume=vol
    splayer.play()

def destory(event):
    game.destroy()

c = Canvas(game, bg=bgc,height=height,width=width,cursor="none")
c.pack()
countt = c.create_text(20+(10*(len(str(count))-1)),20,fill=tc, font='Times 20 bold', text=str(count))

crosshair = c.create_image(width/2, height/2, image=crossimage)

clist = []
line = []
mxy = (width/2, height/2)

clist.append(Circle())
if linestat:
    if linestatdashed:
        l = c.create_line(width / 2, height / 2, clist[0].pos[0], clist[0].pos[1], fill=lc, dash=True,
                          tag='target')
        line.append(l)
    else:
        l = c.create_line(width / 2, height / 2, clist[0].pos[0], clist[0].pos[1], fill=lc, tag='target')
        line.append(l)
    c.tag_lower(line[0])

game.bind('<Motion>', motion)
game.bind('<1>', click)
game.bind('<Escape>', destory)

game.mainloop()
