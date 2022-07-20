from core.utils import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from random import choice
from math import log
import requests, string, re, random
import sys
import time
from urllib.parse import urlparse
import json
#http://testphp.vulnweb.com/
# import logging, pathlib

start = time.perf_counter()
COMMON_CSRF_NAMES = [ 'csrf_token', 
'CSRFName', 
'CSRFToken',  # OWASP CSRF_Guard
'anticsrf',  # AntiCsrfParam.java
'__RequestVerificationToken',  # AntiCsrfParam.java
'token',
'csrf',
'xsrf',
'YII_CSRF_TOKEN',  # http://www.yiiframework.com/
'yii_anticsr',  # http://www.yiiframework.com/
'\"[_token]\"',  # Symfony 2.x
'_csrf_token',  # Symfony 1.4
'csrfmiddlewaretoken' ]  # Django 1.5

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

class Requester:
    @classmethod
    def Session(self, headers, proxy):
        s = requests.Session()
        s.proxies = proxy
        s.headers = headers
        return s

    @classmethod
    def Request(self, url, headers, proxies):
        proxy = ProxyHandler(proxies)
        if "User-Agent" not in headers:
            headers["User-Agent"] = choice(user_agents)

        session = self.Session(headers, proxy.rotate())
        try:
            response = session.get(url, verify=False)
        except requests.exceptions.ProxyError:
            print("[*] Unable to connect with proxy. Check your proxy connection. \n "
            "or Try http:// websites.")
            sys.exit()
        return response, session


class ProxyHandler:
    def __init__(self, proxies):
        self.proxies = proxies

    def scheme(self):
        for key in self.proxies.keys():
            if key == "http":
                return key
            if key == "https":
                return key
        else:
            return None

    def rotate(self):
        scheme = self.scheme()
        if scheme != None:
            proxy = {scheme: "{}://{}".format(scheme, choice(self.proxies[scheme]))}
            return proxy
        else:
            return None



class Crawler:
    def __init__(self, url, session):
        self.session = session
        self.target_url = url
        self.target_links = []

    def extract_links(self, url):
        try:
            response = self.session.get(url, verify = False)
        except requests.exceptions.ConnectionError:
            print("[*] Could not connect to the application. Check your connection or Target App status")
            exit()
        except requests.exceptions.InvalidSchema:
            print("[*] Error in the format of URL")
            exit()
        except KeyboardInterrupt:
            print("[*] KEyboard interrupt, Not gonna run the program :/")
            exit()
        return re.findall('(?:href=")(.*?)"', str(response.content))

    def crawl(self, url=None):
        if url == None:
            url = self.target_url
        href_links = self.extract_links(url)
        for link in href_links:
            link = urljoin(self.target_url, link)

            if "#" in link:
                link = link.split("#")[0]

            if (self.target_url in link and link not in self.target_links and "logout" not in link):
                self.target_links.append(link)
                print(link)
                self.crawl(link)
        return self.target_links


