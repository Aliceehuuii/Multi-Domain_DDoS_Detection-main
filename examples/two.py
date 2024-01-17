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

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h2 = net.addHost('h2', cls=Host, ip='192.168.9.1/24', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='192.168.12.1/24', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.11.1/24', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.10.1/24', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='192.168.8.1/24', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)
    net.addLink(h5, s1)
    net.addLink(h1, s1)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])

    info( '*** Post configure switches and hosts\n')
    s1.cmd('ifconfig s1-eth5 192.168.8.2 netmask 255.255.255.0')
    s1.cmd('ifconfig s1-eth1 192.168.9.2 netmask 255.255.255.0')
    s1.cmd('ifconfig s1-eth2 192.168.10.2 netmask 255.255.255.0')
    s1.cmd('ifconfig s1-eth3 192.168.11.2 netmask 255.255.255.0')
    s1.cmd('ifconfig s1-eth4 192.168.12.2 netmask 255.255.255.0')

    h1.cmd('route add  default gw 192.168.8.2')
    h2.cmd('route add  default gw 192.168.9.2')
    h3.cmd('route add  default gw 192.168.10.2')
    h4.cmd('route add  default gw 192.168.11.2')
    h5.cmd('route add  default gw 192.168.12.2')

    s1.cmd('sysctl net.ipv4.ip_forward=1')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

