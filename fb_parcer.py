from urllib.request import urlparse
from urllib.parse import parse_qs
from bs4 import BeautifulSoup
import requests


def get_bs(html):
    return BeautifulSoup(html, 'html.parser')

def get_default_params(soup):

    def not_empty(tag):
        return False if tag is not None else True

    params = {}
    form = soup.find('form') # get login form
    inputs = form.find_all('input', not_empty) # get inputs form

    for input in inputs:
        if input['type'] != 'submit' and input.has_attr('value'):
            params[input['name']] = input.get('value')

    return params

def get_fb_dtsg_token(soup):
    return soup.find('input', attrs={'name':'fb_dtsg'})['value']

def get_fb_logout(soup):

    def is_logout(href):
        return href and 'logout.php' in href

    result = soup.find(href=is_logout)
    return result['href'][1:] if result else ''

def get_fb_friends_next(soup):

    def is_next(href):
        return href and 'friends/center/friends' in href

    result = soup.find(href=is_next)
    return result['href'][1:] if result else ''

def get_fb_friends(soup):
    result = []
    div = soup.find(id='friends_center_main')
    for a in div.find_all(href=True)[1:-1]:
        url = urlparse(a['href'])
        qs = parse_qs(url.query)
        user = (a.text,qs['uid'][0])
        result.append(user)

    return result

def print_title():
    f = open('title.txt', 'r')
    file_contents = f.read()
    print (file_contents)
    f.close()
