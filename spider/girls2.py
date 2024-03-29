# -*- coding: UTF-8 -*-
import urllib.request
import lxml.html
import time
import os
import re
import ssl

context = ssl._create_unverified_context()


def serchIndex(name):
    url = 'https://www.nvshens.com/girl/search.aspx?name=' + name
    print(url)
    html = urllib.request.urlopen(url, context=context).read().decode('UTF-8')
    return html


def selectOne(html):
    tree = lxml.html.fromstring(html)
    one = tree.cssselect('#DataList1 > tr > td:nth-child(1) > li > div > a')[0]
    href = one.get('href')
    url = 'https://www.nvshens.com' + href + 'album/'
    print(url)
    html = urllib.request.urlopen(url, context=context).read().decode('UTF-8')
    print(html)
    return html


def findPageTotal(html):
    tree = lxml.html.fromstring(html)
    lis = tree.cssselect('#photo_list > ul > li')
    list = []
    for li in lis:
        url = li.cssselect('div.igalleryli_div > a')
        href = url[0].get('href')
        list.append(href)
    findimage_urls = set(list)
    print(findimage_urls)
    return findimage_urls


def dowmloadImage(image_url, filename):
    for i in range(len(image_url)):
        try:
            req = urllib.request.Request(image_url)
            req.add_header('User-Agent', 'chrome 4{}'.format(i))
            image_data = urllib.request.urlopen(req, context=context).read()
        except (urllib.request.HTTPError, urllib.request.URLError) as e:
            time.sleep(0.1)
            print(e)
            continue
        open(filename, 'wb').write(image_data)
        break


def mkdirByGallery(path):
    # 去除首位空格
    path = path.strip()
    path = '/Users/RandyZhang/Pictures/ZnGirls' + path
    # 这两个函数之间最大的区别是当父目录不存在的时候os.mkdir(path)
    # 不会创建，os.makedirs(path)
    # 则会创建父目录。
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
    return path


if __name__ != '__main__':
    # name = str(raw_input("name:"))
    name = str(input("name:"))
    html = serchIndex(name)
    html = selectOne(html)
    pages = findPageTotal(html)
    img_id = 1
    for page in pages:
        path = re.search(r'[0-9]+', page).group()
        path = mkdirByGallery(path)
        for i in range(1, 31):
            url = 'https://www.nvshens.com' + page + str(i) + '.html'
            html = urllib.request.urlopen(url, context=context).read().decode('UTF-8')
            tree = lxml.html.fromstring(html)
            title = tree.cssselect('head > title')[0].text
            if title.find(u"该页面未找到") != -1:
                break
            imgs = tree.cssselect('#hgallery > img')
            list = []
            for img in imgs:
                src = img.get('src')
                list.append(src)
            image_urls = set(list)
            image_id = 0
            for image_url in image_urls:
                dowmloadImage(image_url, path + '\\' + '2017-{}-{}-{}.jpg'.format(img_id, i, image_id))
                image_id += 1
        img_id += 1

if __name__ == '__main__':
    # page = str(raw_input("pageid:"))
    page = str(input("pageid:"))
    path = mkdirByGallery(page)
    for i in range(1, 31):
        url = 'https://www.nvshens.com/girl/' + page + '/' + str(i) + '.html'
        print(url)
        html = urllib.request.urlopen(url, context=context).read().decode('UTF-8')
        tree = lxml.html.fromstring(html)
        title = tree.cssselect('head > title')[0].text
        if title.find(u"该页面未找到") != -1:
            break
        imgs = tree.cssselect('#hgallery > img')
        list = []
        for img in imgs:
            src = img.get('src')
            list.append(src)
        image_urls = set(list)
        image_id = 0
        for image_url in image_urls:
            dowmloadImage(image_url, path + '\\' + '2017-{}-{}.jpg'.format(i, image_id))
            image_id += 1

if __name__ != '__main__':
    url = 'https://www.nvshens.com/gallery/meitui/'
    print(url)
    html = urllib.request.urlopen(url, context=context).read().decode('UTF-8')
    tree = lxml.html.fromstring(html)
    lis = tree.cssselect('#listdiv > ul > li')
    list = []
    for li in lis:
        url = li.cssselect('div.galleryli_div > a')
        href = url[0].get('href')
        list.append(href)
    findimage_urls = set(list)
    print(findimage_urls)
    print(len(findimage_urls))
