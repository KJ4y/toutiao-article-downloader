
import pypandoc
import requests
import execjs
import re
import os
import json
import threading
from tkinter import messagebox


class Article:
    def __init__(self, cookie=None):
        self.ua = 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36(KHTML, like Gecko) Chrome/80.0.3987.122 Mobile Safari/537.36'
        self.date = None
        self.cookie = cookie

        self.list = []
        self.title_list = []
        self.id_list = []

        self.id = None
        self.article = None
        self.new_title = None

        self.target_path = None

        self.download_list = []

    # 请求获取数据
    def request(self, url, params, host):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': host,
            'cookie': self.cookie,
            'user-agent': self.ua,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest'
        }
        with requests.session() as session:
            with session.get(url, params=params, headers=headers) as response:
                html = response.json()
                data = html['data']
                return data

    # 获取文章列表
    def get_list(self):
        self.list = []
        self.id_list = []
        self.title_list = []

        list_url = 'https://mp.toutiao.com/api/high_article_award_list_detail'
        params = {'award_list_date': self.date,
                  'check_date': self.date}
        host = 'mp.toutiao.com'
        self.list = self.request(list_url, params, host)
        self.extract_list()

    # 提取列表数据
    def extract_list(self):
        for item in self.list:
            self.title_list.append(item['title'])
            self.id_list.append(item['item_id'])

    # 获取带_signature的params
    def get_signature(self):
        with open('./signature.js') as f:
            ctx = execjs.compile(f.read())
        _signature = ctx.call('get_signature', self.ua)
        params = {
            '_signature': '',
            'i': ''
        }
        params['_signature'] = _signature
        params['i'] = self.id
        return params

    # 获取文章内容
    def get_article(self):
        article_url = 'https://m.toutiao.com/i' + str(self.id) + '/info/'
        params = self.get_signature()
        host = 'm.toutiao.com'
        self.data = self.request(article_url, params, host)
        self.extract_article()

    # 提取文章数据
    def extract_article(self):
        title = self.data['title']
        source = self.data['source']
        content = self.data['content']

        self.article = '<head><meta charset="UTF-8"><meta name="author" content=' + \
            source + '><title>' + title + '</title></head>' + content

        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        self.new_title = re.sub(rstr, "_", title)

    # 保存路径
    def create_path(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.target_path = config['save_doxc_path'].replace("/", "\\")
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)

    # 保存文章内容为html
    def save_as_html(self):
        self.create_path()
        if not os.path.exists(self.target_path + os.path.sep + self.new_title + '.docx'):
            with open(self.target_path + os.path.sep + self.new_title + '.html', 'wb+') as f:
                f.write(self.article.encode('utf-8'))
                f.close()
        else:
            print('此文档已存在')

    # 将html文章内容转为docx格式
    def html2docx(self):
        path = r"C:\Program Files\Pandoc\pandoc"
        os.environ.setdefault(
            'PYPANDOC_PANDOC', path)

        self.create_path()

        g = os.walk(self.target_path)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                if os.path.splitext(file_name)[-1] == ".html":
                    input_file = os.path.join(path, file_name)
                    extra_args = ['--reference-doc', 'custom-reference.docx']
                    output_file = os.path.join(
                        path, file_name).replace(".html", ".docx")
                    t = threading.Thread(target=self.start_download, args=(
                        input_file, extra_args, output_file))
                    t.start()
        t.join()
        messagebox.showinfo("Basic Example", "文章转换完成")

    def start_download(self, input_file, extra_args, output_file):
        output = pypandoc.convert_file(
            input_file, 'docx', extra_args=extra_args, outputfile=output_file)
        os.remove(input_file)
