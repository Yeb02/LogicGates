#Sur un concept de Sebastian Lague
#https://www.youtube.com/watch?v=QZwneRb-zqA


import cv2, numpy as np, tkinter as tk, os, random
from tkinter import ttk
from PIL import Image, ImageTk
from time import time


class screen():
    def __init__(self, width, height):
        self.node_id = [-1, -1, False, -1, -1, False]  #id du premier noeud dans son bloc, id du bloc, bool vrai si le noeud est une input
        self.line_x, self.line_y = 0, 0
        self.canvas = None
        self.Name = None
        self.name = "TEST"
        self.InEntry = 0
        self.OutEntry = 0
        self.holding_line = False
        self.create_color = "#ff00ff"
        self.time_since_press = time()
        self.mousex, self.mousey = 0,  0
        self.selected_object = None
        self.selected_object_id = -1
        self.float_id = []
        self.width, self.height = width, height
        f = open('units.txt', 'r').readlines()
        self.possible_units = [f[k][:-1].split(" ") for k in range(len(f))]
        self.input_nb, self.output_nb = int(self.possible_units[0][2]), int(self.possible_units[1][1])
        self.components_id = [0, 1]                                             #unit, ComponentsInIDs, ComponentsOutIDs, x, y, DrawingIDs, input, output, lines
        self.components = [component(unit(self.possible_units[0] + [self], True), [],[-1]*self.input_nb,  50, int(self.height/2), [],  [], [0]*self.input_nb, [[]]* self.input_nb),
                           component(unit(self.possible_units[1] + [self], True), [[-1, -1]]*self.output_nb, [], self.width - 50, int(self.height/2), [], [0]*self.input_nb, [], [])]

    def update_GUI(self):
        for (i, elt) in enumerate(self.possible_units[2:]):
            button1 = tk.Button(root, text=elt[0], command = lambda i=i : self.onClicked_unitButton(i), anchor = "w")
            button1.configure(width = 10, activebackground = "#008800", bg="#00ff00")
            button1_window = self.canvas.create_window(80*(i+1), self.height - 25, anchor="nw", window=button1)

        for (i, elt) in enumerate(self.components):
            elt.DrawingIDs = self.draw_block(elt.unite, elt.x, elt.y)
            elt.lines = [[self.draw_line(elt.unite.input[k], e[1], e[2], e[3]), e[1], e[2], e[3]] if e != [] else [] for (k, e) in enumerate(elt.lines)]

        button_undo = tk.Button(root, text="Undo", command = self.onClicked_undoButton, anchor = "w")
        button_undo.configure(width = 10, activebackground = "#33B5E5", bg="#0088bb")
        button_undo_window = self.canvas.create_window(self.width - 80, 0, anchor="nw", window=button_undo)

        button_create = tk.Button(root, text="Create", command = self.onClicked_createButton, anchor = "w")
        button_create.configure(width = 10, activebackground = "#33B5E5", bg="#0088bb")
        button_create_window = self.canvas.create_window(0, self.height - 25, anchor="nw", window=button_create)

        button_clear = tk.Button(root, text="Clear", command = self.onClicked_clearButton, anchor = "w")
        button_clear.configure(width = 10, activebackground = "#33B5E5", bg="#0088bb")
        button_clear_window = self.canvas.create_window(self.width - 80, self.height - 25, anchor="nw", window=button_clear)

        self.Name = tk.StringVar()
        textzone = ttk.Entry(root, width = 18, textvariable=self.Name)
        textzone_window = self.canvas.create_window(0, 0, anchor="nw", window=textzone)
        button = ttk.Button(root, text = "Confirm unit name", command=self.ChangeName)
        button_name_window = self.canvas.create_window(0, 20, anchor="nw", window=button)

        self.InEntry = tk.StringVar()
        textzone = ttk.Entry(root, width = 21, textvariable=self.InEntry)
        textzone_window = self.canvas.create_window(110, 0, anchor="nw", window=textzone)
        button = ttk.Button(root, text = "Confirm input number", command=self.ChangeInEntry)
        button_name_window = self.canvas.create_window(110, 20, anchor="nw", window=button)

        self.OutEntry = tk.StringVar()
        textzone = ttk.Entry(root, width = 22, textvariable=self.OutEntry)
        textzone_window = self.canvas.create_window(240, 0, anchor="nw", window=textzone)
        button = ttk.Button(root, text = "Confirm output number", command=self.ChangeOutEntry)
        button_name_window = self.canvas.create_window(240, 20, anchor="nw", window=button)


    def onClicked_undoButton(self):
        pass

    def onClicked_unitButton(self, i):
        u = unit(self.possible_units[i + 2] + [self], True)
        self.components.append(component(u, u.nb_in*[-1], u.nb_out*[-1], self.mousex, self.mousey, [], u.nb_in*[0], u.nb_out*[0], [[] * u.nb_out]))
        self.selected_object = self.components[-1].unite
        self.float_id = self.draw_block(self.selected_object, self.mousex, self.mousey)
        self.selected_object_id = len(self.components) - 1
        self.components[self.selected_object_id].DrawingIDs = self.float_id

    def onClicked_clearButton(self):
        for elt in self.components:
            for l in elt.lines:
                try: self.canvas.delete(l[0])
                except: pass
            for i in elt.DrawingIDs:
                try: self.canvas.delete(i)
                except: pass

        self.components = [component(unit(self.possible_units[0] + [self], True), [],[-1]*self.input_nb,  50, int(self.height/2), [],  [], [0]*self.input_nb, [[]]* self.input_nb),
                           component(unit(self.possible_units[1] + [self], True), [[-1, -1]]*self.output_nb, [], self.width - 50, int(self.height/2), [], [0]*self.input_nb, [], [])]
        self.components[0].unite.output, self.components[0].unite.nb_out = self.input_nb * [0], self.input_nb
        self.components[1].unite.input, self.components[1].unite.nb_in = self.output_nb * [0], self.output_nb
        self.components_id = [0, 1]
        self.float_id = []
        self.holding_line = False
        self.selected_object = None
        self.update_GUI()

    def onClicked_createButton(self): #data = [name, nb_in, nb_out, color, SCREEN ! components, components_id, screen]
        unit([self.name, self.input_nb, self.output_nb, self.create_color, self.components, self.components_id, self], False)
        self.possible_units.append(open('units.txt', 'r').readlines()[-1][:-1].split(" "))
        self.update_GUI()   #Pour l'instant, créer: le bloc identité ou un bloc sans nom font bugger.

    def ChangeName(self):
        self.name = self.Name.get()

    def ChangeInEntry(self):
        n = int(self.InEntry.get())
        if n > self.input_nb:
            self.components[0].unite.output = self.components[0].unite.output + [0] * (n - self.components[1].unite.nb_out)
            self.components[0].ComponentsOutIDs = self.components[0].ComponentsOutIDs + [-1] * (n - self.components[1].unite.nb_out)
            self.components[0].unite.nb_out = n
            self.output_nb = n
        elif n < self.input_nb:  #TODO remove les liens.
            self.components[0].unite.output = self.components[0].unite.output[:n]
            self.output_nb = n
            for elt in self.components[0].lines[n + 1:]:
                try: self.canvas.delete(elt[0])
                except: pass
            for elt in self.components[0].ComponentsOutIDs[n+1:]:
                #self.disconnect(...)  Et faire pour  outentry
                l = [id[0] for id in self.components[elt].ComponentsInIDs]
                self.components[elt].ComponentsInIDs[self.get_indice(0, l)] = [-1, -1]  #pas le bon élément ... TODO
            self.components[0].ComponentsOutIDs = self.components[0].ComponentsOutIDs[:n]
            self.components[0].lines = self.components[0].lines[:n]

        self.components[0].unite.tailley = self.components[0].unite.nb_out * self.components[0].unite.taille
        self.components[0].unite.taillex = 1.5 * self.components[0].unite.tailley
        self.dynamic_display()

    def ChangeOutEntry(self):
        n = int(self.OutEntry.get())
        if n > self.output_nb:
            self.components[1].unite.input = self.components[1].unite.input + [0] * (n - self.components[1].unite.nb_in)
            self.components[1].ComponentsInIDs = self.components[1].ComponentsInIDs + [-1, -1] * (n - self.components[1].unite.nb_in)
            self.components[1].unite.nb_in = n
            self.output_nb = n
        elif n < self.output_nb:  #TODO remove les liens.
            self.components[1].unite.input = self.components[1].unite.input[:n]
            self.components[1].ComponentsInIDs = self.components[1].ComponentsInIDs[:n]
            self.components[1].unite.nb_in = n
            self.output_nb = n
        self.components[1].unite.tailley = self.components[1].unite.nb_in * self.components[1].unite.taille
        self.components[1].unite.taillex = 1.5 * self.components[1].unite.tailley
        self.dynamic_display()

    def motion(self, event):
        self.mousex, self.mousey = event.x, event.y
        if self.selected_object is not None:
            for elt in self.float_id:
                try: self.canvas.delete(elt)
                except: pass
            self.float_id = self.draw_block(self.selected_object, event.x, event.y)
            self.components[self.selected_object_id].y = event.y
            self.components[self.selected_object_id].x = event.x
            self.components[self.selected_object_id].DrawingIDs = self.float_id

    def key(self, event): #TODO
        pass


    def click(self, event):
        self.time_since_press = time()
        if self.selected_object is not None:  #clic en portant une unité
            for elt in self.float_id:
                try: self.canvas.delete(elt)
                except: pass
            self.float_id = []
            self.components[self.selected_object_id].DrawingIDs = self.draw_block(self.selected_object, event.x, event.y)
            self.components[self.selected_object_id].y = event.y
            self.components[self.selected_object_id].x = event.x
            self.selected_object = None
            self.dynamic_display()

        elif self.mousey < self.height - 25:  #on s'assure de ne pas cliquer en même temps sur un des boutons
            pos = self.get_clicked_object(self.canvas.find_closest(self.mousex, self.mousey, halo=None, start=None)[0])
            if pos[0] == 2: #si click sur noeud
                if pos[1] == 0: #Si sur un noeud de l'input, modification de l'input
                    self.components[0].unite.output[pos[2]] = 1 - self.components[0].unite.output[pos[2]]
                    self.dynamic_display()
                else:
                    self.holding_line = True
                    if self.node_id[3] != -1:
                        self.node_id = self.node_id[3:] + [-1, -1, False]
                    else:
                        self.node_id = self.node_id[:3] + [-1, -1, False]
                    self.line_x, self.line_y = event.x, event.y

            elif pos[0] == 0 or pos[0] == 1: #on est sur une unité, qu'on va déplacer
                self.selected_object_id = pos[1]
                self.selected_object = self.components[self.selected_object_id].unite
                self.float_id = self.components[pos[1]].DrawingIDs

    def get_clicked_object(self, id): #object user clicked (OR UNCLICKED !) on
        for (i, elt) in enumerate(self.components):
            u = self.get_indice(id, elt.DrawingIDs)
            if u == 0:
                return [0,i]    #rectangle principal
            if u == len(elt.DrawingIDs) - 1:
                return [1,i]    #texte
            if u != -1:
                if self.node_id[0] == -1:
                    self.line_x, self.line_y = self.mousex, self.mousey
                    self.node_id[0] = i
                    self.node_id[1] = u - 1
                    if u <= elt.unite.nb_in:
                        self.node_id[2] = True
                    else:
                        self.node_id[1] = u - 1 - elt.unite.nb_in
                else:
                    self.node_id[3] = i
                    self.node_id[4] = u - 1
                    if u <= elt.unite.nb_in:
                        self.node_id[5] = True
                    else:
                        self.node_id[4] = u - 1 - elt.unite.nb_in

                return [2,i, u-1]       #noeud
        return [-1,-1] #ne devrait pas arriver

    def dynamic_display(self):
        for (i,elt) in enumerate(self.components_id):
            try: self.components[elt].unite.input = [self.components[unit_i].unite.output[out_i]
                                                 if unit_i!= -1 else 0 for (unit_i, out_i) in self.components[elt].ComponentsInIDs]
            except: pass
            self.components[elt].unite.evaluate()

            for e in self.components[elt].lines:
                if e != []:
                    try: self.canvas.delete(e[0])
                    except: pass
            self.components[elt].lines = [[self.draw_line(elt, e[1], e[2], e[3]),e[1], e[2], e[3]] if e != [] else [] for (k, e) in enumerate(self.components[elt].lines)]
            for e in self.components[elt].DrawingIDs:
                try: self.canvas.delete(e)
                except: pass
            self.components[elt].DrawingIDs = self.draw_block(self.components[elt].unite, self.components[elt].x, self.components[elt].y)

    def unclick(self, event):
        pos = self.get_clicked_object(self.canvas.find_closest(self.mousex, self.mousey, halo=None, start=None)[0])
        if self.holding_line and time() - self.time_since_press > .2 and pos[0] == 2: #si unclick sur noeud
            if self.node_id[2] != self.node_id[5] and self.node_id[0] != self.node_id[3]: #un output et un input, blocs différents.
                if self.node_id[2]: #c'est alors l'input
                    sending_unit_id, out_id, receiving_unit_id, in_id = self.node_id[3], self.node_id[4], self.node_id[0], self.node_id[1]
                else:
                    sending_unit_id, out_id, receiving_unit_id, in_id = self.node_id[0], self.node_id[1], self.node_id[3], self.node_id[4]
                self.components[sending_unit_id].lines[out_id] = [self.draw_line(sending_unit_id, out_id, receiving_unit_id, in_id), out_id, receiving_unit_id, in_id]
                self.connect(sending_unit_id, out_id, receiving_unit_id, in_id)
                self.node_id = [-1, -1, False] * 2
                self.dynamic_display()

        elif time() - self.time_since_press < .4 and pos[0] == 2 and self.node_id[2] == self.node_id[5] and self.node_id[0] == self.node_id[3] and self.node_id[2]:
            if self.components[pos[1]].ComponentsInIDs[pos[2]] != [-1, -1]:
                try:
                    self.canvas.delete(self.components[self.components[pos[1]].ComponentsInIDs[pos[2]][0]].lines[self.components[pos[1]].ComponentsInIDs[pos[2]][1]][0])
                    self.components[self.components[pos[1]].ComponentsInIDs[pos[2]][0]].lines[self.components[pos[1]].ComponentsInIDs[pos[2]][1]] = []
                except: print("blyat")
                self.disconnect(self.components[pos[1]].ComponentsInIDs[pos[2]][0], self.components[pos[1]].ComponentsInIDs[pos[2]][1], pos[1], pos[2])
            self.dynamic_display()
        self.holding_line = False



    def draw_line(self, sending_unit_id, out_id, receiving_unit_id, in_id):
        x1, y1 = self.components[sending_unit_id].unite.get_output_coordinate(out_id, self.components[sending_unit_id].x, self.components[sending_unit_id].y)
        x2, y2 = self.components[receiving_unit_id].unite.get_input_coordinate(in_id, self.components[receiving_unit_id].x, self.components[receiving_unit_id].y)
        color = "#000000" * (1 - self.components[sending_unit_id].unite.output[out_id]) + "#ff0000" * self.components[sending_unit_id].unite.output[out_id]
        return self.canvas.create_line(x1, y1, x2, y2, fill=color, capstyle="round", joinstyle="round", width = 3)

    def draw_block(self, unit, x, y):
        return unit.draw(x, y)

    def connect(self, sending_unit_id, out_id, receiving_unit_id, in_id):
        s, r = self.get_indice(sending_unit_id, self.components_id), self.get_indice(receiving_unit_id, self.components_id)
        if s != -1:
            if r != -1:
                if r < s:
                    l = self.components_id[r + 1:s+1]
                    l1, l2 = [], []
                    for elt in l:
                        if elt in self.components[receiving_unit_id].ComponentsOutIDs:
                            l1.append(elt)
                        else:
                            l2.append(elt)
                    self.components_id = self.components_id[:r] + l2 + [receiving_unit_id] + l1 + self.components_id[s+1:]
            else:
                self.components_id.insert(s + 1, receiving_unit_id)
        else:
            if r != -1:
                self.components_id.insert(r, sending_unit_id)
            else:
                self.components_id.insert(1, sending_unit_id)
                self.components_id.insert(1, receiving_unit_id)
        self.components[receiving_unit_id].ComponentsInIDs[in_id] = [sending_unit_id, out_id]
        self.components[sending_unit_id].ComponentsOutIDs[out_id] = receiving_unit_id

    def disconnect(self, sending_unit_id, out_id, receiving_unit_id, in_id):
        self.components[receiving_unit_id].ComponentsInIDs[in_id] = [-1, -1]
        self.components[sending_unit_id].ComponentsOutIDs[out_id] = -1

    def get_indice(self, id, l):
        try: x = l.index(id)
        except: return -1
        return x

