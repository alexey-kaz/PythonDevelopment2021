import tkinter as tk
import tkinter.messagebox
import random


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky='news')
        self.createWidgets()

    def solvability(self, checker):
        parity = 0
        row = 0
        blankrow = 0
        for i in range(16):
            if i % 4 == 0:
                row += 1
            if checker[i] == 0:
                blankrow = row
                continue
            for j in range(i+1, 16):
                if (checker[i] > checker[j]) and checker[j] != 0:
                    parity += 1
        if blankrow % 2 == 0:
            return bool(parity % 2 == 0)
        else:
            return bool(parity % 2 != 0)

    def check(self, x):
        d = self.dictionary[int(x['text'])]
        if (d-1 not in self.dictionary.values()) and d-1 >= 0:
            d -= 1
        elif (d+1 not in self.dictionary.values()) and d+1 <= 15:
            d += 1
        elif (d-4 not in self.dictionary.values()) and d-4 >= 0:
            d -= 4
        elif (d+4 not in self.dictionary.values()) and d+4 <= 15:
            d += 4
        self.dictionary[int(x['text'])] = d
        x.grid(row=1+d % 4, column=d//4, sticky='news')
        if self.dictionary == self.win:
            tk.messagebox.showinfo("Yay!", "Success!")

    def restart(self):
        for i in self.buttons:
            i.destroy()
        self.buttons = [(tk.Button(self, text=x, height=1, width=2)) for x in range(1, 16)]
        solvability = False
        while not solvability:
            checker = [0]*16
            for i in self.buttons:
                i['command'] = lambda x=i: self.check(x)
                rand = random.randint(0, 15)
                while rand in self.dictionary.values():
                    rand = random.randint(0, 15)
                j = int(i.cget('text'))
                self.dictionary[j] = rand
                if rand == 15:
                    checker[15] = j
                else:
                    checker[(rand*4) % 15] = j
                i.grid(row=1+self.dictionary[j] % 4, column=self.dictionary[j]//4, sticky='news')
            solvability = self.solvability(checker)
            print(solvability)

    def createWidgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        for i in range(1, 5):
            self.columnconfigure(i - 1, weight=1)
            self.grid_rowconfigure(i, weight=1)
        self.win = {}
        self.dictionary = {}
        for i in range(15):
            self.win[i+1] = (i*4) % 15
        self.buttons = []
        self.newButton = tk.Button(self, text='New', command=self.restart, height=2, width=2)
        self.exitButton = tk.Button(self, text='Exit', command=self.quit, height=2, width=2)
        self.newButton.grid(row=0, column=0, columnspan=2, sticky='news')
        self.exitButton.grid(row=0, column=2, columnspan=2, sticky='news')
        self.restart()


app = Application()
app.master.title('15 puzzle')
app.mainloop()
