#!/usr/bin/python

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.util import irange, dumpNodeConnections
import threading
import subprocess
import time
#from kwargs import kwargs
import sys
from collections import Counter
import math



class SimpleTopo(Topo):

   def build(self):
   #def myNetwork(self):

       net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

       info( '*** Adding controller\n' )

       info( '*** Add switches\n')
       r1 = net.addHost('r1', cls=Node, ip='192.168.10.1/24')
       r1.cmd('sysctl -w net.ipv4.ip_forward=1')
       r2 = net.addHost('r2', cls=Node, ip='10.0.10.1/24')
       r2.cmd('sysctl -w net.ipv4.ip_forward=1')
       r3 = net.addHost('r3', cls=Node, ip='202.99.8.1/24')
       r3.cmd('sysctl -w net.ipv4.ip_forward=1')

       info( '*** Add hosts\n')
       h1 = self.addHost('h1', cls=CustomHost, ip='192.168.10.10/24', defaultRoute='via 192.168.10.1')
       h2 = self.addHost('h2', cls=CustomHost, ip='10.0.10.10/24', defaultRoute='via 10.0.10.1')
       h3 = self.addHost('h3', cls=CustomHost, ip='202.99.8.10/24', defaultRoute='via 202.99.8.1')


       info( '*** Add links\n')
       net.addLink(r2, r3)
       self.addLink(r3, h3)
       self.addLink(h1, r1)
       net.addLink(r1, r2)
       self.addLink(h2, r2)
class CustomHost(Host):
   def __init__(self, *args, **kwargs): 
       super(CustomHost, self).__init__(*args, **kwargs)
       self.normal_traffic_percentage = 0.8

   def generate_normal_trafic(self):
       self.cmd('iperf -s -t 300 &')

   def generate_traffic_trafic(self):
       self.cmd('hping3 -c 10000 -i u100 --udp -p 5000 10.0.0.2 &')

def generate_traffic(net):
    h1, h3 = net.get('h1', 'h3')
    if h1.normal_traffic_percentage >= 0.8:
       h1.generate_normal_traffic()
    else:
       h1.generate_attack_traffic()

def capture_traffic(duration):
    subprocess.Popen(['tshark', '-i', 'h1-eth0', '-w', 'traffic.pcap'])
    time.sleep(duration)
    subprocess.Popen(['pkill', 'tshark'])

def main():
    topo = SimpleTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    print("Dumping Node Connections:")
    dumpNodeConnections(net.switches + net.hosts)
    generate_traffic(net)
    capture_duration = 300
    capture_traffic(capture_duration)
      
    net.stop()

  

if __name__ == '__main__':
    main()
