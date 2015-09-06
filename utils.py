# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import simplejson
import xml.etree.ElementTree as ET
import collections
import functools


class memoized(object):
   '''Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   '''
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      '''Return the function's docstring.'''
      return self.func.__doc__
   def __get__(self, obj, objtype):
      '''Support instance methods.'''
      return functools.partial(self.__call__, obj)


bearychat_url = "https://hook.bearychat.com/=bw6L9/incoming/e36b4dfc18160d22f0327ce5fb74d5e6"

def is_article_h2(title):
    return lambda tag: tag.name == "h2" and tag.get_text() and title == tag.get_text().lower()

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


def cal_new_data(old_data, full_data):
    return set(full_data) - set(old_data)


def check_rss(target):

    (store_file_name, url, msg_title) = (target["store_file_name"], target["url"], target["msg_title"])

    @memoized
    def get_html_data(url):
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        req = urllib.request.Request(url, headers={'User-Agent': user_agent})
        f = urllib.request.urlopen(req)
        soup = ET.fromstring(f.read()) # 
        
        return soup

    def get_full_data(html, tag):
        full_data = []
        items = html[0].findall(".//%s" % (tag, ))
        for item in items:
            full_data.append(item.findall("./link")[0].text.strip().replace(u'\xa0', u' ') + "GGBREAK" +item.findall("./title")[0].text.strip().replace(u'\xa0', u' '))
        return full_data

    if "cus_get_full_data" in target and target["cus_get_full_data"]:
      get_full_data = target["cus_get_full_data"]
    old_data = read_old_data(store_file_name)
    html = get_html_data(url)
    if "tag" in target:
      tag = target["tag"]
    else:
      tag = "item"
    new_data = cal_new_data(old_data, get_full_data(html, tag))
    if new_data:
        send_data = {"text": concat_data(msg_title, new_data), "markdown": True}
        params = simplejson.JSONEncoder().encode(send_data).encode('utf8')
        req = urllib.request.Request(bearychat_url, data=params, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        write_new_data(store_file_name, new_data)


def check_html(target):

    (store_file_name, url, msg_title, anchors, get_full_data) = (target["store_file_name"], target["url"], target["msg_title"], target["anchors"], target["get_full_data"])

    if type(anchors) != type([]):
        anchors = [anchors]

    @memoized
    def get_html_data(url):
      user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
      req = urllib.request.Request(url, headers={'User-Agent': user_agent})
      f = urllib.request.urlopen(req)
      soup = BeautifulSoup(f.read(), "html.parser")  # .decode('gbk', 'ignore').encode('utf-8', 'ignore')
      return soup

    if "cus_get_html_data" in target and target["cus_get_html_data"]:
      get_html_data = target["cus_get_html_data"]
    old_data = read_old_data(store_file_name)
    html = get_html_data(url)
    new_data = []
    for title in anchors:
        new_data += cal_new_data(old_data, get_full_data(html, title))
    if new_data:
        send_data = {"text": concat_data(msg_title, new_data), "markdown": True}
        params = simplejson.JSONEncoder().encode(send_data).encode('utf8')
        req = urllib.request.Request(bearychat_url, data=params, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        write_new_data(store_file_name, new_data)
