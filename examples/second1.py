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

def create_topology():
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch, link=TCLink, autoSetMacs=True)
    #c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)


    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    r1 = net.addHost('r1', cls=Node)
    r2 = net.addHost('r2', cls=Node)
    r3 = net.addHost('r3', cls=Node)

    net.addLink(r1, s1, intfName1='r1-eth1', params1={'ip':"192.168.10.1/24"})
    net.addLink(r2, s2, intfName1='r2-eth1', params1={'ip':"10.0.10.1/24"})
    net.addLink(r3, s3, intfName1='r3-eth1', params1={'ip':"202.99.8.1/24"})

    net.addLink(s1, s2)
    net.addLink(s2, s3)

    net.start()

    r1.cmd('ip route add default via 192.168.10.1')
    r2.cmd('ip route add default via 10.0.10.1')
    r3.cmd('ip route add default via 202.99.8.1')

    r1.cmd('tshark -i r1-eth1 -w /tmp/192.168.10.pcap &')
    r2.cmd('tshark -i r2-eth1 -w /tmp/10.0.10.pcap &')
    r3.cmd('tshark -i r3-eth1 -w /tmp/202.99.8.pcap &')

    CLI(net)

    r1.cmd('kill %tshark')
    r2.cmd('kill %tshark')
    r3.cmd('kill %tshark')

    net.stop()

if __name__ == '__main__':
      create_topology()

