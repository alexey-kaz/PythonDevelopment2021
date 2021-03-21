import tkinter as tk


class Application(tk.Frame):
    """Sample tkinter application class"""

    def __init__(self, master=None):
        """Create root window with frame, tune weight and resize"""
        super().__init__(master, background='black')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        """Create all the widgets"""
        self.Label_Input = LabelEdit(self)
        self.Label_Input.grid(row=1)
        self.Q = tk.Button(self, text='Quit', background='yellow', command=self.quit)
        self.Q.grid(row=2)


class LabelEdit(tk.Label):
    def __init__(self, master=None):
        self.S = tk.StringVar()
        super().__init__(master, font=('Menlo', 25), anchor='w', takefocus=True,
                         highlightthickness=1, textvariable=self.S, background='yellow')
        self.sym_pos = tk.Frame(self, height=35, background='red')
        self.bind('<Button-1>', self.mouse_click)
        self.bind('<KeyPress>', self.key_press)
        self.sym_width = 15
        self.change_pos = 0
        self.cur_pos = 0
        self.move = 0
        self.pos_change()

    def mouse_click(self, event):
        self.focus()
        self.cur_pos = round(event.x / self.sym_width)
        self.move = 0
        self.pos_change()

    def key_press(self, event):
        if event.char.isprintable():
            self.S.set(self.S.get()[:self.change_pos] + event.char + self.S.get()[self.change_pos:])
            self.move += 1
        elif event.keysym == 'BackSpace' and len(self.S.get()) > 0:
            self.S.set(self.S.get()[0:self.change_pos - 1] + self.S.get()[self.change_pos:])
            self.move -= 1
        elif event.keysym == 'Delete' and len(self.S.get()) > 0:
            self.S.set(self.S.get()[:self.change_pos] + self.S.get()[self.change_pos + 1:])
        elif event.keysym == 'End' or event.keysym == 'Home':
            self.cur_pos = len(self.S.get()) * int(event.keysym != 'Home')
            self.move = 0
        elif event.keysym == 'KP_Left' or event.keysym == 'Left':
            self.move -= 1
        elif event.keysym == 'KP_Right' or event.keysym == 'Right':
            self.move += 1
        self.pos_change()

    def pos_change(self):
        self.change_pos = self.cur_pos
        self.change_pos += self.move
        self.change_pos = max(0, min(self.change_pos, len(self.S.get())))
        self.sym_pos.place(x=self.sym_width * self.change_pos)


app = Application()
app.master.title('LabelEdit')
app.mainloop()
