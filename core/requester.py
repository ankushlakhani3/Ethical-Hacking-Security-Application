from core.logger import *
import requests
from core.logger import *
import random
import warnings
from urllib3.exceptions import ProtocolError
import json
from core.config import cookie

warnings.filterwarnings('ignore')  # Disable SSL related warnings

class Requester:

    @classmethod
    def Session(self, headers, proxy, cookie):
        s = requests.Session()
        s.proxies= proxy
        s.headers= headers
        s.cookies.update(json.loads(cookie))
        return s

    @classmethod

    def Request(self,xss, url, headers, proxy):
        user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']
        if 'User-Agent' not in headers:
            headers['User-Agent'] = random.choice(user_agents)
        session = self.Session(headers, proxy, cookie)
        try:
            response = session.get(url)
            return response, session
        except ProtocolError:
            output4 ="[-] WAF is dropping requests"
            xss.xss_textBrowser.append(output4)
        except (requests.ConnectionError, requests.Timeout):
            output5 ="[-] Check your internet conectivity or input url!"
            xss.xss_textBrowser.append(output5)