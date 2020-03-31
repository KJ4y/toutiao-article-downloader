from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import os
import json


class Setting(Toplevel):
    def __init__(self, master=None, cookie=None, path=None):
        Toplevel.__init__(self, master)

        self.style = ttk.Style(self).theme_use('clam')

        self.title('设置')
        self.resizable(width=False, height=False)

        self.cookie = StringVar()
        self.cookie.set(cookie)

        self.path = StringVar()
        self.path.set(path)

        self.setting_cookie()
        self.save_as()
        self.save_button()

    def setting_cookie(self):
        frame = Frame(self)
        frame.pack(anchor=NW)

        Label(frame, text="Cookie:        ").grid(row=0, column=0)
        ttk.Entry(frame, textvariable=self.cookie).grid(row=0, column=1)

    def save_as(self):
        frame = Frame(self)
        frame.pack(anchor=NW)

        Label(frame, text="文章保存路径:").grid(row=0, column=0)
        ttk.Entry(frame, textvariable=self.path).grid(row=0, column=1)
        Button(frame, text="路径选择", command=self.select_path).grid(
            row=0, column=2, padx=5)

    def save_button(self):
        frame = Frame(self)
        frame.pack(padx=10, pady=10)

        ttk.Button(frame, text="保存设置", command=self.save_setting).grid(
            row=0, column=2)

    def select_path(self):
        path_ = askdirectory()
        self.path.set(path_) if path_ != '' else self.path.set('')

    def save_setting(self):
        cookie = self.cookie.get()
        if cookie != '':
            config = {
                'cookie': cookie,
                'save_doxc_path': self.path.get()
            }
            with open('config.json', 'w') as f:
                json.dump(config, f)
            self.destroy()
        else:
            messagebox.showinfo("Basic Example", "cookie不能为空")
