#!/usr/bin/python

import subprocess
from mininet.net import Mininet
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
import time
import sys
import math

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h2 = self.addHost('h2', cls=Host, ip='202.99.8.3/24', defaultRoute=None)
    h3 = self.addHost('h3', cls=Host, ip='10.0.10.3', defaultRoute=None)
    h1 = self.addHost('h1', cls=Host, ip='192.168.10.5/24', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(r2, r3)
    net.addLink(r3, h3)
    net.addLink(h1, r1)
    net.addLink(r1, r2)
    net.addLink(h2, r2)



def main():

    topo = myNetwork()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    info( '*** Post configure switches and hosts\n')




    def generate_traffic(net):
        h1 = net.get('h1')
        h3 = net.get('h3')
        generate_traffic(h1, h3)
        if h1.normal_traffic_percentage >= 0.8:
           h1.generate_normal_traffic()
        else:
           h1.generate_attack_traffic()

    class Host(Host):
       def __init__(self, *args, **kwargs): 
           super(Host, self).__init__(*args, **kwargs)
           self.normal_traffic_percentage = 0.8

       def generate_normal_trafic(self):
           self.cmd('iperf -s -t 300 &')

       def generate_traffic_trafic(self):
           self.cmd('hping3 -c 10000 -i u100 --udp -p 5000 10.0.0.2 &')

       print("Dumping Node Connections:")
       dumpNodeConnections(net.switches + net.hosts)
       generate_traffic(net)
       capture_duration = 300
       capture_traffic(capture_duration)



    def capture_traffic(duration):
        subprocess.Popen(['tshark', '-i', 'h1-eth0', '-w', 'traffic.pcap'])
        time.sleep(duration)
        subprocess.Popen(['pkill', 'tshark'])



        CLI(net)

        net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
    main()

