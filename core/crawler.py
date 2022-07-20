# from core import config
from core.logger import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
from core.requester import Requester

from core.config import cookie
from core.scanner import Scanner


class Crawler:
	
	visited=[]
	
	@classmethod
	def getLinks(self,base, proxy,headers):
		lst=[]
		session = Requester.Session(headers, proxy, cookie)
		response = session.get(base)
		text=response.text
		isi=BeautifulSoup(text,"html.parser")
	
		
		for obj in isi.find_all("a",href=True):
			url=obj["href"]
			
			
			if urljoin(base,url) in self.visited:
				continue

			elif url.startswith("mailto:") or url.startswith("javascript:"):
				continue
		
			elif url.startswith(base) or "://" not in url :
				lst.append(urljoin(base,url))
				self.visited.append(urljoin(base,url))
			
		return lst

	@classmethod
	def crawl(self,xss,base,depth,proxy,headers,level):

		urls=self.getLinks(base, proxy, headers)
		
		for url in urls:
			if url.startswith("https://") or url.startswith("http://"):
				self.flash(xss,url,proxy,headers,level)
				if depth != 0:
					self.crawl(xss,url,depth-1,base,proxy,level)
					
				else:
					break	
	@classmethod
	def flash(self,xss,url,proxy,headers,level):
		t = threading.Thread(target=Scanner.scan, args=(xss,url,proxy,headers,level))
		t.start()
		t.join()
		