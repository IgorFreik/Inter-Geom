from tkinter import *
 
class Point():
    def __init__(self, x1, y1):
        self.x = x1
        self.y = y1
    def dist(self, p):
        return ((self.x - p.x) ** 2 + (self.y - p.y) ** 2) ** (1 / 2)
 
 
class Line():
    def __init__(self, p1, p2):
        self.a = (p1.y - p2.y) / (p1.x - p2.x);
        self.b = -p2.x * (p1.y - p2.y) / (p1.x - p2.x) + p2.y
    def dist(self, p):
        return abs(self.a * p.x - p.y +self.b) / ((self.a*self.a + 1)**(1/2))        
 
 
 
 
class Segment():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.l = Line(p1, p2)
    def dist(self, p):
        dd = (-self.l.a * p.x + p.y - self.l.b) 
        p = Point((self.l.a*dd)/(self.l.a*self.l.a+1)+p.x, (self.l.a*dd)/(self.l.a*self.l.a+1)+p.y)
        print(p.x, p.y)
        if (p.x <= max(self.p1.x, self.p2.x) and p.x >= min(self.p1.x, self.p2.x)):
            if (p.y <= max(self.p1.y, self.p2.y) and p.y >= min(self.p1.y, self.p2.y)):
                return self.l.dist(p)
        return min(p.dist(self.p1), p.dist(self.p2))
 
class Circle():
    def __init__(self, p1, r1):
        self.p = p1
        self.r = r1
    def dist(self, p):
        return abs(((p.x - self.p.x)*(p.x - self.p.x) + (p.y - self.p.y)*(p.y - self.p.y))**(1/2) - self.r)
 
 
def cw(a, b, c):
    return a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y) < 0
 
def cmp(a):
    return [a.x, a.y]
 
def ccw(a, b, c):
    return a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y) > 0
 
 
 
