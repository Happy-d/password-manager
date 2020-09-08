import tkinter as tk
from PIL import ImageTk, Image
from random import randint


class SmartPasswordEntry(tk.Entry):
    """
    Create password entries with the option to show to not show the password.
    """
    def __init__(self, master, button_text=None, **kw):
        tk.Entry.__init__(self, master=master, **kw)
        self.master = master
        self.entry = tk.Entry(self.master, show='*', **kw)
        self.v = tk.IntVar()
        self.check_btn = tk.Checkbutton(self.master, bg=self.master['bg'], text=button_text, variable=self.v,
                                        command=self.update, activebackground=self.master['bg'])

    def update(self):
        if self.v.get() == 0:
            self.entry['show'] = '*'
        elif self.v.get() == 1:
            self.entry['show'] = ''

    def place(self, **kw):
        self.entry.place(**kw)
        self.master.update()
        self.check_btn.place(x=self.entry.winfo_x() + (self.entry['width'] * 6), y=self.entry.winfo_y() - 2)

    def place_toggle(self, **kw):
        self.check_btn.place(**kw)

    def place_forget(self):
        self.entry.place_forget()
        self.check_btn.place_forget()


class ImageFormat(tk.Canvas):
    def __init__(self, master, image, **kw):
        tk.Canvas.__init__(self, master=master, **kw)
        self.file = Image.open(image)
        self.width, self.height = self.file.size
        self.canvas = tk.Canvas(master, width=self.width, height=self.height)
        self.image = ImageTk.PhotoImage(self.file)

    def place(self, x=None, y=None, anchor=None):
        self.canvas.place(x=x, y=y, anchor=anchor)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultForeground = self["foreground"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['foreground'] = self['activeforeground']
        try:    # Use Parameter
            bool(e)
        except IndexError:
            pass

    def on_leave(self, e):
        self['foreground'] = self.defaultForeground
        try:    # Use Parameter
            bool(e)
        except IndexError:
            pass


class PasswordGenUtility:
    """
    Used to generate dynamic passwords

    Toggles for generating passwords (default 0 = False)
    ----------------------------------------------------
    lower - Allow lowercase characters
    upper - Allow uppercase characters
    num - Allow numeric characters
    spec - Allow special characters
    rep - Allow repeated characters
    char - Numeric length of password

    Use ".generate()" to generate a new password
    The product will be ".finalPassword"
    """

    def __init__(self, lower, upper, num, spec, rep, char):
        self.lowerList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.upperList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.numberList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.specialList = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?']
        self.noRepeatList = []
        self.lower = lower
        self.upper = upper
        self.num = num
        self.spec = spec
        self.rep = rep
        self.char = char
        self.catList = []
        self.catLen = 0
        self.cat = None
        self.character = None
        self.finalPassword = None

    def generate(self):
        if not self.lower == 0:
            self.catList.append("lower")

        if not self.upper == 0:
            self.catList.append("upper")

        if not self.num == 0:
            self.catList.append("num")

        if not self.spec == 0:
            self.catList.append("spec")

        if not self.rep == 0:
            self.catList.append("rep")

        if len(self.catList) == 0:
            pass
            # print("ERROR: No option has been selected")
        else:
            self.catLen = len(self.catList)

            for char in range(0, int(self.char)):
                self.cat = self.catList[randint(0, self.catLen - 1)]

                if self.cat == "lower":
                    self.character = self.lowerList[randint(0, len(self.lowerList) - 1)]

                if self.cat == "upper":
                    self.character = self.upperList[randint(0, len(self.upperList) - 1)]

                if self.cat == "num":
                    self.character = self.numberList[randint(0, len(self.numberList) - 1)]

                if self.cat == "spec":
                    self.character = self.specialList[randint(0, len(self.specialList) - 1)]

                if self.finalPassword is None:
                    self.finalPassword = self.character
                else:
                    self.finalPassword += self.character