class Scanner:
    def __init__(self, session, password):
        self.session = session
        self.password = password
        self.count_csrf = 0

    def extract_forms(self, url):
        try:
            response = self.session.get(url)
        except requests.exceptions.ConnectionError:
            print("[*] Could not connect to application. Check Target App status")
            exit()
        except requests.exceptions.InvalidSchema:
            print("[*] Error in the format of provided URL")
            exit()
        except KeyboardInterrupt:
            print("[*] KEyboard interrupt, Not gonna run the program :/")
            exit()
        parsed_html = BeautifulSoup(response.content, "html.parser")
        return parsed_html.findAll("form")

    def shannon_entropy(self, data):
        if not data:
            return 0

        entropy = 0

        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += -p_x * log(p_x, 2)

        return entropy

    def is_csrf_token(self, key, value):
        min_length = 5
        max_length = 512
        min_entropy = 2.4

        # Check length
        if len(value) <= min_length:
            return False

        if len(value) > max_length:
            return False

        if not re.match("^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$", value):
            return False

        # Check for common CSRF token names
        for common_csrf_name in COMMON_CSRF_NAMES:
            if common_csrf_name.lower() in key.lower():
                return True

        # Calculate entropy
        entropy = self.shannon_entropy(value)
        if entropy >= min_entropy:
            return True

        return False

    def rand_str_generator(self, size=4, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for _ in range(size))

    def is_resp_equal(self, resp1, resp2):
        if resp1.status_code != resp2.status_code:
            return False
        return True

    def is_token_checked(self, post_url, method, post_data, csrf_token_key, csrf_token):
        modified_data = post_data
        modified_data[csrf_token_key] = csrf_token.replace(
            csrf_token[0:4], self.rand_str_generator()
        )
        try:
            if method == "post":
                original_response = self.session.post(post_url, data=post_data)
                modified_response = self.session.post(post_url, data=modified_data)
                result = self.is_resp_equal(original_response, modified_response)
                return not result
            else:
                original_response = self.session.get(post_url, params=post_data)
                modified_response = self.session.get(post_url, params=modified_data)
                result = self.is_resp_equal(original_response, modified_response)
                return not result
        except requests.exceptions.ConnectionError:
            print("[*] Hey! I am not able to connect to application. Check your Target App status")
            pass
        except requests.exceptions.InvalidSchema:
            print("[*] Error in the provided URL format.")
            exit()

    def scan(self, link):

        print(f"\n[+] Testing forms for CSRF: {link}\n")
        forms = self.extract_forms(link)
        count = 0
        for form in forms:
            csrf_token_key = ""
            csrf_token = ""
            action = form.get("action")
            post_url = urljoin(link, action)
            method = form.get("method")
            post_data = {}
            inputs_list = form.findAll("input")
            for inputs in inputs_list:
                name = inputs.get("name")
                value = inputs.get("value")
                input_type = inputs.get("type")
                if input_type == "password":
                    value = self.password
                post_data[name] = value
                if (name is not None and value is not None
                    and input_type != "submit" and self.is_csrf_token(name, value)):
                    csrf_token_key = name
                    csrf_token = value
            if csrf_token_key != "":
                print("\n[+] CSRF token found; Checking if token is verified\n")
                if not self.is_token_checked(post_url, method, post_data, csrf_token_key, csrf_token):
                    count += 1
                    print("\n[*] Form in " + link + " is vulnerable to CSRF, Token is not verified.\n"
                        "Security Risk: High")
                    print(form)
            else:
                count += 1
                print("\n[*] Form in "+ link + " is vulnerable to CSRF; Lack of csrf_token.\n"
                    "Security Risk: High")
                print(form)
            if method == "GET":
                count += 1
                print("\n[*] Form in "+ link + " is vulnerable to CSRF due to GET request method.\n"
                    "Security Risk: Low")
                print(form)
        if count == 0:
            print("\n[+] This is not vulnerable to CSRF.\n" + link)
           
        else:
            self.count_csrf += count




def main():

    target = str(input("url (Default scheme - https): "))
    proxyy = str(input("Note: Proxy is not working properly with https sites.\n"
        "Do you want to enable proxy? (y/n) - "))
    burp = str(input("NOTE: You have to verify burpsuite CA cert for https sites.\n"
        "You want to capture request in burp:(y/n) Default= NO - "))
    
    # default headers
    headers = {  
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Connection': 'close',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
    }
    password = ""
    # filename = "Scan-Report.txt"

    # logging.basicConfig(
    #     filename="Scan-Report.txt",
    #     filemode="a",
    #     level=logging.INFO,
    #     format="%(message)s",
    # )

    if not target:
        print("\nTarget url is required to start a CSRF scan.\n")
        sys.exit()

    print("CSRF scanning is started on...", target)

    if (proxyy=="y" or proxyy == "yes" or proxyy== "YES" or proxyy=="Y"):
        proxies = enable_proxy()
    else:
        proxies = {}

    if (burp=="y" or burp == "yes" or burp == "YES" or burp=="Y"):
        proxies = burpproxy()
    else:
        proxies = {}

    target = validate(target)
    resp, session = Requester.Request(target, headers, proxies)
    print(f"\n{'*'*25} Creating SiteMap {'*'*25}\n")
    crawler = Crawler(target, session)

    sitemap = crawler.crawl()

    scanner = Scanner(session, password)

    for link in sitemap:
        print(f"\n[+] Testing link: {link}\n")
        print(f"\n{'*'*25} Testing for CSRF {'*'*25}\n")
        scanner.scan(link)

    print(f"\n{'*'*25} Summary of SCAN {'*'*25}\n")
    if scanner.count_csrf == 0:
        print("\nThis App is not vulnerable to csrf.\n")
    else:
        print(f"\nPossible CSRF vulns found: {str(scanner.count_csrf)}")


    # print(f"\nScan report is saved in: {str(pathlib.Path().absolute())}\\{filename}\n")
    session.close()


if __name__ == "__main__":
    logo = "CSRFSCAN"
    print(logo)
    main()
