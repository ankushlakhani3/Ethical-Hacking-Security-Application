import argparse, time
from distutils.command.config import config
from core.colors import *
from core.logger import *
from core.scanner import Scanner
from core.crawler import Crawler
#from core.fuzzer import Fuzzer
from core.utils import check, wordlist
# Configuration file contains tool settings
from core import config



def main(xss,depth,target,payload):
	if depth == 1:
		level =1
	elif depth ==2:
		level = 2
	else:
		level = 3
	proxy = 'http://127.0.0.1:8080/'
	headers = config.headers
	#start = time.perf_counter()	
	output1 ="[+] Started finding of xss vulnerability"
	xss.xss_textBrowser.append(output1)
	Scanner.scan(xss,target, proxy, headers, check(payload))
	Crawler.crawl(xss,target, level, proxy, headers, check(payload))
	#end = time.perf_counter()
	output2 ="[+] finding finished "#in" +round(end-start,3) +"seconds"
	xss.xss_textBrowser.append(output2)
	if os.path.isfile('Xss vulnerability.txt') and os.stat('Xss vulnerability.txt').st_size != 0:
		output3 ="[+] Results saved in Xss vulnerability.txt"
		xss.xss_textBrowser.append(output3)
		
	
	
	








