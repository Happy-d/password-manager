import tkinter.font as font
from tkinter import *
from tkinter import filedialog
from distutils import util
from utils import *
import os
import shutil
from datetime import datetime
import database as db


version = "v1.0.0-beta"


def run_setup():
    with open('path.txt', 'r') as file:
        try:
            path = file.readlines()[0]
        except IndexError:
            path = ''

    operator = db.Database(path)
    try:
        runSetup = util.strtobool(operator.get_setup_tog())
    except db.sqlite3.OperationalError:
        runSetup = True
    return runSetup


class SetupApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.default_font = font.Font(size=12, underline=1)

        # Setup root and settings
        self.windowX = 600
        self.windowY = 400
        self.window_bg_l = 'gray92'
        self.window_bg_d = 'gray21'
        self.master = master
        self.master.configure(bg=self.window_bg_l)
        self.master.geometry('{}x{}'.format(self.windowX, self.windowY))
        self.master.title('Password Manager - Setup')
        self.can_close = False
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

        # Theme widgets
        self.v = IntVar()
        self.thmX = 30
        self.thmY = 20
        self.theme = 'light'
        self.darkRad = Radiobutton(self.master, text="Dark", variable=self.v, value=1, command=self.update,
                                   bg=self.window_bg_l, activebackground=self.window_bg_l)
        self.lightRad = Radiobutton(self.master, text="Light", variable=self.v, value=0, command=self.update,
                                    bg=self.window_bg_l, activebackground=self.window_bg_l)
        self.theme_lbl = Label(self.master, text="Theme:", bg=self.window_bg_l, font=self.default_font)

        # Location widgets
        self.lv = IntVar()
        self.locX = 30
        self.locY = 60
        self.localLoc = Radiobutton(self.master, text="Local Folder", variable=self.lv, value=0, command=self.update,
                                    bg=self.window_bg_l, activebackground=self.window_bg_l)
        self.extLoc = Radiobutton(self.master, text="External Drive", variable=self.lv, value=1, command=self.update,
                                  bg=self.window_bg_l, activebackground=self.window_bg_l)
        self.location_lbl = Label(self.master, text="Store Database:", bg=self.window_bg_l, font=self.default_font)

        # New Path
        self.pathX = 30
        self.pathY = 100
        self.default_dir = ''
        self.path_lbl = Label(self.master, text="New Path:", bg=self.window_bg_l, font=self.default_font)
        self.path_ent = Entry(self.master, width=36)
        self.path_ent.insert(0, self.default_dir)
        self.path_btn = Button(self.master, text="Choose Path...", command=self.get_dir)

        # Pin
        self.pinX = 30
        self.pinY = 100  # Change this in the self.update function too!!!
        self.pin = StringVar()
        self.pin_re = StringVar()
        self.pin_lbl = Label(self.master, text="Enter Pin:", bg=self.window_bg_l, font=self.default_font)
        self.pin_re_lbl = Label(self.master, text="Re-enter Pin:", bg=self.window_bg_l, font=self.default_font)
        self.pin_ent = SmartPasswordEntry(self.master, 'Show', width=10, textvariable=self.pin)
        self.pin_re_ent = SmartPasswordEntry(self.master, 'Show', width=10, textvariable=self.pin_re)

        # Auto backup
        self.backupX = 30
        self.backupY = 180
        self.backup_dir = ''
        self.backup_var = IntVar()
        self.backup_var.set(1)
        self.backup_tog = 'no'
        self.backup_lbl = Label(self.master, text="Auto Backup:", font=self.default_font)
        self.backup_yes = Radiobutton(self.master, text="Yes", variable=self.backup_var, value=0, command=self.update)
        self.backup_no = Radiobutton(self.master, text="No", variable=self.backup_var, value=1, command=self.update)
        self.backup_path_lbl = Label(self.master, text="Backup Path:", font=self.default_font)
        self.backup_path_ent = Entry(self.master, width=36)
        self.backup_path_btn = Button(self.master, text="Choose Path...", command=self.get_backup_dir)

        # Warning
        warning_text = "WARNING: Running the setup multiple times may result in data loss."
        self.warning_lbl = Label(self.master, text=warning_text, fg='red')

        # Confirm and cancel buttons
        self.confirm_btn = Button(self.master, text="Confirm", width=10, command=self.confirm)
        self.cancel_btn = Button(self.master, text="Cancel", width=10, command=self.quit)
        self.error_lbl = Label(self.master, fg='red', bg=self.window_bg_l)

        # Invoke functions
        self.place()
        self.pack()
        self.update()

    def place(self):
        # Theme
        self.theme_lbl.place(x=self.thmX, y=self.thmY)
        self.lightRad.place(x=self.thmX + 160, y=self.thmY)
        self.darkRad.place(x=self.thmX + 260, y=self.thmY)

        # Location
        self.location_lbl.place(x=self.locX, y=self.locY)
        self.localLoc.place(x=self.locX + 160, y=self.locY)
        self.extLoc.place(x=self.locX + 260, y=self.locY)

        # Pin
        self.pin_lbl.place(x=self.pinX, y=self.pinY)
        self.pin_re_lbl.place(x=self.pinX, y=self.pinY + 40)
        self.pin_ent.place(x=self.pinX + 160, y=self.pinY + 5)
        self.pin_re_ent.place(x=self.pinX + 160, y=self.pinY + 45)

        # Auto Backup
        self.backup_lbl.place(x=self.backupX, y=self.backupY)
        self.backup_yes.place(x=self.backupX + 160, y=self.backupY)
        self.backup_no.place(x=self.backupX + 260, y=self.backupY)

        # Warning
        self.warning_lbl.place(x=self.windowX / 2, y=(self.windowY / 6) * 5, anchor=CENTER)

        # Confirm and cancel
        self.confirm_btn.place(x=self.windowX - 10, y=self.windowY - 10, anchor=SE)
        self.cancel_btn.place(x=10, y=self.windowY - 10, anchor=SW)
        self.error_lbl.place(x=self.windowX / 2, y=(self.windowY / 4) * 3, anchor=CENTER)

    def update(self):

        widget_config = [self.lightRad, self.darkRad, self.localLoc, self.extLoc, self.theme_lbl, self.location_lbl,
                         self.path_lbl, self.path_btn, self.pin_lbl, self.pin_re_lbl, self.pin_ent.check_btn,
                         self.pin_re_ent.check_btn, self.confirm_btn, self.cancel_btn, self.error_lbl, self.backup_lbl,
                         self.backup_yes, self.backup_no, self.backup_path_btn, self.backup_path_lbl, self.warning_lbl]

        # Light Theme
        if self.v.get() == 0:
            self.master.configure(bg=self.window_bg_l)
            self.theme = 'light'

            # Background
            for w in widget_config:
                w['bg'] = self.window_bg_l
                w['fg'] = 'black'

                if w == self.error_lbl or w == self.warning_lbl:
                    w['fg'] = 'red'

                try:
                    w['selectcolor'] = 'white'
                    w['activebackground'] = self.window_bg_l
                except TclError:
                    pass

        # Dark Theme
        elif self.v.get() == 1:
            self.master.configure(bg=self.window_bg_d)
            self.theme = 'dark'

            for w in widget_config:
                w['bg'] = self.window_bg_d
                w['fg'] = 'white'

                if w == self.error_lbl or w == self.warning_lbl:
                    w['fg'] = 'red'

                try:
                    w['selectcolor'] = 'black'
                    w['activebackground'] = self.window_bg_d
                except TclError:
                    pass

        path_list = [self.path_lbl, self.path_ent, self.path_btn]

        # Local location
        if self.lv.get() == 0:

            for w in path_list:
                w.place_forget()

            self.pinY = 100

            self.backupY = 180

            self.place()

        # External location
        elif self.lv.get() == 1:

            self.pinY = 140

            self.backupY = 220

            # New path
            self.path_lbl.place(x=self.pathX, y=self.pathY)
            self.path_ent.place(x=self.pathX + 160, y=self.pathY + 3)
            self.path_btn.place(x=self.pathX + 390, y=self.pathY)

            self.place()

        # Backup No
        backup_list = [self.backup_path_lbl, self.backup_path_ent, self.backup_path_btn]
        if self.backup_var.get() == 1:
            self.backup_tog = 'no'
            for w in backup_list:
                w.place_forget()

            self.place()

        # Backup Yes
        elif self.backup_var.get() == 0:
            self.backup_tog = 'yes'
            self.backup_path_lbl.place(x=self.backupX, y=self.backupY + 40)
            self.backup_path_ent.place(x=self.backupX + 160, y=self.backupY + 43)
            self.backup_path_btn.place(x=self.backupX + 390, y=self.backupY + 40)
            self.place()

    def get_dir(self):
        self.default_dir = filedialog.askdirectory(initialdir=self.default_dir)
        self.path_ent.delete(0, END)
        self.path_ent.insert(0, self.default_dir + '/')

    def get_backup_dir(self):
        self.backup_dir = filedialog.askdirectory(initialdir=self.backup_dir)
        self.backup_path_ent.delete(0, END)
        self.backup_path_ent.insert(0, self.backup_dir + '/')

    def confirm(self):
        if self.pin_ent.get()[:1] == '0':
            self.error_lbl['text'] = "Your PIN cannot start with a 0."
        else:
            try:
                self.pin = int(self.pin_ent.get())
                self.pin_re = int(self.pin_re_ent.get())

                if self.pin == self.pin_re > 999:   # When PIN is successful
                    self.error_lbl['fg'] = 'green'
                    self.error_lbl['text'] = "PIN created successfully!"
                    # print(self.default_dir)
                    operator = db.Database(self.default_dir)
                    operator.setup(self.theme, str(self.pin), self.backup_dir, self.backup_tog)
                    self.master.destroy()
                    os.startfile('main.py')

                elif self.pin != self.pin_re:
                    self.error_lbl['text'] = "Your PINS do not match."
                elif self.pin < 0:
                    self.error_lbl['text'] = "Your PIN cannot be a negative number."
                elif self.pin == self.pin_re:
                    self.error_lbl['text'] = "Your PIN must be at least 4 digits."
            except ValueError:
                self.error_lbl['text'] = "Your PIN cannot have any letters."

    def quit(self):
        exit(0)


