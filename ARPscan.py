from scapy.all import ARP,Ether,srp,conf
import time
import psutil
from termcolor import colored

def arp_scan(arps, iface, ip_range):
  output2 = "[+]Scanning.." + str(ip_range) 
  arps.arps_textBrowser.append(output2)
  curr_time = time.time()
  output3 = "[+]Scan started at :"+ time.ctime(curr_time)+"\n"
  conf.verb = 0
  arps.arps_textBrowser.append(output3)
  broadcast = "ff:ff:ff:ff:ff:ff"
  ether_layer = Ether(dst = broadcast)
  arp_layer = ARP(pdst = ip_range)

  packet = ether_layer / arp_layer

  ans, unans = srp(packet, iface=iface , timeout=4,inter=0.1)

  for snd, rcv in ans:
    ip = rcv[ARP].psrc
    mac = rcv[Ether].src
    output5 = "ip: " + str(ip)+ " mac: "+str(mac) +"\n"
    arps.arps_textBrowser.append(output5)
    
  duration = time.time() - curr_time
  output4= "[+] Scan Completed, Duration : " + str(duration)+ "\n"
  arps.arps_textBrowser.append(output4)
# scanner.py eth0 192.168.0.1/24
def main(arps, iface,ip_range):

  

  arp_scan(arps, iface,ip_range)