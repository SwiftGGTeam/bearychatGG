# -*- coding: utf-8 -*-
from utils import *
import sys

def ic_get_full_data(html, class_):
    content_div = html.find("div", class_=class_)
    full_data = []
    for a in content_div.find_all("a"):
        full_data.append(a["href"].strip().replace(u'\xa0', u' ') + "GGBREAK" + a.get_text().strip().replace(u'\xa0', u' '))
    return full_data

def th_get_full_data(html, title):
    titles = html.find_all("h2", title)
    full_data = []
    for title in titles:
        full_data.append(title.a["href"].strip().replace(u'\xa0', u' ') + "GGBREAK" + title.a.get_text().strip().replace(u'\xa0', u' '))
    return full_data

def jbs_get_full_data(html, tag):
    articles = html.find_all(tag)
    full_data = []
    for article in articles:
        full_data.append(article.a["href"].strip().replace(u'\xa0', u' ') + "GGBREAK" + article.a.h1.get_text().strip().replace(u'\xa0', u' '))
    return full_data

def ts_get_full_data(html, class_):
    posts = html.find_all("li", class_=class_)
    full_data = []
    for post in posts:
        full_data.append(post.h2.a["href"].strip().replace(u'\xa0', u' ') + "GGBREAK" + post.h2.a.get_text().strip().replace(u'\xa0', u' '))
    return full_data

def o_get_full_data(html, tag):
    full_data = []
    items = [item for item in html if item.tag.endswith("entry")]
    for item in items:
        for i in item:
            if i.tag.endswith("title"):
                title = i.text
                break
        for i in item:
            if i.tag.endswith("link"):
                link = i.attrib["href"]
                break
        full_data.append(link.strip().replace(u'\xa0', u' ') + "GGBREAK" + title.strip().replace(u'\xa0', u' '))
    return full_data

authorized = [
    {
        "store_file_name": "natashatherobot_profile",
        "url": "http://natashatherobot.com/feed/",
        "msg_title": "Natasha The Robot",
        "typeis": "rss"
    },
    {
        "store_file_name": "swiftandpainless_profile",
        "url": "http://swiftandpainless.com/feed/",
        "msg_title": "Swift and Painless",
        "typeis": "rss"
    },
    {
        "store_file_name": "nsblog_profile",
        "url": "https://www.mikeash.com/pyblog/rss.py",
        "msg_title": "NSBlog(mikeash.com)",
        "typeis": "rss"
    },
    {
        "store_file_name": "ericasadun_profile",
        "url": "http://ericasadun.com/feed/",
        "msg_title": "Erica Sadun",
        "typeis": "rss"
    },
    {
        "store_file_name": "ioscreator_profile",
        "url": "http://www.ioscreator.com/swift/",
        "msg_title": "IOSCREATOR",
        "anchors": ["sqs-block-content"],
        "get_full_data": ic_get_full_data,
        "typeis": "html"
    },
    {
        "store_file_name": "appventure_profile",
        "url": "http://appventure.me/rss-feed",
        "msg_title": "APPVENTURE",
        "typeis": "rss"
    },
    {
        "store_file_name": "szulctomasz_profile",
        "url": "http://szulctomasz.com/",
        "msg_title": "Tomasz Szulc",
        "anchors": ["post"],
        "get_full_data": ts_get_full_data,
        "typeis": "html"
    },
    {
        "store_file_name": "thomashanning_profile",
        "url": "http://www.thomashanning.com/category/swift/",
        "msg_title": "THOMAS HANNING",
        "anchors": ["entry-title"],
        "get_full_data": th_get_full_data,
        "typeis": "html"
    },
    {
        "store_file_name": "ole_profile",
        "url": "http://oleb.net/blog/atom.xml",
        "msg_title": "Ole Begemann",
        "cus_get_full_data": o_get_full_data,
        "typeis": "rss"
    },
    {
        "store_file_name": "raj_profile",
        "url": "http://rajkandathi.com/category/ios/",
        "msg_title": "Raj Kandathi",
        "anchors": ["entry-title"],
        "get_full_data": th_get_full_data,
        "typeis": "html"
    },
    {
        "store_file_name": "chrunchy_profile",
        "url": "http://alisoftware.github.io/feed.xml",
        "msg_title": "Crunchy Development",
        "typeis": "rss"
    },
    {
        "store_file_name": "jameson_profile",
        "url": "http://jamesonquave.com/blog/feed/",
        "msg_title": "JamesonQuave.com",
        "typeis": "rss"
    },
    {
        "store_file_name": "jacob_profile",
        "url": "http://bandes-stor.ch/archive/",
        "msg_title": "Jacob Bandes-Storch",
        "anchors": ["article"],
        "get_full_data": jbs_get_full_data,
        "typeis": "html"
    },
]

def ray_get_full_data(html, title):
    target_elem = html.find(is_article_h2(title))
    while target_elem.name != "ul":
        target_elem = target_elem.next_sibling
    full_data = []
    for li in target_elem.children:
        full_data.append(li.a["href"].strip().replace(u'\xa0', u' ') + "GGBREAK" + li.a.get_text().strip().replace(u'\xa0', u' '))
    return full_data

def tb_get_full_data(html, title):
    titles = html.find_all("h2", title)
    full_data = []
    for title in titles:
        full_data.append(title.a["href"].strip().replace(u'\xa0', u' ') + "GGBREAK" + title.a.get_text().strip().replace(u'\xa0', u' '))
    return full_data

unauthorized = [
    {
        "store_file_name": "raywenderlich_profile",
        "url": "http://www.raywenderlich.com/category/swift",
        "msg_title": "Ray Wenderlich",
        "anchors": ["articles", "tutorials"],
        "get_full_data": ray_get_full_data,
        "typeis": "html"
    },
    {
        "store_file_name": "appleblog_profile",
        "url": "https://developer.apple.com/swift/blog/news.rss",
        "msg_title": "苹果官方博客",
        "typeis": "rss"
    },
    {
        "store_file_name": "thoughtbot_profile",
        "url": "https://robots.thoughtbot.com/tags/swift",
        "msg_title": "thoughtbot",
        "anchors": ["mini-post-title"],
        "get_full_data": tb_get_full_data,
        "typeis": "html"
    },
]

for i in authorized + unauthorized:
    if i["typeis"] == "rss":
        check_rss(i)
    elif i["typeis"] == "html":
        check_html(i)
