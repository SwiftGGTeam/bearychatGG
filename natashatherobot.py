# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import simplejson
import xml.etree.ElementTree as ET


bearychat_url = "https://hook.bearychat.com/=bw6L9/incoming/e36b4dfc18160d22f0327ce5fb74d5e6"


def is_article_h2(title):
    return lambda tag: tag.name == "h2" and tag.string and title == tag.string.lower()


def concat_data(title, data):
    result = "**%s 更新文章**\n" % (title, )
    for i in data:
        result += "> [%s](%s)\n" % (i.split("GGBREAK")[1], i.split("GGBREAK")[0])
    return result

def read_old_data(filename):   
    try:
        profile = open(filename, "r+")
    except:
        open(filename, 'a').close()
        profile = open(filename, "r+")
    old_data = []
    for i in profile.readlines():
        old_data.append(i.strip())
    profile.close()
    return old_data

def write_new_data(filename, data): 
    profile = open(filename, "a+")
    profile.write("\n".join(data) + "\n")
    profile.close()

def get_html_data():
    f = urllib.request.urlopen("http://natashatherobot.com/feed/")
    soup = ET.fromstring(f.read()) # .decode('gbk', 'ignore').encode('utf-8', 'ignore')
    return soup

def get_full_data(html, tag):
    full_data = []
    items = get_html_data()[0].findall(".//%s" % (tag, ))
    for item in items:
        full_data.append(item.findall("./link")[0].text.strip() + "GGBREAK" +item.findall("./title")[0].text.strip())
    return full_data

def cal_new_data(old_data, full_data):
    return set(full_data) - set(old_data)

def check():
    old_data = read_old_data("natashatherobot_profile")
    html = get_html_data()
    new_data = cal_new_data(old_data, get_full_data(html, "item"))
    if new_data:
        send_data = {"text": concat_data("Natasha The Robot", new_data), "markdown": True}
        params = simplejson.JSONEncoder().encode(send_data).encode('utf8')
        req = urllib.request.Request(bearychat_url, data=params, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        write_new_data("natashatherobot_profile", new_data)

check()