class component(screen):  #lines = lignes sortantes sous la forme [draw id, out_id, receiving_unit_id, in_id]
    def __init__(self, unit, ComponentsInIDs, ComponentsOutIDs, x, y, DrawingIDs, input, output, lines):
        self.unite, self.ComponentsInIDs, self.ComponentsOutIDs, self.x, self.y, self.DrawingIDs, self.input, self.output, self.lines = unit, ComponentsInIDs, ComponentsOutIDs, x, y, DrawingIDs, input, output, lines

class unit(screen):
    def __init__(self, data, from_file):  #Components : unit

        self.name = data[0]    #data = ligne du fichier texte
        self.nb_in, self.nb_out = int(data[1]), int(data[2])
        self.input, self.output = [0]*self.nb_in, [0]*self.nb_out
        self.screen = data[-1]
        self.color = data[3]
        self.taille = 20
        self.tailley = max(self.nb_in, self.nb_out) * self.taille
        self.taillex = 1.5 * self.tailley
        #create recursivly from file:
        #si vient du fichier: #data = [name, nb_in, nb_out, colors, components, subUnits_ComponentsInIDs, components_id, screen]
        #si de la fct create: #data = [name, nb_in, nb_out, color, SCREEN ! components, components_id, screen]
        if not from_file:
            names, comps, comps_id = "", "", ""
            for (comp, id) in zip(data[4], data[5]):
                names += comp.unite.name + '_'
                comps_id += str(id) + "_"
                for i in comp.ComponentsInIDs:
                    comps += str(i[0]) + ',' + str(i[1]) + ',_'
                comps += "#"
            with open('units.txt', 'a') as output_file:
                ligne = data[0]+" "+ str(self.nb_in)+" "+str(self.nb_out)+" "+self.color+" "+names+" "+comps+" "+comps_id
                output_file.write(ligne + "\n")


        if self.name not in ["INPUT", "OUTPUT", "NOT", "AND"]:
            data = self.get_line_in_file(self.name)
            l1, l2, l3, e = [], [], [], ''
            for elt in data[5]:
                if elt == ",":
                    l3.append(int(e))
                    e = ""
                elif elt == "_":
                    l2.append(l3)
                    l3 = []
                elif elt == "#":
                    l1.append(l2)
                    l2 = []
                else:
                    e += elt


            l3, name, l2, id = [], '', [], ''
            for n in data[4]: #data = [name, nb_in, nb_out, color, SCREEN ! components, components_id, screen]
                if n == '_':
                    l3.append(name)
                    name = ''
                else:
                    name+=n
            for i in data[6]:
                if i == '_':
                    l2.append(int(id))
                    id = ''
                else:
                    id+=i

            self.unit_components = [[unit(self.get_line_in_file(n), True), l] for (n, l) in zip(l3, l1)]
            self.unit_components_id = list(l2)
            self.unit_components[0][0].nb_output = self.nb_out
            self.unit_components[1][0].nb_input = self.nb_in
            self.unit_components[0][0].output = self.output
            self.unit_components[1][0].nb_input = self.input


    def get_line_in_file(self, name):
        f = [elt.split(" ")[0] for elt in open('units.txt', 'r').readlines()]
        return open('units.txt', 'r').readlines()[f.index(name)].split()

    def get_output_coordinate(self, out_id, x, y):
        return x + self.taillex + self.taille/3, y - self.tailley  + 2*(out_id + 1)*self.tailley/(self.nb_out + 1)

    def get_input_coordinate(self, in_id, x, y):
        return x - self.taillex - self.taille/3, y - self.tailley  + 2*(in_id + 1)*self.tailley/(self.nb_in + 1)

    def draw(self, x, y):
        if len(self.input) != self.nb_in:
            print(len(self.input), self.nb_in)
        fill_in = [self.input[k-1] * 'red' + (1 - self.input[k-1])*'black' for k in range(1, self.nb_in + 1)]
        fill_out = [self.output[k-1] * 'red' + (1 - self.output[k-1])*'black' for k in range(1, self.nb_out + 1)]
        active_in = [self.input[k-1] * 'black' + (1 - self.input[k-1])*'red' for k in range(1, self.nb_in + 1)]
        active_out = [self.output[k-1] * 'black' + (1 - self.output[k-1])*'red' for k in range(1, self.nb_out + 1)]
        return([self.screen.canvas.create_rectangle(x - self.taillex, y - self.tailley, x + self.taillex, y + self.tailley, fill=self.color, activefill="#aa5500", width = 2)] +
               [self.screen.canvas.create_oval(x - self.taillex - self.taille, y - self.tailley  + 2*k*self.tailley/(self.nb_in + 1) - self.taille/2, x - self.taillex, y - self.tailley + self.taille/2  + 2*k*self.tailley/(self.nb_in + 1),
                fill=fill_in[k-1], activefill=active_in[k-1], width=0) for k in range(1, self.nb_in + 1)] +
               [self.screen.canvas.create_oval(x + self.taillex, y - self.tailley  + 2*k*self.tailley/(self.nb_out + 1) - self.taille/2, x + self.taillex + self.taille, y - self.tailley + self.taille/2  + 2*k*self.tailley/(self.nb_out + 1),
                fill=fill_out[k-1], activefill=active_out[k-1], width=0) for k in range(1, self.nb_out + 1)] +
               [self.screen.canvas.create_text(x, y, text=self.name, font="Arial 16 italic", fill="black")])

    def evaluate(self):
        if self.name == "NOT":
            self.output = [not self.input[0]]
        elif self.name == "AND":
            self.output = [1*(self.input[0] and self.input[1])]
        elif self.name == "INPUT" or self.name == "OUTPUT":
            pass
        else:
            self.unit_components[0][0].output = self.input
            for id in self.unit_components_id:
                self.unit_components[id][0].input = [self.unit_components[unit_i][0].output[out_i] if unit_i != -1 else 0
                                                    for (unit_i, out_i) in self.unit_components[id][1]]
                self.unit_components[id][0].evaluate()
            self.output = self.unit_components[1][0].input
#Dans le fichiers txt annexe:
if True: #reset ou pas à chaque boot
    with open('units.txt', 'a') as f:
        f.truncate(0)
        f.write("INPUT 0 2 #ffffff # # #" + "\n" +
                "OUTPUT 2 0 #ffffff # # #" + "\n" +
                "NOT 1 1 #ff0000 # # #" + "\n" +
                "AND 2 1 #8888ee # # #" + "\n")
        f.close()


root = tk.Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.title('Feeling The Turing')
root.attributes('-fullscreen', True)
display = screen(w, h)
display.canvas = tk.Canvas(root, width=w, height=h)
display.canvas.bind("<KeyPress>", display.key)
display.canvas.bind("<Button-1>", display.click)
display.canvas.bind('<ButtonRelease-1>', display.unclick)
display.canvas.bind('<Motion>', display.motion)
path = "computer-circuit-board-16.jpg"

img = ImageTk.PhotoImage(Image.open(path))
image = display.canvas.create_image(0, 0, anchor="nw", image=img)
display.canvas.pack(side="top")
display.canvas.focus_set()
display.update_GUI()
root.mainloop()
