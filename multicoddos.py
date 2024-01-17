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
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6634)

    c2=net.addController(name='c2',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6635)

    info( '*** Add switches\n')
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch, dpid='0000000000000006')
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, dpid='0000000000000005')
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, dpid='0000000000000003')
    #r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    #r2.cmd('sysctl -w net.ipv4.ip_forward=1')
    #r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    #r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch, dpid='0000000000000004')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, dpid='0000000000000002')
    #r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    #r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, dpid='0000000000000001')

    info( '*** Add hosts\n')
    h16 = net.addHost('h16', cls=Host, ip='10.0.10.7/24', defaultRoute='via 10.0.10.2')
    h12 = net.addHost('h12', cls=Host, ip='202.99.8.8/24', defaultRoute='via 202.99.8.2')
    h8 = net.addHost('h8', cls=Host, ip='202.99.8.4/24', defaultRoute='via 202.99.8.1')
    h4 = net.addHost('h4', cls=Host, ip='192.168.10.8/24', defaultRoute='via 192.168.10.2')
    h5 = net.addHost('h5', cls=Host, ip='192.168.10.9/24', defaultRoute='via 192.168.10.2')
    h17 = net.addHost('h17', cls=Host, ip='10.0.10.8/24', defaultRoute='via 10.0.10.2')
    h9 = net.addHost('h9', cls=Host, ip='202.99.8.5/24', defaultRoute='via 202.99.8.1')
    h1 = net.addHost('h1', cls=Host, ip='192.168.10.5/24', defaultRoute='via 192.168.10.1')
    h18 = net.addHost('h18', cls=Host, ip='10.0.10.9/24', defaultRoute='via 10.0.10.2')
    h14 = net.addHost('h14', cls=Host, ip='10.0.10.5/24', defaultRoute='via 10.0.10.1')
    h10 = net.addHost('h10', cls=Host, ip='202.99.8.6/24', defaultRoute='via 202.99.8.2')
    h6 = net.addHost('h6', cls=Host, ip='192.168.10.10/24', defaultRoute='via 192.168.10.2')
    h13 = net.addHost('h13', cls=Host, ip='10.0.10.4/24', defaultRoute='via 10.0.10.1')
    h15 = net.addHost('h15', cls=Host, ip='10.0.10.6/24', defaultRoute='via 10.0.10.1')
    h2 = net.addHost('h2', cls=Host, ip='192.168.10.6/24', defaultRoute='via 192.168.10.1')
    h11 = net.addHost('h11', cls=Host, ip='202.99.8.7/24', defaultRoute='via 202.99.8.2')
    h7 = net.addHost('h7', cls=Host, ip='202.99.8.3/24', defaultRoute='via 202.99.8.1')
    h3 = net.addHost('h3', cls=Host, ip='192.168.10.7/24', defaultRoute='via 192.168.10.1')


    r1 = net.addHost('r1')
    r2 = net.addHost('r2')
    r3 = net.addHost('r3')

    info( '*** Add links\n')
    net.addLink(h1, s4)
    net.addLink(h2, s4)
    net.addLink(h3, s4)
    net.addLink(h4, s5)
    net.addLink(h5, s5)
    net.addLink(h6, s5)
    net.addLink(h7, s6)
    net.addLink(h8, s6)
    net.addLink(h9, s6)
    net.addLink(h10, s7)
    net.addLink(h11, s7)
    net.addLink(h12, s7)
    net.addLink(h13, s8)
    net.addLink(h14, s8)
    net.addLink(h15, s8)
    net.addLink(h16, s9)
    net.addLink(h17, s9)
    net.addLink(h18, s9)
    net.addLink(s4, r1)
    net.addLink(s5, r1)
    net.addLink(s6, r2)
    net.addLink(s7, r2)
    net.addLink(s8, r3)
    net.addLink(s9, r3)
    net.addLink(r1, r2)
    net.addLink(r2, r3)
    net.addLink(s4, s5)
    net.addLink(s5, s6)
    net.addLink(s6, s7)
    net.addLink(s7, s8)
    net.addLink(s8, s9)

    net.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2')
    net.addLink(r2, r3, intfName1='r2-eth3', intfName2='r3-eth2')

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s9').start([c2])
    net.get('s8').start([c2])
    net.get('s6').start([c1])
    net.get('s7').start([c1])
    net.get('s5').start([c0])
    net.get('s4').start([c0])

    info( '*** Post configure switches and hosts\n')


    r1.cmd('ifconfig r1-eth0 192.168.10.1/24')
    r1.cmd('ifconfig r1-eth1 192.168.10.2/24')
    r1.cmd('ifconfig r1-eth2 172.16.2.1/24')
    r2.cmd('ifconfig r2-eth2 172.16.2.2/24')
    r2.cmd('ifconfig r2-eth0 192.168.20.1/24')
    r2.cmd('ifconfig r2-eth2 192.168.20.2/24')
    r2.cmd('ifconfig r2-eth3 202.99.8.1/24')
    r3.cmd('ifconfig r3-eth1 10.0.10.1/24')
    r3.cmd('ifconfig r3-eth0 10.0.10.1/24')
    r3.cmd('ifconfig r3-eth1 10.0.10.2/24')
    r3.cmd('ifconfig r3-eth2 192.168.20.2/24')


    h1.cmd('route add default gw 192.168.10.1 dev h1-eth0')
    h2.cmd('route add default gw 192.168.10.1 dev h2-eth0')
    h3.cmd('route add default gw 192.168.10.1 dev h3-eth0')
    h4.cmd('route add default gw 192.168.10.2 dev h4-eth0')
    h5.cmd('route add default gw 192.168.10.2 dev h5-eth0')
    h6.cmd('route add default gw 192.168.10.2 dev h6-eth0')

    h7.cmd('route add default gw 202.99.8.1 dev h7-eth0')
    h8.cmd('route add default gw 202.99.8.1 dev h8-eth0')
    h9.cmd('route add default gw 202.99.8.1 dev h9-eth0')
    h10.cmd('route add default gw 202.99.8.2 dev h10-eth0')
    h11.cmd('route add default gw 202.99.8.2 dev h11-eth0')
    h12.cmd('route add default gw 202.99.8.2 dev h12-eth0')

    h13.cmd('route add default gw 10.0.10.1 dev h13-eth0')
    h14.cmd('route add default gw 10.0.10.1 dev h14-eth0')
    h15.cmd('route add default gw 10.0.10.1 dev h15-eth0')
    h16.cmd('route add default gw 10.0.10.2 dev h16-eth0')
    h17.cmd('route add default gw 10.0.10.2 dev h17-eth0')
    h18.cmd('route add default gw 10.0.10.2 dev h18-eth0')

    r1.cmd('route add -net 202.99.8.0/24 gw 172.16.2.2 dev r1-eth2')
    r2.cmd('route add -net 192.168.10.0/24 gw 172.16.2.1 dev r2-eth2')
    r2.cmd('route add -net 10.0.10.0/24 gw 192.168.20.2 dev r2-eth3')
    r3.cmd('route add -net 202.99.8.0/24 gw 192.168.20.1 dev r3-eth2')
    r1.cmd('route add -net 10.0.10.0/24 gw 172.16.2.2 dev r1-eth2')
    r3.cmd('route add -net 192.168.10.0/24 gw 192.168.20.1 dev r3-eth2')


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

