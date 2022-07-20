from xsrfscan.core.utils import *
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
    def Request(self,csrf, url, headers, proxies):
        proxy = ProxyHandler(proxies)
        if "User-Agent" not in headers:
            headers["User-Agent"] = choice(user_agents)

        session = self.Session(headers, proxy.rotate())
        try:
            response = session.get(url, verify=False)
        except requests.exceptions.ProxyError:
            output="[*] Unable to connect with proxy. Check your proxy connection or Try http:// websites.\n" 
            csrf.csrf_textBrowser.append(output)
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
    def __init__(self,csrf, url, session):
        self.session = session
        self.target_url = url
        self.target_links = []

    def extract_links(self,csrf, url):
        try:
            response = self.session.get(url, verify = False)
        except requests.exceptions.ConnectionError:
            output="[*] Could not connect to the application. Check your connection or Target App status"
            csrf.csrf_textBrowser.append(output)
            
            exit()
        except requests.exceptions.InvalidSchema:
            output="[*] Error in the format of URL"
            csrf.csrf_textBrowser.append(output)
            exit()
        except KeyboardInterrupt:
            output="[*] KEyboard interrupt, Not gonna run the program :/"
            csrf.csrf_textBrowser.append(output)
            exit()
        return re.findall('(?:href=")(.*?)"', str(response.content))

    def crawl(self,csrf, url=None):
        if url == None:
            url = self.target_url
        href_links = self.extract_links(csrf,url)
        for link in href_links:
            link = urljoin(self.target_url, link)

            if "#" in link:
                link = link.split("#")[0]

            if (self.target_url in link and link not in self.target_links and "logout" not in link):
                self.target_links.append(link)
            
                csrf.csrf_textBrowser.append(link)
                self.crawl(csrf,link)
        return self.target_links


class Scanner:
    def __init__(self, csrf,session, password):
        self.session = session
        self.password = password
        self.count_csrf = 0

    def extract_forms(self,csrf, url):
        try:
            response = self.session.get(url)
        except requests.exceptions.ConnectionError:
            output="[*] Could not connect to application. Check Target App status"
            csrf.csrf_textBrowser.append(output)
            exit()
        except requests.exceptions.InvalidSchema:
            output="[*] Error in the format of provided URL"
            csrf.csrf_textBrowser.append(output)
            exit()
        except KeyboardInterrupt:
            output="[*] KEyboard interrupt, Not gonna run the program :/"
            csrf.csrf_textBrowser.append(output)
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

    def is_csrf_token(self,csrf, key, value):
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

    def is_token_checked(self,csrf, post_url, method, post_data, csrf_token_key, csrf_token):
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
            output="[*] Hey! I am not able to connect to application. Check your Target App status"
            csrf.csrf_textBrowser.append(output)
            pass
        except requests.exceptions.InvalidSchema:
            output="[*] Error in the provided URL format."
            csrf.csrf_textBrowser.append(output)
            exit()

    def scan(self,csrf, link):

        output="\n[+] Testing forms for CSRF: "+link
        csrf.csrf_textBrowser.append(output)
        forms = self.extract_forms(csrf,link)
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
                    and input_type != "submit" and self.is_csrf_token(csrf,name, value)):
                    csrf_token_key = name
                    csrf_token = value
            if csrf_token_key != "":
                output="\n[+] CSRF token found; Checking if token is verified\n"
                csrf.csrf_textBrowser.append(output)
                if not self.is_token_checked(csrf,post_url, method, post_data, csrf_token_key, csrf_token):
                    count += 1
                    output="\n[*] Form in " + link + " is vulnerable to CSRF, Token is not verified.\nSecurity Risk: High"
                    csrf.csrf_textBrowser.append(output)
                    csrf.csrf_textBrowser.append(form)
                
                    
            else:
                count += 1
                output="\n[*] Form in "+ link + " is vulnerable to CSRF; Lack of csrf_token.\nSecurity Risk: High"
                csrf.csrf_textBrowser.append(output)
                output=str(form)
                csrf.csrf_textBrowser.append(output)
            if method == "GET":
                count += 1
                output="\n[*] Form in "+ link + " is vulnerable to CSRF due to GET request method.\nSecurity Risk: Low"
                csrf.csrf_textBrowser.append(output)
                csrf.csrf_textBrowser.append(form)
        if count == 0:
            output="\n[+] This is not vulnerable to CSRF.\n" + link
            csrf.csrf_textBrowser.append(output)
           
        else:
            self.count_csrf += count




def main(csrf,target):

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

    output="CSRF scanning is started on..." + target 
    csrf.csrf_textBrowser.append(output)


    target = validate(target)
    proxies = enable_proxy()
    resp, session = Requester.Request(csrf,target,headers,proxies)
    output="\n************************* Creating SiteMap *************************\n"
    csrf.csrf_textBrowser.append(output)
    
    crawler = Crawler(csrf,target, session)

    sitemap = crawler.crawl(csrf)

    scanner = Scanner(csrf,session, password)

    for link in sitemap:
        output="\n[+] Testing link: "+link
        csrf.csrf_textBrowser.append(output) 
        output="\n************************* Testing for CSRF *************************\n"
        csrf.csrf_textBrowser.append(output)
        scanner.scan(csrf,link)

    output="\n************************* Summary of SCAN *************************\n"
    csrf.csrf_textBrowser.append(output)
   
    if scanner.count_csrf == 0:  
        output="\nThis App is not vulnerable to csrf.\n"
        csrf.csrf_textBrowser.append(output)

    else:
        output="\nPossible CSRF vulns found: " + str(scanner.count_csrf)
        csrf.csrf_textBrowser.append(output)
    
    # print(f"\nScan report is saved in: {str(pathlib.Path().absolute())}\\{filename}\n")
    session.close()

