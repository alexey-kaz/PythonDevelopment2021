import tkinter as tk


class Application(tk.Frame):
    """Sample tkinter application class"""

    def __init__(self, master=None, title='<application>', **kwargs):
        """Create root window with frame, tune weight and resize"""
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky='NEWS')
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        """Create all the widgets"""


class App(Application):
    def create_widgets(self):
        self.move = False
        self.T = tk.Text(self, undo=True, font='fixed', borderwidth=2, relief='groove')
        self.T.tag_configure('good', foreground='green')
        self.T.tag_configure('bad', foreground='red')
        self.T.grid(row=0, column=0, sticky='NEWS')

        self.B = tk.LabelFrame(self)
        self.B.grid(row=1, columnspan=2, sticky='NEWS')

        self.Q = tk.Button(self.B, text='Quit', command=self.master.quit)

        self.C = tk.Canvas(self, borderwidth=2, relief='groove')
        self.C.grid(row=0, column=1, sticky='NEWS')
        self.C.bind('<Button-1>', self.pick_oval)
        self.C.bind('<B1-Motion>', self.move_oval)
        self.C.bind('<B1-ButtonRelease>', self.release_oval)

        self.CT = tk.Button(self.B, text='Clear Text', command=self.clearText, relief='groove')
        self.CC = tk.Button(self.B, text='Clear Canvas', command=self.clearCanvas, relief='groove')
        self.R = tk.Button(self.B, text='Text => Canvas', command=self.text2canvas, relief='groove')
        self.L = tk.Button(self.B, text='Canvas => Text', command=self.canvas2text, relief='groove')

        for O in self.CT, self.CC, self.R, self.L, self.Q:
            O.grid(row=1, column=self.B.grid_size()[0], padx=20)

    def clearText(self):
        self.T.delete(1.0, tk.END)
        self.T.mark_set('From', '1.0')
        self.T.mark_set('To', 'end')

    def clearCanvas(self):
        self.C.delete('all')

    def pick_oval(self, event):
        overlapping = self.C.find_overlapping(event.x, event.y, event.x, event.y)
        self.old_coord = (event.x, event.y)
        if not overlapping:
            self.oval = self.C.create_oval(event.x, event.y, event.x, event.y,
                                           width=2, outline='blue', fill='lightblue')
        else:
            self.oval = overlapping[-1]
            self.move = True

    def move_oval(self, event):
        if self.move:
            self.C.move(self.oval, event.x - self.old_coord[0], event.y - self.old_coord[1])
            self.old_coord = (event.x, event.y)
        else:
            self.C.coords(self.oval, self.old_coord[0], self.old_coord[1], event.x, event.y)

    def release_oval(self, event):
        self.move = False

    def addTag(self, new_tag, line_num, length):
        if new_tag:
            old_tag = 'bad' if new_tag == 'good' else 'good'
        else:
            return
        self.T.tag_remove(old_tag, '{}.0'.format(line_num), '{}.0 + {} chars'.format(line_num, length))
        self.T.tag_add(new_tag, '{}.0'.format(line_num), '{}.0 + {} chars'.format(line_num, length))

    def text2canvas(self):
        self.C.delete('all')
        text = self.T.get(1.0, tk.END).split('\n')
        for i, line in enumerate(text):
            if not line.lstrip():
                continue
            elif line[0] == '#':
                self.addTag('good', i + 1, len(line))
                continue
            parameters = line.split()[1:]
            *coords, width, outline, fill = parameters
            try:
                eval(('self.C.create_oval(' + ('{}, ' * 4).format(*coords) +
                      'width={}, outline=\'{}\', fill=\'{}\')'.format(width, outline, fill)))
                self.addTag('good', i + 1, len(line))
            except Exception:
                self.addTag('bad', i + 1, len(line))

    def canvas2text(self):
        ovals = self.C.find_all()
        text = ''
        self.T.delete(1.0, tk.END)
        for oval in ovals:
            coords = (str(coords) for coords in self.C.coords(oval))
            params = self.C.itemconfigure(oval)
            width, outline, fill = params['width'][-1], params['outline'][-1], params['fill'][-1]
            line = 'oval ' + ' '.join(coords) + ' {} {} {}\n'.format(width, outline, fill)
            text += line
            self.T.replace(1.0, tk.END, text)
        self.addTag('good', 1, len(text))


app = App(title='05_SshAndSmartWidgets')
app.mainloop()
