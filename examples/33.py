#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
#from scapy.all import *

import random
import time

def generate_traffic(net, normal_traffic, duration):

    start_time = time.time()
    normal_packets = []
    attack_packets = []
    while time.time() - start_time <= duration:
        h1, h3 = net.get('h1', 'h3')
        if random.random() < normal_traffic:
            h1.cmd('ping -c 1 10.0.10.3')
               #packet = IP(src="192.168.10.5", dst="10.0.10.3") / ICMP()
            #normal_packets.append(packet)
        else:
            h1.cmd('hping3 -c 10000 -d 120 -S -w 64 -p 80 --flood 10.0.10.3')
              #packet = IP(src="192.168.10.5", dst="10.0.10.3") / TCP(dport=80, flags="S")
            #attack_packets.append(packet)
        time.sleep(0.1) 


def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    #r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    #r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    #r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    #r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    #r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    #r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.10.5/24', defaultRoute='via 192.168.10.1')
    h2 = net.addHost('h2', cls=Host, ip='202.99.8.3/24', defaultRoute='via 202.99.8.1')
    h3 = net.addHost('h3', cls=Host, ip='10.0.10.3/24', defaultRoute='via 10.0.10.1')
    
    #h1 = net.addHost('h1')
    #h2 = net.addHost('h2')
    #h3 = net.addHost('h3')
    r1 = net.addHost('r1')
    r2 = net.addHost('r2')
    r3 = net.addHost('r3')


    info( '*** Add links\n')
    #net.addLink(r2, r3)

    net.addLink(h1, r1)
    net.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth1')
    net.addLink(r2, r3, intfName1='r2-eth0', intfName2='r3-eth0')
    net.addLink(h2, r2)
    net.addLink(r3, h3)

    #h1.cmd('ifconfig h1-eth0 192.168.10.5/24')
    #h2.cmd('ifconfig h2-eth0 202.99.8.3/24')
    #h3.cmd('ifconfig h3-eth0 10.0.10.3/24')




    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    info( '*** Post configure switches and hosts\n')

    r1.cmd('ifconfig r1-eth0 192.168.10.1/24')
    r1.cmd('ifconfig r1-eth1 172.16.2.1/24')
    r2.cmd('ifconfig r2-eth1 172.16.2.2/24')
    r2.cmd('ifconfig r2-eth0 192.168.20.1/24')
    r2.cmd('ifconfig r2-eth2 202.99.8.1/24')
    r3.cmd('ifconfig r3-eth0 192.168.20.2/24')
    r3.cmd('ifconfig r3-eth1 10.0.10.1/24')

    h1.cmd('route add default gw 192.168.10.1 dev h1-eth0')
    h2.cmd('route add default gw 202.99.8.1 dev h2-eth0')
    h3.cmd('route add default gw 10.0.10.1 dev h3-eth0')
    r1.cmd('route add -net 202.99.8.0/24 gw 172.16.2.2 dev r1-eth1')
    r2.cmd('route add -net 192.168.10.0/24 gw 172.16.2.1 dev r2-eth1')
    r2.cmd('route add -net 10.0.10.0/24 gw 192.168.20.2 dev r2-eth0')
    r3.cmd('route add -net 202.99.8.0/24 gw 192.168.20.1 dev r3-eth0')
    r1.cmd('route add -net 10.0.10.0/24 gw 172.16.2.2 dev r1-eth1')
    r3.cmd('route add -net 192.168.10.0/24 gw 192.168.20.1 dev r3-eth0')

    r1.cmd('sysctl net.ipv4.ip_forward=1')
    r2.cmd('sysctl net.ipv4.ip_forward=1')
    r3.cmd('sysctl net.ipv4.ip_forward=1')

    #net.startTerms()
    #h1.cmd('tcpdump -i h1-eth0 -w normal_traffic.pcap &')
    #h1.cmd('tcpdump -i h1-eth0 -w attack_traffic.pcap &')

    #normal_traffic = 0.8
    #attack_traffic = 0.2

    #while True:
        #if random.random() < normal_traffic:

           #h1.cmd('ping -c 1 10.0.10.3')
        #else:
           #h1.cmd('hping3 -c 10000 -d 120 -S -w 64 -p 80 --flood 10.0.10.3')
        #time.sleep(1)



    normal_traffic = 0.8
    attack_traffic = 0.2
    duration = 5
    generate_traffic(net, normal_traffic, duration)

    #all_packets = normal_packets + attack_packets
    #wrpcap("traffic.pcap", all_packets)
    h1.cmd('tcpdump -i h1-eth0 -w /home/linux/mininet/mininet/examples/attack_traffic.pcap &')
    r3.cmd('tcpdump -i r3-eth0 -w /home/linux/mininet/mininet/examplestraffic1.pcap &')




    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
