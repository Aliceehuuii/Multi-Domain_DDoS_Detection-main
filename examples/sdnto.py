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
    c1=net.addController(name='c1',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s22 = net.addSwitch('s22', cls=OVSKernelSwitch, dpid='0000000000000006')
    s21 = net.addSwitch('s21', cls=OVSKernelSwitch, dpid='0000000000000005')
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, dpid='0000000000000004')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid='0000000000000001')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, dpid='0000000000000002')
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, dpid='0000000000000003')

    info( '*** Add hosts\n')
    h5 = net.addHost('h5', cls=Host, ip='10.1.2.2', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.10.20.2', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.10.10.1', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.10.20.1', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.10.10.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.1.2.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.1.1.2', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.10.20.3', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.1.1.3', defaultRoute=None)
    h1 = net.addHost('h1', cls=Host, ip='10.1.1.1', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='10.1.2.3', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.10.10.2', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h4, s12)
    net.addLink(h5, s12)
    net.addLink(h6, s12)
    net.addLink(h7, s21)
    net.addLink(h8, s21)
    net.addLink(h9, s21)
    net.addLink(h10, s22)
    net.addLink(h11, s22)
    net.addLink(h12, s22)
    net.addLink(s11, s1)
    net.addLink(s12, s1)
    net.addLink(s21, s2)
    net.addLink(s22, s2)
    net.addLink(s1, s2)
    net.addLink(h1, s11)
    net.addLink(h2, s11)
    net.addLink(h3, s11)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s22').start([])
    net.get('s21').start([])
    net.get('s12').start([])
    net.get('s1').start([c1])
    net.get('s2').start([c1])
    net.get('s11').start([])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

