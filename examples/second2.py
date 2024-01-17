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

    r1 = net.addHost('r1', ip='192.168.10.1/24')
    r2 = net.addHost('r2', ip='10.0.10.1/24')
    r3 = net.addHost('r3', ip='202.99.8.1/24')

    h1 = net.addHost('h1', ip='192.168.10.10/24', defaultRoute='via 192.168.10.1')
    h2 = net.addHost('h2', ip='10.0.10.10/24', defaultRoute='via 10.0.10.1')
    h3 = net.addHost('h3', ip='202.99.8.10/24', defaultRoute='via 202.99.8.1')

    net.addLink(h1, r1)
    net.addLink(h2, r2)
    net.addLink(h3, r3)

    net.addLink(r1, r2)
    net.addLink(r2, r3)

    net.start()

    h1.cmd('wireshark -i h1-eth0 -k &')
    h2.cmd('wireshark -i h2-eth0 -k &')
    h3.cmd('wireshark -i h3-eth0 -k &')

    CLI(net)

    h1.cmd('kill %tshark')
    h2.cmd('kill %tshark')
    h3.cmd('kill %tshark')

    net.stop()

if __name__ == '__main__':
      create_topology()

