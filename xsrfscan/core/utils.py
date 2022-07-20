from urllib.parse import urlparse
import json


user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']

globalVar = {}

def validate(url):
    # improvement needed to this function
    scheme = urlparse(url).scheme
    if scheme == "http" or scheme == "https":
        return url
    else:
        scheme = "https"
        return scheme + "://" + url


def enable_proxy():
    with open("proxies.json") as proxyfile:
        proxies = json.load(proxyfile)
    return proxies

def burpproxy():
    with open("burp.json") as proxyfile:
        proxies = json.load(proxyfile)
    return proxies
