# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import codecs
import re

from scrapy.conf import settings
import pymysql
import requests

import oss2


class MyfendoPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(host='120.78.136.232', port=3306, user='root', passwd='123', db='meinvha', charset='utf8')
        self.cursor = self.conn.cursor()

        self.auth = oss2.Auth('LTAI6KRnoV0ZfBJH', 'VKYiSOyfZJ7ojrJZpy3u5PrCLrKWHz')
        self.bucket = oss2.Bucket(self.auth, 'oss-cn-shenzhen.aliyuncs.com', 'sayid0924')

        # def close_spider(self, spider):
        #     self.conn.close()


    def process_item(self, item, spider):

        meinvha_title = item['title']
        img_url = item['imgUrl']
        dir = item['dir']
        img_name = item['img_name']



        meinvha_title = meinvha_title.replace('<h>', " ").replace('</h>', " ").replace('\\', " ").replace('/',
                                                                                                          " ").replace(
            '*', " ").replace(':', " ").replace('?', " ").replace('"', " ").replace('<', " ").replace('>', " ").replace(
            '|', " ").replace('(', '').replace(')','').replace(r'\d+','')

        meinvha_title = meinvha_title.strip()

        if not os.path.exists(dir):
            os.makedirs(dir)
        Dir_Ptah = os.path.abspath(dir)

        ailiyunPath = 'meinvha' + "/" + dir

        conut = self.cursor.execute("select * from dir where dir = '%s'" % dir)

        self.cursor.fetchall()
        if conut == 0:
            sql = "insert into dir(dir) values(%s)"
            params = (dir)
            self.cursor.execute(sql, params)
        else:
            pass

        meinvha_title = meinvha_title.strip()
        if not os.path.exists(meinvha_title):

            try:

                os.makedirs(Dir_Ptah + "/" + meinvha_title)

            except OSError:

                pass


        conut = self.cursor.execute("select * from title where title= '%s'" % meinvha_title)
        self.cursor.fetchall()
        ss = os.path.abspath(Dir_Ptah+ "/" + meinvha_title)

        # ailiyunPath=ailiyunPath+ "/" + bookname
        # ailiyunImgPath = ailiyunPath + "/" + bookname + '.jpg'

        if conut == 0:

            self.cursor.execute("select * from dir where dir= '%s'" % dir)
            re = self.cursor.fetchall()
            dir_id = re[0][0]
            sql = "insert into title(title, dir_id) values(%s,%s)"
            params = (meinvha_title, dir_id)
            self.cursor.execute(sql, params)

        else:

            pass



        if len(img_url)> 1:
            i =0
            for url in img_url:

                if url.startswith('http'):
                    url = url
                else:
                    url = 'http://www.meinvha.com' + url

                ir = requests.get(url)
                if ir.status_code == 200:

                    self.cursor.execute("select * from title where title= '%s'" % meinvha_title)
                    re = self.cursor.fetchall()
                    title_id = re[0][0]
                    sql = "insert into img_url(img_url, title_id) values(%s,%s)"
                    params = (url, title_id)
                    self.cursor.execute(sql, params)



        else:
            img_url = img_url[0]

            if img_url.startswith('http'):
                img_url = img_url
            else:
                img_url = 'http://www.meinvha.com' + img_url

            ir = requests.get(img_url)

            if ir.status_code == 200:

                self.cursor.execute("select * from title where title= '%s'" % meinvha_title)
                re = self.cursor.fetchall()
                title_id = re[0][0]
                sql = "insert into img_url(img_url, title_id) values(%s,%s)"
                params = (img_url, title_id)
                self.cursor.execute(sql, params)

                # open(ss + "\\" + str(img_name)+'.jpg', 'wb').write(ir.content)
                # imgFilePath = ss + "\\" + img_url
                # self.bucket.put_object_from_file(ailiyunImgPath, imgFilePath)

            else:

                pass

            #     self.cursor.execute("select * from book_list where book_list= '%s'" % book_List)
            #     re = self.cursor.fetchall()
            #     book_list_id = re[0][0]
            #     sql = "insert into book_name(book_name, book_list_id,book_author,book_introduced,img_url,img_path) values(%s,%s,%s,%s,%s,%s)"
            #     params = (bookname, book_list_id, author,introduced, imgUrl, ailiyunImgPath)
            #     self.cursor.execute(sql, params)
            #
            # else:
            #     pass
            # booktitle= booktitle.replace('\\', " ").replace('/', " ").replace('*', " ").replace(':', " ").replace('?', " ").replace('"', " ").replace('<', " ").replace('>', " ").replace('|', " ")
            #
            # book_Path = ss + "/" + booktitle + '.text'
            # book_Path.encode("utf-8")
            #
            # filename = codecs.open(book_Path, 'wb', encoding="utf-8")
            # filename.write(content)
            #
            # filePath = os.path.abspath(filename.name)
            # ailiyunFeliPath = ailiyunPath + "/" + booktitle + '.text'
            # self.bucket.put_object_from_file(ailiyunFeliPath, filePath)
            # conut = self.cursor.execute("select * from book where book_title= '%s'" % booktitle)
            # self.cursor.fetchall()
            #
            # if conut == 0:
            #     self.cursor.execute("select * from book_name where book_name= '%s'" % bookname)
            #     re = self.cursor.fetchall()
            #     book_name_id = re[0][0]
            #     sql = "insert into book(book_title, book_url,book_path,book_number,book_name_id) values(%s,%s,%s,%s,%s)"
            #     params = (booktitle, url, ailiyunFeliPath, bookdirnumber, book_name_id)
            #     self.cursor.execute(sql, params)
            #
            #
            # else:
            #     pass
        self.conn.commit()
        return item
