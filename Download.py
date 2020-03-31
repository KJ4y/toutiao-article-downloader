from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
import time
import json

from Article import Article


class Download(Toplevel):
    def __init__(self, master=None, date=None):
        Toplevel.__init__(self, master)
        self.style = ttk.Style(self).theme_use('clam')

        self.date = date

        with open('config.json', 'r') as f:
            config = json.load(f)

        cookie = config['cookie']
        self.article = Article(cookie=cookie)

        self.article.date = self.date
        self.article.get_list()

        self.title('青云计划文章列表（{}-文章数：{}）'.format(
            self.article.date, len(self.article.title_list)))
        self.resizable(width=True, height=False)

        self.frame_list()
        self.frame_button()

    # 文章列表
    def frame_list(self):
        frame_out = Frame(self)
        frame_out.pack(fill="both")

        self.canvas = Canvas(frame_out, borderwidth=0, width=600)
        self.frame = Frame(self.canvas)
        self.frame.pack()
        vsb = Scrollbar(frame_out, orient="vertical",
                        command=self.canvas.yview)
        vsb.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="frame")
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.frame.bind("<Configure>", self.frame_configure)

        self.v = []
        for item in self.article.title_list:
            self.v.append(IntVar())
            self.list = Checkbutton(
                self.frame, text=item, font=('微软雅黑', 12), variable=self.v[-1], command=self.tick_article)
            self.list.pack(anchor=W)
    # 绑定画布

    def frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    # 绑定鼠标滚轮

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # 按钮框架

    def frame_button(self):
        frame_button = Frame(self)
        frame_button.pack(side="bottom", fill="x", padx=10, pady=10)
        ttk.Button(frame_button, text="文章转换为docx格式",
                   command=self.html2docx).pack(side="right", fill="both", padx=10)
        ttk.Button(frame_button, text="勾选文章一键下载",
                   command=self.download_article).pack(side="right", fill="both", padx=10)
        ttk.Button(frame_button, text="勾选《》文章",
                   command=self.tick_other).pack(side="right", fill="both", padx=10)
        ttk.Button(frame_button, text="勾选 王者荣耀 文章",
                   command=self.tick_king).pack(side="right", fill="both", padx=10)

   # 勾选文章内容
    def tick_article(self):
        self.article.download_list.clear()
        for item in self.v:
            if item.get() == 1:
                id = self.v.index(item)
                self.article.download_list.append(self.article.id_list[id])

    # 多线程下载文章
    def download_article(self):
        for item in self.article.download_list:
            t = threading.Thread(target=self.start_download, args=(item,))
            t.start()
        t.join()
        tips = messagebox.askokcancel('提示', '勾选文章已下载完成，是否立即转换为docx格式？')
        self.article.html2docx() if tips == True else None

    # 开始下载并转换为word文档
    def start_download(self, item):
        self.article.id = item
        self.article.get_article()
        self.article.save_as_html()

    # 勾选带《》文章
    def tick_other(self):
        for item in self.article.title_list:
            if '《' in item:
                index = self.article.title_list.index(item)
                if self.v[index].get() == 0:
                    self.v[index].set(1)
                    self.tick_article()
                else:
                    self.v[index].set(0)
                    self.tick_article()

    # 勾选带王者荣耀的文章
    def tick_king(self):
        for item in self.article.title_list:
            if '王者荣耀' in item:
                index = self.article.title_list.index(item)
                if self.v[index].get() == 0:
                    self.v[index].set(1)
                    self.tick_article()
                else:
                    self.v[index].set(0)
                    self.tick_article()

    def html2docx(self):
        self.article.html2docx()
        self.destroy()
