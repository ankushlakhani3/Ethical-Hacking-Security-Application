
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse,parse_qs,urlencode
from urllib3.exceptions import ConnectionError
# from requests.sessions import session
from core.requester import Requester
from core.config import method
from core.logger import *


class Scanner:
		
	@classmethod
	def post_method(self,xss):
		bsObj=BeautifulSoup(self.body,"html.parser")
		forms=bsObj.find_all("form",method=True)
		
		for form in forms:
			try:
				action=form["action"]
			except KeyError:
				action=self.url
				
			if form["method"].lower().strip() == "post":
				#Logger.warning("Target have form with POST method: "+C+urljoin(self.url,action))
				#.info("Collecting form input keys.....")
				
				keys={}
				for key in form.find_all(["input","textarea"]):
					try:
						if key["type"] == "submit":
							#Logger.info("Form endpoint: "+G+key["name"]+N+" value: "+G+"<Submit Confirm>")
							keys.update({key["name"]:key["name"]})
				
						else:
							#Logger.info("Form key name: "+G+key["name"]+N+" value: "+G+self.payload)
							keys.update({key["name"]:self.payload})
							
					except Exception as e:
						pass
						#Logger.info("Internal error: "+str(e))
				
				#Logger.info("Sending payload (POST) method...")
				req=self.session.post(urljoin(self.url,action),data=keys)
				if self.payload in req.text:
					output7 ="*************************************\n[$$] Detected XSS (POST) at,\n "+urljoin(self.url,req.url)
					xss.xss_textBrowser.append(output7)
					file = open("Xss vulnerability.txt", "a")
					file.write(str(req.url)+"\n\n")
					file.close()
					output8 ="[$$] vulnerability: "+str(keys)+ "\n""*************************************"
					xss.xss_textBrowser.append(output8)
					
				else:
					output9 ="[-] XSS not detected (POST) "#at "+urljoin(self.url,req.url)
					xss.xss_textBrowser.append(output9)
				
					
	
	@classmethod
	def get_method_form(self, xss):
		bsObj=BeautifulSoup(self.body,"html.parser")
		forms=bsObj.find_all("form",method=True)
		
		for form in forms:
			try:
				action=form["action"]
			except KeyError:
				action=self.url
				
			if form["method"].lower().strip() == "get":
				#Logger.warning("Target have form with GET method: "+C+urljoin(self.url,action))
				#Logger.info("Collecting form input keys.....")
				
				keys={}
				for key in form.find_all(["input","textarea"]):
					try:
						if key["type"] == "submit":
							#Logger.info("Form key name: "+G+key["name"]+N+" value: "+G+"<Submit Confirm>")
							keys.update({key["name"]:key["name"]})
				
						else:
							#Logger.info("Form key name: "+G+key["name"]+N+" value: "+G+self.payload)
							keys.update({key["name"]:self.payload})
							
					except Exception as e:
						#Logger.info("Internal error: "+str(e))
						try:
							#Logger.info("Form key name: "+G+key["name"]+N+" value: "+G+self.payload)
							keys.update({key["name"]:self.payload})
						except KeyError as e:
							pass
							#Logger.info("key Internal error: "+str(e))
							
						
				#Logger.info("Sending payload (GET) method...")
				req=self.session.get(urljoin(self.url,action),params=keys)
				if self.payload in req.text:
					output10 ="*************************************\n[$$] Detected XSS (POST) at,\n "+urljoin(self.url,req.url)
					xss.xss_textBrowser.append(output10)
					file = open("Xss vunerability.txt", "a")
					file.write(str(req.url)+"\n\n")
					file.close()
					output11 ="[$$] vulnerability: "+str(keys)+ "\n""*************************************"
					xss.xss_textBrowser.append(output11)
					
				else:
					output12 ="[-] XSS not detected (GET) "#at "+urljoin(self.url,req.url)
					xss.xss_textBrowser.append(output12)
					#Logger.info("\033[0;35;47m Parameter page using GET")
		
	@classmethod
	def get_method(self,xss):
		bsObj=BeautifulSoup(self.body,"html.parser")
		links=bsObj.find_all("a",href=True)
		for a in links:
			url=a["href"]
			if url.startswith("http://") is False or url.startswith("https://") is False or url.startswith("mailto:") is False:
				base=urljoin(self.url,a["href"])
				query=urlparse(base).query
				if query != "":
					#Logger.warning("Found link with query: "+G+query+N+" Maybe a vuln XSS point")
					
					query_payload=query.replace(query[query.find("=")+1:len(query)],self.payload,1)
					test=base.replace(query,query_payload,1)
					
					query_all=base.replace(query,urlencode({x: self.payload for x in parse_qs(query)}))
					
					

					if not url.startswith("mailto:") and not url.startswith("tel:"):
							
						_respon=self.session.get(test,verify=False)
						if _respon.status_code != 200:
							if _respon.status_code == 500:
								#Logger.warning(R+str(_respon.status_code)+'-Internal server error.'+W)
								#Logger.info('There is a problem with the resource you are looking for, and it cannot be displayed.')
								continue
						output14 ="[+]Trying payload using query (GET) : "+test
						xss.xss_textBrowser.append(output14)
						if self.payload in _respon.text or self.payload in self.session.get(query_all).text:
							output13 ="*************************************\n[$$] Detected XSS (GET) at,\n "+_respon.url
							xss.xss_textBrowser.append(output13)
									
							file = open("Xss vunerability.txt", "a")
							file.write(str(_respon.url)+"\n\n")
							file.close()
							
						
						else:
							output14 ="[-] XSS not detected (GET) "#at "+_respon.url
							xss.xss_textBrowser.append(output14)
							#Logger.info("Parameter page using GET")
					else:
						output15 ="[-] URL is not an HTTP url, ignoring"
						xss.xss_textBrowser.append(output15)
	
	@classmethod
	def scan(self,xss,url,proxy,headers,payload):
		
		
		self.payload=payload
		self.url=url
		#Logger.info("Checking connection to: "+Y+url)	
		try:
			response, self.session = Requester.Request(xss,url, headers, proxy)
			self.body = response.text

		except Exception:
			return
		except KeyboardInterrupt:
			pass
		try:
			if response.status_code > 400:
				#Logger.info("Connection failed "+G+str(response.status_code))
				return 
			else:
				output6 ="----------------------------------------------------\n[+] Connection estabilished with " +url +str(response.status_code)
				xss.xss_textBrowser.append(output6)
			
			if method == 'ALL':
				self.post_method(xss)
				self.get_method(xss)
				self.get_method_form(xss)

			elif method == 'POST':
				self.post_method(xss)
				
			elif method == 'GET':
				self.get_method(xss)
				self.get_method_form(xss)
				
		except KeyboardInterrupt:
			pass