from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
import time
import json

from Setting import Setting
from Download import Download


class Main(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(padx=10, pady=10)

        ttk.Style(self).theme_use('clam')
        self.master.title('今日头条文章下载器')
        self.master.resizable(width=False, height=False)

        # UI界面
        self.frame_title()
        self.frame_calendar()
        self.frame_button()

    # 标题框架
    def frame_title(self):
        frame = Frame(self)
        frame.pack()
        Label(frame, text='今日头条文章下载器',
              font=('微软雅黑', 16), width=25).pack()

    # 日历框架
    def frame_calendar(self):
        frame = Frame(self)
        frame.pack()
        year = time.strftime("%Y", time.localtime())
        month = time.strftime("%m", time.localtime())
        day = time.strftime("%d", time.localtime())
        self.cal = Calendar(frame,
                            font=('微软雅黑', 12), selectmode='day', year=int(year), month=int(month), day=int(day))
        self.cal.pack(fill="both", expand=True, padx=10, pady=10)

    # 按钮框架
    def frame_button(self):
        frame = Frame(self)
        frame.pack()
        ttk.Button(frame, text="设置", command=self.save_setting).grid(
            row=1, column=1)
        Label(frame, text=' ', width=17, height=2).grid(
            row=1, column=2)
        ttk.Button(frame, text="获取文章列表", command=self.get_list).grid(
            row=1, column=3)

    def save_setting(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        cookie = config['cookie']
        path = config['save_doxc_path']
        setting = Setting(cookie=cookie, path=path)

    def get_list(self):
        download = Download(date=str(self.cal.selection_get()))

if __name__ == "__main__":
    main = Main()
    main.mainloop()