class Application(tk.Frame):
    def __init__(self, build=None, master=None):
        super().__init__(master)
        self.windowX = 1000
        self.windowY = 600
        self.window_bg = 'gray21'
        # Setup root and settings
        self.master = master
        self.master.configure(bg=self.window_bg)
        # self.master.geometry('{}x{}'.format(self.windowX, self.windowY))
        self.master.title('Password Manager ({})'.format(build))
        self.canvasPadX = 10
        self.canvasPadY = 10
        self.title_font = font.Font(size=12, underline=1)
        self.theme = 'dark'    # Two values (light or dark)
        self.theme_color_d = 'gray30'
        self.theme_color_l = 'gray90'

        with open('path.txt', 'r') as file:
            try:
                self.path = file.readlines()[0]
            except IndexError:
                self.path = ''
            file.close()

        self.operator = db.Database(self.path)

        # Start Pin Window
        self.pin_window = PinWindow(self.master)
        self.pin = self.pin_window.pin.get()

        # Logo Canvas
        self.c_logo = Canvas(master, width=250, height=150, highlightthickness=0)

        # Settings Canvas
        self.settingsAnchorX = 10
        self.settingsAnchorY = 10
        self.theme_var = IntVar()
        self.show_var = IntVar()
        self.backup_var = IntVar()
        if self.operator.get_theme() == "light":
            self.theme_var.set(1)
        elif self.operator.get_theme() == "dark":
            self.theme_var.set(0)
        if self.operator.get_backup_tog() == "yes":
            self.backup_var.set(1)
        elif self.operator.get_backup_tog() == "no":
            self.backup_var.set(0)
        if self.operator.get_hide_tog() == "yes":
            self.show_var.set(0)
        elif self.operator.get_hide_tog() == "no":
            self.show_var.set(1)
        self.c_settings = Canvas(master, width=200, height=150, highlightthickness=0)
        self.settings_title = Label(self.c_settings, text='Settings', font=self.title_font)
        self.theme_lbl = Label(self.c_settings, text='Theme:')
        self.darkRad = Radiobutton(self.c_settings, text="Dark", variable=self.theme_var, value=0, command=self.update)
        self.litRad = Radiobutton(self.c_settings, text="Light", variable=self.theme_var, value=1, command=self.update)
        self.show_lbl = Label(self.c_settings, text='Hide Passwords:')
        self.show_check = Checkbutton(self.c_settings, variable=self.show_var, command=self.load_database)
        self.backup_lbl = Label(self.c_settings, text="Auto Backup:")
        self.backup_check = Checkbutton(self.c_settings, variable=self.backup_var, command=self.toggle_backup)

        # Password Generator Canvas
        self.c_gen = Canvas(master, width=250, height=400, highlightthickness=0)
        self.c_gen_lbl = Label(self.c_gen, text="Password Generator", font=self.title_font)
        self.password = None
        self.cAnchorX = 10
        self.cAnchorY = 40
        self.lVar = tk.IntVar()
        self.lc = tk.Checkbutton(self.c_gen, text="Allow Lowercase (abcdefg)", variable=self.lVar)
        self.uVar = tk.IntVar()
        self.uc = tk.Checkbutton(self.c_gen, text="Allow Uppercase (ABCDEFG)", variable=self.uVar)
        self.nVar = tk.IntVar()
        self.nc = tk.Checkbutton(self.c_gen, text="Allow Numbers (123456)", variable=self.nVar)
        self.sVar = tk.IntVar()
        self.sc = tk.Checkbutton(self.c_gen, text="Allow Special Characters (!@#$%^&*)", variable=self.sVar)
        self.rVar = tk.IntVar()
        self.rc = tk.Checkbutton(self.c_gen, text="Allow Repeated Characters (AAaa11!!)", variable=self.rVar)
        self.cNum_lbl = Label(self.c_gen, text="Character Length:")
        self.cNum = tk.Spinbox(self.c_gen, from_=2, to=16, width=6)
        self.genBtn = tk.Button(self.c_gen, text="Generate", width=12, command=self.generate_password)
        self.copyBtn = tk.Button(self.c_gen, text="Copy", width=6, command=self.copy_password)
        self.entVar = tk.StringVar()
        self.passwordEnt = tk.Entry(self.c_gen, textvariable=self.entVar, width=20, state="readonly")
        self.copyLbl = Label(self.c_gen, text="Password copied!")
        self.use_btn = Button(self.c_gen, text='Use', width=6, command=self.use_generated_password)

        # Tool Canvas
        self.toolAnchorX = 10
        self.toolAnchorY = 10
        self.id_var = StringVar()
        self.site_var = StringVar()
        self.user_var = StringVar()
        self.pass_var = StringVar()
        self.c_tools = Canvas(master, width=200, height=400, highlightthickness=0)
        self.tool_title = Label(self.c_tools, text='Tools', font=self.title_font)
        self.tool_add = Button(self.c_tools, text='Add', width=6, command=self.add_to_database)
        self.tool_del = Button(self.c_tools, text='Delete', width=6, command=self.delete_from_database)
        self.tool_update = Button(self.c_tools, text='Update', width=6, command=self.update_database)
        self.tool_clear = Button(self.c_tools, text='Clear', width=6, command=self.clear_entries)
        self.tool_prev = Button(self.c_tools, text='Prev', width=6, command=self.listbox_prev)
        self.tool_next = Button(self.c_tools, text='Next', width=6, command=self.listbox_next)
        self.id_lbl = Label(self.c_tools, text='ID:')
        self.id_ent = Entry(self.c_tools, width=10, textvariable=self.id_var, state='readonly')
        self.site_lbl = Label(self.c_tools, text='Site:')
        self.site_ent = Entry(self.c_tools, width=29, textvariable=self.site_var)
        self.user_lbl = Label(self.c_tools, text='Username/Email:')
        self.user_ent = Entry(self.c_tools, width=20, textvariable=self.user_var)
        self.pass_lbl = Label(self.c_tools, text='Password:')
        self.pass_ent = Entry(self.c_tools, width=20, textvariable=self.pass_var)
        self.error_lbl = Label(self.c_tools, text='Please fill in all fields')
        self.copy_user_btn = Button(self.c_tools)
        self.copy_user_btn.config(text='Copy', width=6, command=lambda e=None: self.copy_user_pass('user'))
        self.copy_pass_btn = Button(self.c_tools)
        self.copy_pass_btn.config(text='Copy',  width=6, command=lambda e=None: self.copy_user_pass('pass'))
        self.tool_error = Label(self.c_tools)

        # Path Canvas
        self.pathAnchorX = 10
        self.pathAnchorY = 10
        self.backup_path = StringVar()
        self.backup_path.set(self.operator.get_backup_path())
        self.c_path = Canvas(master, width=500, height=150, highlightthickness=0)
        self.path_title = Label(self.c_path, text="Path To Database", font=self.title_font)
        self.path_lbl = Label(self.c_path, text="Path:")
        self.pathEntVar = StringVar()
        self.path_ent = Entry(self.c_path, width=55, state='readonly', textvariable=self.pathEntVar)
        self.path_btn = Button(self.c_path, text="Choose...", command=self.get_new_path)
        self.path_backup_lbl = Label(self.c_path, text="Backup:")
        self.path_backup_ent = Entry(self.c_path, width=55, state='readonly', textvariable=self.backup_path)
        self.path_backup_btn = Button(self.c_path, text="Choose...", command=self.set_backup_path)

        # Database Canvas
        self.dbAnchorX = 10
        self.dbAnchorY = 10
        self.act_val = 0
        self.opt_var = StringVar()
        self.keyword_var = StringVar()
        self.options_tup = ("All", "Site", "Username", "Password")
        self.c_db = Canvas(master, width=500, height=400, highlightthickness=0)
        self.db_title = Label(self.c_db, text='Database', font=self.title_font)
        self.db_refresh = Button(self.c_db, text='Refresh', width=10, command=self.load_database)
        self.db_listbox = Listbox(self.c_db, height=21, width=79)
        self.db_listbox.bind('<<ListboxSelect>>', lambda event=None: self.update())
        self.db_listbox.bind('<Button-1>', lambda event=None: self.mouse_select())
        self.db_search_btn = Button(self.c_db, text='Open Search', width=10, command=self.toggle_search)
        self.db_search_lbl = Label(self.c_db, text="Search:")
        self.db_search_ent = Entry(self.c_db, width=70, textvariable=self.keyword_var)
        self.keyword_var.trace_add('write', lambda name, index, mode, sv=self.keyword_var: self.load_database())
        # self.db_search_ent.bind('<Key>', self.key_press)
        self.db_search_by_lbl = Label(self.c_db, text="Search by:")
        self.db_search_opt = OptionMenu(self.c_db, self.opt_var, *self.options_tup)
        self.db_search_opt['highlightthickness'] = 0

        # Invoke functions
        self.place()
        self.load_database()
        self.toggle_backup()
        self.update()

    def update(self):
        canvas_list = [self.c_logo, self.c_settings, self.c_gen, self.c_tools, self.c_path, self.c_db]
        self.theme = self.operator.get_theme()

        # Do not include entries below
        widget_list = [self.c_gen_lbl, self.lc, self.uc, self.nc, self.sc, self.rc, self.cNum, self.cNum_lbl,
                       self.genBtn, self.copyBtn, self.copyLbl, self.path_title, self.path_lbl, self.path_backup_lbl,
                       self.path_btn, self.settings_title, self.theme_lbl, self.darkRad, self.litRad, self.db_title,
                       self.db_refresh, self.db_listbox, self.tool_title, self.tool_add, self.tool_del, self.tool_error,
                       self.tool_update, self.site_lbl, self.user_lbl, self.pass_lbl, self.tool_clear, self.tool_prev,
                       self.tool_next, self.error_lbl, self.id_lbl, self.show_lbl, self.show_check, self.use_btn,
                       self.db_search_btn, self.db_search_lbl, self.db_search_by_lbl, self.db_search_opt,
                       self.path_backup_btn, self.backup_lbl, self.backup_check, self.copy_user_btn, self.copy_pass_btn]

        # Changing Theme
        if self.theme_var.get() == 0:
            self.theme = 'dark'
        else:
            self.theme = 'light'

        self.operator.set_theme(self.theme)

        if self.theme == 'light':
            self.master['bg'] = 'gray75'

            for c in canvas_list:
                c['bg'] = self.theme_color_l
            for w in widget_list:
                w['bg'] = self.theme_color_l
                w['fg'] = 'black'
                if w == self.cNum:
                    w['buttonbackground'] = 'white'
                try:
                    w['selectcolor'] = 'white'
                    w['activebackground'] = self.theme_color_l
                except TclError:
                    pass

        elif self.theme == 'dark':
            self.master['bg'] = 'gray21'

            for c in canvas_list:
                c['bg'] = self.theme_color_d

            for w in widget_list:
                w['bg'] = self.theme_color_d
                w['fg'] = 'white'
                if w == self.cNum:
                    w['buttonbackground'] = 'black'
                try:
                    w['selectcolor'] = 'gray21'
                    w['activebackground'] = self.theme_color_d
                except TclError:
                    pass

        # Set path in entry
        if self.path == '':
            self.path = os.getcwd()
        self.pathEntVar.set(self.path)

        # Load anchor from listbox into entries
        try:
            self.id_var.set(self.db_listbox.get(self.db_listbox.curselection())[0])
            self.site_var.set(self.db_listbox.get(self.db_listbox.curselection())[1])
            self.user_var.set(self.db_listbox.get(self.db_listbox.curselection())[2])
            self.pass_var.set(self.db_listbox.get(self.db_listbox.curselection())[3])
        except IndexError and TclError:
            pass

    def place(self):
        self.c_logo.grid(padx=self.canvasPadX, pady=self.canvasPadY)

        # Settings
        self.c_settings.grid(padx=self.canvasPadX, pady=self.canvasPadY, row=0, column=1)
        self.settings_title.place(x=self.settingsAnchorX, y=self.settingsAnchorY)
        self.theme_lbl.place(x=self.settingsAnchorX, y=self.settingsAnchorY + 30)
        self.darkRad.place(x=self.settingsAnchorX + 110, y=self.settingsAnchorY + 30)
        self.litRad.place(x=self.settingsAnchorX + 50, y=self.settingsAnchorY + 30)
        self.show_lbl.place(x=self.settingsAnchorX, y=self.settingsAnchorY + 60)
        self.show_check.place(x=self.settingsAnchorX + 110, y=self.settingsAnchorY + 59)
        self.backup_lbl.place(x=self.settingsAnchorX, y=self.settingsAnchorY + 90)
        self.backup_check.place(x=self.settingsAnchorX + 110, y=self.settingsAnchorY + 89)

        # Password Gen
        self.c_gen.grid(padx=self.canvasPadX, pady=self.canvasPadY, row=1, column=0)
        self.c_gen_lbl.place(x=self.cAnchorX, y=self.cAnchorY - 30)
        self.lc.place(x=self.cAnchorX, y=self.cAnchorY)
        self.uc.place(x=self.cAnchorX, y=self.cAnchorY + 40)
        self.nc.place(x=self.cAnchorX, y=self.cAnchorY + 80)
        self.sc.place(x=self.cAnchorX, y=self.cAnchorY + 120)
        self.rc.place(x=self.cAnchorX, y=self.cAnchorY + 160)
        self.cNum_lbl.place(x=self.cAnchorX, y=self.cAnchorY + 200)
        self.cNum.place(x=self.cAnchorX + 120, y=self.cAnchorY + 202)
        self.genBtn.place(x=self.cAnchorX + 10, y=self.cAnchorY + 240)
        self.copyBtn.place(x=self.cAnchorX + 110, y=self.cAnchorY + 240)
        self.passwordEnt.place(x=self.cAnchorX + 115, y=self.cAnchorY + 285, anchor="center")
        self.use_btn.place(x=self.cAnchorX + 168, y=self.cAnchorY + 240)

        # Tools
        self.c_tools.grid(padx=self.canvasPadX, pady=self.canvasPadY, row=1, column=1)
        self.tool_title.place(x=self.toolAnchorX, y=self.toolAnchorY)
        self.tool_add.place(x=self.toolAnchorX, y=self.toolAnchorY + 40)
        self.tool_del.place(x=self.toolAnchorX + 60, y=self.toolAnchorY + 40)
        self.tool_update.place(x=self.toolAnchorX + 120, y=self.toolAnchorY + 40)
        self.tool_clear.place(x=self.toolAnchorX, y=self.toolAnchorY + 70)
        self.tool_prev.place(x=self.toolAnchorX + 60, y=self.toolAnchorY + 70)
        self.tool_next.place(x=self.toolAnchorX + 120, y=self.toolAnchorY + 70)
        self.id_lbl.place(x=self.toolAnchorX, y=self.toolAnchorY + 110)
        self.id_ent.place(x=self.toolAnchorX, y=self.toolAnchorY + 140)
        self.site_lbl.place(x=self.toolAnchorX, y=self.toolAnchorY + 165)
        self.site_ent.place(x=self.toolAnchorX, y=self.toolAnchorY + 195)
        self.user_lbl.place(x=self.toolAnchorX, y=self.toolAnchorY + 220)
        self.user_ent.place(x=self.toolAnchorX, y=self.toolAnchorY + 250)
        self.pass_lbl.place(x=self.toolAnchorX, y=self.toolAnchorY + 275)
        self.pass_ent.place(x=self.toolAnchorX, y=self.toolAnchorY + 305)
        self.copy_user_btn.place(x=self.toolAnchorX + 130, y=self.toolAnchorY + 247)
        self.copy_pass_btn.place(x=self.toolAnchorX + 130, y=self.toolAnchorY + 302)
        self.tool_error.place(x=self.toolAnchorX + 90, y=self.toolAnchorY + 355, anchor='center')

        # Path
        self.c_path.grid(padx=self.canvasPadX, pady=self.canvasPadY, row=0, column=2)
        self.path_title.place(x=self.pathAnchorX, y=self.pathAnchorY)
        self.path_lbl.place(x=self.pathAnchorX, y=self.pathAnchorY + 50)
        self.path_ent.place(x=self.pathAnchorX + 50, y=self.pathAnchorY + 52)
        self.path_btn.place(x=self.pathAnchorX + 390, y=self.pathAnchorY + 49)
        self.path_backup_lbl.place(x=self.pathAnchorX, y=self.pathAnchorY + 85)
        self.path_backup_ent.place(x=self.pathAnchorX + 50, y=self.pathAnchorY + 87)
        self.path_backup_btn.place(x=self.pathAnchorX + 390, y=self.pathAnchorY + 84)

        # Database
        self.c_db.grid(padx=self.canvasPadX, pady=self.canvasPadY, row=1, column=2)
        self.db_title.place(x=self.dbAnchorX, y=self.dbAnchorY)
        self.db_refresh.place(x=self.dbAnchorX + 400, y=self.dbAnchorY)
        self.db_listbox.place(x=self.dbAnchorX + 240, y=self.dbAnchorY + 380, anchor='s')
        self.db_search_btn.place(x=self.dbAnchorX + 315, y=self.dbAnchorY)

    def generate_password(self):
        self.password = PasswordGenUtility(self.lVar.get(), self.uVar.get(), self.nVar.get(), self.sVar.get(),
                                           self.rVar.get(), self.cNum.get())
        self.password.generate()
        self.entVar.set(self.password.finalPassword)

    def load_database(self):
        # Load Database into listbox
        self.db_listbox.delete(0, END)
        self.operator.open(self.pin)
        if self.db_search_btn['text'] == 'Open Search':
            if self.show_var.get() == 0:
                for row in self.operator.get_info():
                    self.db_listbox.insert(END, row)
            else:
                for row in self.operator.get_encrypted_info():
                    self.db_listbox.insert(END, row)
        elif self.db_search_btn['text'] == 'Close Search':
            if self.show_var.get() == 0:
                for row in self.operator.query(self.opt_var.get(), self.keyword_var.get()):
                    self.db_listbox.insert(END, row)
            else:
                for row in self.operator.encrypted_query(self.opt_var.get(), self.keyword_var.get()):
                    self.db_listbox.insert(END, row)

        if self.show_var.get() == 0:
            self.operator.set_hide_tog('no')
        elif self.show_var.get() == 1:
            self.operator.set_hide_tog('yes')

        self.update()

    def copy_password(self):
        if self.password is None:
            self.master.after(2000, self.clear_copy_text)
            self.copyLbl['text'] = 'Generate a password first!'
            self.copyLbl.place(x=self.cAnchorX + 115, y=self.cAnchorY + 320, anchor="center")
        else:
            self.copyLbl['text'] = 'Password copied!'
            self.master.after(2000, self.clear_copy_text)
            self.master.clipboard_clear()
            self.master.clipboard_append(self.password.finalPassword)
            self.copyLbl.place(x=self.cAnchorX + 115, y=self.cAnchorY + 320, anchor="center")

    def copy_user(self):
        if self.pass_var.get() == '':
            self.master.after(2000, self.clear_copy_text)

    def clear_copy_text(self):
        self.copyLbl.place_forget()
        self.tool_error.place_forget()

    def copy_user_pass(self, button_type):
        if button_type == 'user':
            if self.user_var.get() == '':
                self.master.after(2000, self.clear_copy_text)
                self.tool_error['text'] = "Fill in the 'Username' field"
                self.tool_error.place(x=self.toolAnchorX + 90, y=self.toolAnchorY + 355, anchor='center')
            else:
                self.tool_error['text'] = 'Password copied!'
                self.master.after(2000, self.clear_copy_text)
                self.master.clipboard_clear()
                self.master.clipboard_append(self.user_var.get())
                self.tool_error.place(x=self.toolAnchorX + 90, y=self.toolAnchorY + 355, anchor='center')
        elif button_type == "pass":
            if self.pass_var.get() == '':
                self.master.after(2000, self.clear_copy_text)
                self.tool_error['text'] = "Fill in the 'Password' field"
                self.tool_error.place(x=self.toolAnchorX + 90, y=self.toolAnchorY + 355, anchor='center')
            else:
                self.tool_error['text'] = 'Password copied!'
                self.master.after(2000, self.clear_copy_text)
                self.master.clipboard_clear()
                self.master.clipboard_append(self.pass_var.get())
                self.tool_error.place(x=self.toolAnchorX + 90, y=self.toolAnchorY + 355, anchor='center')

    def get_new_path(self):
        self.path = filedialog.askdirectory(initialdir=self.path) + '/'
        os.remove('path.txt')
        with open('path.txt', 'w+') as file:
            file.write(self.path)
            file.close()
        self.update()

    def forget_error(self):
        self.error_lbl.place_forget()

    def set_backup_path(self):
        self.backup_path.set(filedialog.askdirectory(initialdir=self.backup_path.get()))
        self.operator.set_backup_path(self.backup_path.get())

    def add_to_database(self):
        if 0 in (len(self.site_var.get()), len(self.user_var.get()), len(self.pass_var.get())):
            self.error_lbl['fg'] = 'firebrick3'
            self.error_lbl.place(x=100, y=375, anchor='center')
            self.master.after(2000, self.forget_error)
        else:
            self.operator.open(self.pin)
            self.operator.insert(self.site_var.get(), self.user_var.get(), self.pass_var.get())
            self.id_var.set('')
            self.site_var.set('')
            self.user_var.set('')
            self.pass_var.set('')
        self.load_database()

    def clear_entries(self):
        self.id_var.set('')
        self.site_var.set('')
        self.user_var.set('')
        self.pass_var.set('')

    def delete_from_database(self):
        # Load anchor from listbox into entries
        try:
            selection = self.db_listbox.get(self.db_listbox.curselection())
            self.operator.delete(selection[0])
        except IndexError and TclError:
            pass
        self.load_database()

    def update_database(self):
        self.operator.update(self.id_var.get(), self.site_var.get(), self.user_var.get(), self.pass_var.get())
        self.load_database()

    def listbox_next(self):
        self.db_listbox.selection_clear(0, END)
        if self.act_val >= self.db_listbox.index(END) - 1:
            pass
        else:
            self.act_val += 1
        self.db_listbox.select_set(self.act_val)
        self.update()

    def listbox_prev(self):
        self.db_listbox.selection_clear(0, END)
        if self.act_val == 0:
            pass
        else:
            self.act_val -= 1
        self.db_listbox.select_set(self.act_val)
        self.update()

    def mouse_select(self):
        self.act_val = self.db_listbox.index(ANCHOR)

    def use_generated_password(self):
        if self.password is None:
            self.master.after(2000, self.clear_copy_text)
            self.copyLbl['text'] = 'Generate a password first!'
            self.copyLbl.place(x=self.cAnchorX + 115, y=self.cAnchorY + 320, anchor="center")
        else:
            self.db_listbox.selection_clear(0, END)
            self.pass_var.set(self.password.finalPassword)
        self.update()

    def toggle_search(self):
        if self.db_search_btn['text'] == 'Open Search':
            self.db_listbox['height'] = 16
            self.db_search_lbl.place(x=self.dbAnchorX, y=self.dbAnchorY + 40)
            self.db_search_ent.place(x=self.dbAnchorX + 50, y=self.dbAnchorY + 40)
            self.db_search_by_lbl.place(x=self.dbAnchorX, y=self.dbAnchorY + 80)
            self.db_search_opt.place(x=self.dbAnchorX + 70, y=self.dbAnchorY + 78)

            self.db_search_btn['text'] = "Close Search"

        elif self.db_search_btn['text'] == "Close Search":
            self.db_listbox['height'] = 21
            self.db_search_lbl.place_forget()
            self.db_search_ent.place_forget()
            self.db_search_by_lbl.place_forget()
            self.db_search_opt.place_forget()
            self.keyword_var.set('')
            self.db_search_btn['text'] = "Open Search"

    def toggle_backup(self):
        if self.backup_var.get() == 0:
            self.path_backup_lbl.place_forget()
            self.path_backup_btn.place_forget()
            self.path_backup_ent.place_forget()
            self.master.protocol("WM_DELETE_WINDOW", self.quit)
            self.operator.set_backup_tog('no')
        else:
            self.path_backup_lbl.place(x=self.pathAnchorX, y=self.pathAnchorY + 85)
            self.path_backup_ent.place(x=self.pathAnchorX + 50, y=self.pathAnchorY + 87)
            self.path_backup_btn.place(x=self.pathAnchorX + 390, y=self.pathAnchorY + 84)
            self.master.protocol("WM_DELETE_WINDOW", self.backup_database)
            self.operator.set_backup_tog('yes')

    def backup_database(self):
        today = datetime.today().strftime('%Y-%m-%d-%H;%M;%S')
        # print(today)
        if not os.path.exists('{}/Backups/{}/'.format(self.backup_path.get(), today)):
            os.makedirs('{}/Backups/{}/'.format(self.backup_path.get(), today))
        shutil.copy('app.db', '{}/Backups/{}/app.db'.format(self.backup_path.get(), today))
        self.quit()

    def quit(self):
        exit(0)


