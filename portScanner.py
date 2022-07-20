from threading import Thread
from termcolor import colored
import optparse
import time
import socket

curr_time = time.time()

def duration():
  duration = time.time() - curr_time
  return duration

def connScan(ps, tgtHost,tgtPort):
  try:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((tgtHost,tgtPort)) 
    output2=' '+str(tgtPort)+' /tcp Open '
    ps.ps_textBrowser.append(output2)
    
    sock.close()
  except :
    pass

    

def portScan(ps, tgtHost, tgtPorts):
  output=""""""
  try:
    tgtIP = socket.gethostbyname(tgtHost)
  except:
    output='Unknown Host '
    ps.ps_textBrowser.append(output)  
  try:
    tgtName = socket.gethostbyaddr(tgtIP)
    output='\n[+] Scan Result for :' + tgtName+ '\n'
    ps.ps_textBrowser.append(output)
  except:
    output='\n[+] Scan Result for :' + tgtIP + '\n'
    ps.ps_textBrowser.append(output)

  socket.setdefaulttimeout(1)

  if tgtPorts != None:
    for tgtPort in tgtPorts:
      t = Thread(target=connScan, args=(ps, tgtHost,int(tgtPort)))
      t.start()
  else:
    for tgtPort in range(0,1024):
      t = Thread(target=connScan, args=(ps, tgtHost,int(tgtPort)))
      t.start()
      
    
  
  
def main(ps, option,tgtPort,tgtHost):
 
  if(option == 'well khown port'):
    tgtPorts = None
  else:
    tgtPorts = tgtPort.split(',')

  portScan(ps, tgtHost,tgtPorts)
