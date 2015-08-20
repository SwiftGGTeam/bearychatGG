# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import simplejson



anchor_titles = ["articles", "tutorials"]
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
    f = urllib.request.urlopen("http://www.raywenderlich.com/category/swift")
    soup = BeautifulSoup(f.read(), "html.parser")  # .decode('gbk', 'ignore').encode('utf-8', 'ignore')
    return soup

def get_full_data(html, title):
    target_elem = html.find(is_article_h2(title))
    while target_elem.name != "ul":
        target_elem = target_elem.next_sibling
    full_data = []
    for li in target_elem.children:
        full_data.append(li.a["href"] + "GGBREAK" + li.a.string)
    return full_data

def cal_new_data(old_data, full_data):
    return set(full_data) - set(old_data)

def check():
    old_data = read_old_data("raywenderlich_profile")
    html = get_html_data()
    new_data = []
    for title in anchor_titles:
        new_data += cal_new_data(old_data, get_full_data(html, title))
    if new_data:
        send_data = {"text": concat_data("Ray Wenderlich", new_data), "markdown": True}
        params = simplejson.JSONEncoder().encode(send_data).encode('utf8')
        req = urllib.request.Request(bearychat_url, data=params, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        write_new_data("raywenderlich_profile", new_data)

check()