class PinWindow(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.master.withdraw()
        self.windowX = 300
        self.windowY = 200
        self.geometry('{}x{}'.format(self.windowX, self.windowY))
        self.theme = None
        self.theme_color_l = 'gray90'
        self.theme_color_d = 'gray30'
        self.protocol("WM_DELETE_WINDOW", self.quit)

        with open('path.txt', 'r') as file:
            try:
                self.path = file.readlines()[0]
            except IndexError:
                self.path = ''
            file.close()

        self.operator = db.Database(self.path)

        self.pin_lbl = Label(self, text='Enter your pin:')
        self.pin = StringVar()
        self.pin_entry = SmartPasswordEntry(self, 'Show', width=10, textvariable=self.pin)
        self.pin_btn = Button(self, text="Enter", width=8, command=self.test_pin)
        self.bind('<Return>', lambda event=None: self.pin_btn.invoke())
        self.error_lbl = Label(self)

        self.place()
        self.update()

    def place(self):
        self.pin_lbl.place(x=self.windowX / 2, y=self.windowY / 2 - 20, anchor='center')
        self.pin_entry.place(x=self.windowX / 2, y=self.windowY / 2 + 10, anchor='center')
        self.pin_entry.place_toggle(x=self.windowX / 2 + 65, y=self.windowY / 2 + 10, anchor='center')
        self.pin_btn.place(x=self.windowX - 10, y=self.windowY - 10, anchor='se')
        self.error_lbl.place(x=self.windowX / 2, y=self.windowY / 2 + 40, anchor='center')

    def update(self):
        self.theme = self.operator.get_theme()

        widget_list = [self.pin_lbl, self.pin_btn, self.pin_entry.check_btn, self.error_lbl]

        if self.theme == 'light':
            self['bg'] = self.theme_color_l

            for w in widget_list:
                w['bg'] = self.theme_color_l
                w['fg'] = 'black'
                try:
                    w['selectcolor'] = 'white'
                    w['activebackground'] = self.theme_color_l
                except TclError:
                    pass

        elif self.theme == 'dark':
            self['bg'] = self.theme_color_d

            for w in widget_list:
                w['bg'] = self.theme_color_d
                w['fg'] = 'white'
                try:
                    w['selectcolor'] = 'gray21'
                    w['activebackground'] = self.theme_color_d
                except TclError:
                    pass

    def test_pin(self):
        self.operator.open(self.pin.get())
        if self.operator.open(self.pin.get()) == 'Pin Successful':
            self.error_lbl['fg'] = 'green'
            self.error_lbl['text'] = 'Pin Successful'
            self.destroy()
            self.master.deiconify()
        else:
            self.error_lbl['fg'] = 'red'
            self.error_lbl['text'] = 'Invalid Pin'

    def quit(self):
        exit(0)


while True:
    root = tk.Tk()
    if __name__ == "__main__":
        if run_setup():
            setup = SetupApp(master=root)
            setup.mainloop()
        else:
            app = Application(master=root, build=version)
            app.mainloop()
