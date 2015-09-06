# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import simplejson



anchor_titles = ["articles", "tutorials"]
bearychat_url = "https://hook.bearychat.com/=bw6L9/incoming/e36b4dfc18160d22f0327ce5fb74d5e6"

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
    result = profile.read()
    profile.close()
    return result

def write_new_data(filename, data): 
    profile = open(filename, "w")
    profile.write(str(data))
    profile.close()

def get_html_data(issue_id):
    try:
        f = urllib.request.urlopen("http://swiftsandbox.io/issues/%s#start" % (issue_id, ))
    except:
        exit(0)
    soup = BeautifulSoup(f.read(), "html.parser")  # .decode('gbk', 'ignore').encode('utf-8', 'ignore')
    return soup

def get_full_data(html, title):
    target_elem = html.find("span", string=title).parent.parent

    full_data = []
    for item in target_elem.findAll("h3"):
        try:
            full_data.append(item.a["href"] + "GGBREAK" + item.a.string)
        except:
            pass
    return full_data

def check():
    old_data = read_old_data("swiftsandbox_profile") or 1
    html = get_html_data(int(old_data) + 1)
    new_data = get_full_data(html, "TOPICS IN SWIFT")
    if new_data:
        send_data = {"text": concat_data("Swift Sandbox", new_data), "markdown": True}
        params = simplejson.JSONEncoder().encode(send_data).encode('utf8')
        req = urllib.request.Request(bearychat_url, data=params, headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        write_new_data("swiftsandbox_profile", int(old_data) + 1)

check()