class Geoma(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
 
        self.parent = parent
        self.color = "blue"
        self.width = 4
        self.stack = []
        self.marked = []
        self.h = []
        self.r = []
        self.setUI()
 
 
    def marked_point(self, p, col):
        self.canv.create_oval(p.x - self.width,
                              p.y - self.width,
                              p.x + self.width,
                              p.y + self.width,
                              fill=col, outline=col)
 
    def marked_segment(self, seg, col):
        self.canv.create_line(seg.p1.x, seg.p1.y, seg.p2.x, seg.p2.y, 
	                      width = self.width, fill = col)
 
    def marked_line(self, l, col):
        p1 = Point(0, l.b)
        p2 = Point(1920, 1920 * l.a + l.b)
        self.canv.create_line(p1.x, p1.y, p2.x, p2.y, 
                                width = self.width, fill = col)    
 
    def marked_circle(self, c, col):
        self.canv.create_oval(c.p.x - c.r, 
                              c.p.y - c.r, 
                              c.p.x + c.r, 
                              c.p.y + c.r, 
                              fill="", outline=col, width=5)
 
 
 
    def draw(self, event):
        self.h.append(["draw", event])
        p = Point(event.x, event.y)
        self.stack.append(p)
        self.marked_point(p, self.color)
 
 
    def mark(self, event):
        self.h.append(["mark", event])
        ev = Point(event.x, event.y)
        for ind in range(len(self.marked)):
            i = self.marked[ind]
            if (i.dist(ev) < 5):
                if (type(i) == Point):
                    self.marked_point(i, self.color)
                if (type(i) == Circle):
                    self.marked_circle(i, "black")
                if (type(i) == Line):
                    self.marked_line(i, self.color)
                if (type(i) == Segment):
                    self.marked_segment(i, self.color)
                self.stack.append(i) 
                self.marked.pop(ind)
                return
        for ind in range(len(self.stack)):
            i = self.stack[ind]
            if (i.dist(ev) < 10):
                if (type(i) == Point):
                    self.marked_point(i, "red")
                if (type(i) == Circle):
                    self.marked_circle(i, "red")
                if (type(i) == Line):
                    self.marked_line(i, "red")
                if (type(i) == Segment):
                    self.marked_segment(i, "red")
                self.marked.append(i)
                self.stack.pop(ind)                
                return
 
 
    def clear_marked(self):
        self.h.append(["clear_marked"])
        for i in self.marked:
            if (type(i) == Point):
                self.marked_point(i, self.color)
            if (type(i) == Circle):
                self.marked_circle(i, "black")
            if (type(i) == Line):
                self.marked_line(i, self.color)
            if (type(i) == Segment):
                self.marked_segment(i, self.color)
            self.stack.append(i)
 
        self.marked.clear()
 
    def clear_marked1(self):
        for i in self.marked:
            if (type(i) == Point):
                self.marked_point(i, self.color)
            if (type(i) == Circle):
                self.marked_circle(i, "black")
            if (type(i) == Line):
                self.marked_line(i, self.color)
            if (type(i) == Segment):
                self.marked_segment(i, self.color)
            self.stack.append(i)
        self.marked.clear()    
 
 
    def segment(self):
        pp = []
        for i in self.marked:
            if (type(i) == Point):
                pp.append(i)
        if (len(pp) <= 1):
            self.clear_marked1()
            return
        self.h.append(["segment"])
        pp.sort(key = cmp)
        p1 = pp[0]
        p2 = pp[-1]
        up = []
        down = []
        up.append(p1)
        down.append(p1)
        for i in range(1, len(pp)):
            if ((i == len(pp) - 1) or cw(p1, pp[i], p2)):
                while (len(up) >= 2 and not cw(up[-2], up[-1], pp[i])):
                    up.pop()
                up.append(pp[i])
            if (i == len(pp) - 1 or ccw(p1, pp[i], p2)):
                while (len(down) >= 2 and not ccw(down[-2], down[-1], pp[i])):
                    down.pop()
                down.append(pp[i])	
        curr = up[0]
        for i in range(1, len(up)):
            s = Segment(curr, up[i])
            self.marked_segment(s, self.color)
            self.stack.append(s)
            curr = up[i]
        for i in range(len(down) - 2, -1, -1):
            s = Segment(curr, down[i])
            self.marked_segment(s, self.color)
            self.stack.append(s)
            curr = down[i]
        self.clear_marked1()
 
    def circle(self):
        pp = []
        for i in self.marked:
            if (type(i) == Point):
                pp.append(i)
        if (len(pp) == 2):
            self.h.append(["circle"])
            a_x = pp[0].x
            a_y = pp[0].y
            b_x = pp[1].x
            b_y = pp[1].y
            x = (a_x + b_x) // 2
            y = (a_y + b_y) // 2            
            r = int(((a_x - x) * (a_x - x) + (a_y - y) * (a_y - y)) ** (1 / 2))
            p = Point(x, y)            
            c = Circle(p, r)
            self.marked_circle(c, "Black")
            self.marked.append(c)
 
        elif (len(pp) >= 3):
            self.h.append(["circle"])
            min_r = 10**10
            xx = -1
            yy = -1
            for i in range(len(pp)):
                for j in range(i + 1, len(pp)):
                    a_x = pp[i].x
                    a_y = pp[i].y
                    b_x = pp[j].x
                    b_y = pp[j].y
                    x = (a_x + b_x) / 2
                    y = (a_y + b_y) / 2
                    r2 = ((a_x - x) * (a_x - x) + (a_y - y) * (a_y - y))  
                    ok = True                 
                    for k in range(len(pp)):
                        d = (((x - pp[k].x) * (x - pp[k].x)) + 
                            ((y - pp[k].y) * (y - pp[k].y)))
                        if (d > r2):
                            ok = False
                    if (ok):
                        if (r2 <= min_r):
                            min_r = r2
                            xx = x
                            yy = y
            for i in range(len(pp)):
                for j in range(i + 1, len(pp)):
                    for k in range(j + 1, len(pp)):
                        a_x = pp[i].x
                        a_y = pp[i].y
                        b_x = pp[j].x
                        b_y = pp[j].y
                        c_x = pp[k].x
                        c_y = pp[k].y
                        D = 2 * (a_x * (b_y - c_y) + b_x* (c_y - a_y) + c_x * (a_y - b_y))
                        if (D == 0):
                            break
                        U_x = ((a_x * a_x + a_y * a_y) * (b_y - c_y) + (b_x* b_x + b_y * b_y) * (c_y - a_y) + (c_x * c_x + c_y * c_y) * (a_y - b_y)) / D
                        U_y = ((a_x * a_x + a_y * a_y) * (c_x - b_x) + (b_x* b_x + b_y * b_y) * (a_x - c_x) + (c_x * c_x + c_y * c_y) * (b_x - a_x)) / D
                        R = ((a_x - U_x) ** 2 + (a_y - U_y) ** 2) 
                        ok = True
                        for ind in range(len(pp)):
                            d = (((U_x - pp[ind].x) * (U_x - pp[ind].x)) + 
                                ((U_y - pp[ind].y) * (U_y - pp[ind].y)))
                            if (d > R + 0.0001):
                                ok = False
                        if (ok):
                            if (R <= min_r):
                                min_r = R
                                xx = U_x
                                yy = U_y
            r = int((min_r) ** (1 / 2))
            p = Point(xx, yy)
            c = Circle(p, r)
            self.marked_circle(c, "black")
            self.marked.append(c)                   
        self.clear_marked1()         
 
    def l_intersection(self):
        ll = []
        for i in self.marked:
            if (type(i) == Line):
                ll.append(i)
            if (type(i) == Segment):
                ll.append(i.l)
        if len(ll) > 1:
            self.h.append("l_intersection")
            line1, line2 = ll[0], ll[1]
            x = (line2.b - line1.b) / (line1.a - line2.a)
            y = line1.a * x + line1.b
            p = Point(x, y)
            self.marked_point(p, self.color)
            self.stack.append(p)    
            self.clear_marked1()        
 
 
    def clear(self):
        self.h.append(["clear"])
        self.stack.clear()
        self.marked.clear()
        self.canv.delete("all")
 
    def marked_all(self):
        self.h.append(["marked_all"])
        for i in self.stack:
            if (type(i) == Point):
                self.marked_point(i, "red")
            if (type(i) == Circle):
                self.marked_circle(i, "red")
            if (type(i) == Line):
                self.marked_line(i, "red")
            if (type(i) == Segment):
                self.marked_segment(i, "red")
            self.marked.append(i)  
        self.stack.clear()
 
 
    def line(self):
        pp = []
        for i in self.marked:
            if (type(i) == Point):
                pp.append(i)
        if (len(pp) == 1):
            self.clear_marked1()
            return
        self.h.append(["line"])
        st = pp[0]
        fn = pp[1]
        ln = Line(st, fn)
        self.marked_line(ln, self.color)
        self.stack.append(ln)
        self.clear_marked1()
 
    def make_grid(self):
        self.h.append(["grid"])
        max_y = 1080
        max_x = 840
        for i in range(0, max_x + 1, 20):
            wdh = 1            
            if (i * 2 == max_x):
                wdh += 2  
            p1 = Point(0, i);
            p2 = Point(max_y, i);
            self.canv.create_line(p1.x, p1.y, p2.x, p2.y, 
                                  width = wdh, fil = "grey")
 
        for i in range(0, max_y + 1, 20):
            wdh = 1            
            if (i * 2 == max_y):
                wdh += 2        
            p3 = Point(i, 0)
            p4 = Point(i, max_x)
            self.canv.create_line(p3.x, p3.y, p4.x, p4.y, 
                                  width = wdh, fil = "grey")
 
    def add_point(self, e):
        l = (e.get()).split()
        x = int(l[0])
        y = int(l[1])
        p = Point(x, y)
        self.draw(p)
 
    def undo(self):
        if (len(self.h) != 0):
            self.r.append(self.h[-1])
            self.h.pop()
        self.clear()
        self.h.pop()
        for ind in range(len(self.h)):
            i = self.h[ind]
            if (i[0] == "draw"):
                self.draw(i[1])
            if (i[0] == "mark"):
                self.mark(i[1])
            if (i[0] == "clear_marked"):
                self.clear_marked()
            if (i[0] == "segment"):
                self.segment()
            if (i[0] == "circle"):
                self.circle()
            if (i[0] == "l_intersection"):
                self.l_intersection()
            if (i[0] == "clear"):
                self.clear()
            if (i[0] == "marked_all"):
                self.marked_all()
            if (i[0] == "line"):
                self.line()
            if (i[0] == "grid"):
                self.grid()
            self.h.pop()
 
    def redo(self):
        if (len(self.r) == 0):
            return
        i = self.r[-1]
        if (i[0] == "draw"):
            self.draw(i[1])
        if (i[0] == "mark"):
            self.mark(i[1])
        if (i[0] == "clear_marked"):
            self.clear_marked()
        if (i[0] == "segment"):
            self.segment()
        if (i[0] == "circle"):
            self.circle()
        if (i[0] == "l_intersection"):
            self.l_intersection()
        if (i[0] == "clear"):
            self.clear()
        if (i[0] == "marked_all"):
            self.marked_all()
        if (i[0] == "line"):
            self.line()
        if (i[0] == "grid"):
            self.make_grid() 
        self.r.pop()
 
 
 
    def setUI(self):
        self.parent.title("Geogebra Pro ++")
        self.pack(fill=BOTH, expand=1)  # Размещаем активные элементы на родительском окне
 
        self.columnconfigure(6, weight=1) # Даем седьмому столбцу возможность растягиваться, благодаря чему кнопки не будут разъезжаться при ресайзе
        self.rowconfigure(2, weight=1) # То же самое для третьего ряда
 
        self.canv = Canvas(self, bg="white")
        self.canv.grid(row=2, column=0, columnspan=7,
                       padx=5, pady=5, sticky=E+W+S+N)  
        self.canv.bind("<Button-1>", self.draw)
        self.canv.bind("<Button-3>", self.mark)
        sg = Button(self, text="segment", width=10, command=lambda: self.segment())
        sg.grid(row=0, column=1)
        cl = Button(self, text="clear", width = 10, command=lambda: self.clear())
        cl.grid(row=0, column=2)
        al = Button(self, text="marked all", width=10, command=lambda: self.marked_all())
        al.grid(row=1, column=1)
        cr = Button(self, text="circle", width=10, command=lambda: self.circle())
        cr.grid(row=0, column=3)
        tt = Button(self, text="clear marked", width=10, command=lambda: self.clear_marked())
        tt.grid(row=1, column=4)
        ln = Button(self, text="line", width=10, command=lambda: self.line())
        ln.grid(row=1, column=2)
        gr = Button(self, text="grid", width=10, command=lambda: self.make_grid())
        gr.grid(row=1, column=3)
 
        intr = Button(self, text="Intersection", width=10, command=lambda: self.l_intersection())
        intr.grid(row=0, column=4)   
 
        und = Button(self, text="undo", width = 6, command=lambda: self.undo())
        und.place(x = 1300, y = 30)
        red = Button(self, text="redo", width = 6, command=lambda: self.redo())
        red.place(x = 1300, y = 5)
 
        e = Entry(width=10)
        e.place(x=1100, y=670)
 
        b = Button(self, text="add point", width=20, command=lambda: self.add_point(e))
        b.place(x=1200, y=670)        
        #tr = Button(self, text="treangulation", width=10, command=lambda: self.treangulation())
        #tr.grid(row=1, column=2)
 
 
root = Tk()
root.geometry("1920x1080")
app = Geoma(root)
root.mainloop()
