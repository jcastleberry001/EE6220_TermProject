#!/usr/bin/env python3
from mininet.log import setLogLevel
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import OVSKernelAP
from mininet.node import Controller
from mininet.term import makeTerm
import os
import socket
import time

def topology():

    # Initial setup. Clear previous xterm windows
    print("Cleaning with mn")
    os.system("pkill xterm")
    os.system("sudo mn -c")

    if 'SUMO_HOME' not in os.environ:
        os.environ['SUMO_HOME'] = "/usr/share/sumo"

    # Create the mininet network
    print("Creating controller")
    net = Mininet_wifi(
        accessPoint=OVSKernelAP,
        link=wmediumd,
        wmediumd_mode=interference)

    # Start local controller
    c1 = net.addController('c1', controller=Controller)

    print("Setting up propagation model")
    net.setPropagationModel(model="logDistance", exp=2.35)

    # Add cars (mobile stations)
    for i in range(1, 8):
        net.addCar(
            f'car{i}',
            wlans=2,
            encrypt=['wpa2', ''],
            range=310)

    # AP settings
    kwargs = {
        'ssid': 'vanet-ssid',
        'mode': 'g',
        'passwd': '123456789a',
        'encrypt': 'wpa2',
        'failMode': 'standalone'}

    # add AP and "RSU" station
    e1 = net.addAccessPoint(
        'e1',
        mac='00:00:00:11:00:01',
        channel='1',
        position='2400,3600,0',
        range=310,
        **kwargs)

    sta1 = net.addStation('sta1',
        ip='192.168.0.100/24',
        position='2500,3600,0',
        wlans=2,
        encrypt=['wpa2', ''],
        range=310)

    print("Configure nodes \n")
    net.configureNodes()

    # SUMO simulation
    net.useExternalProgram(
        program=sumo,
        port=8813,
        config_file='map.sumocfg',
        extra_params=["--start", "--delay", "1000"])

    #Wired Link
    net.addLink(e1, sta1)

    # Build/start network
    net.build()
    c1.start()
    e1.start([c1])

    # ITS links for second wireless interface on each car
    for car in net.cars:
        net.addLink(
            car,
            e1,
            intf=car.wintfs[1].name,
            cls=ITSLink,
            band=20,
            channel=181)

    # Add IPs to each car
    for idx, car in enumerate(net.cars, start=1):
        car.setIP(f'192.168.0.{idx}/24',
        intf=car.wintfs[0].name)

    # Telemetry for each car
    nodes = net.cars + net.aps + [sta1]
    net.telemetry(
        nodes=nodes,
        data_type='position',
        min_x=2000,
        min_y=2000,
        max_x=4000,
        max_y=4000)

    #Give SUMO and Mininet time to begin
    time.sleep(5)
    #start Emergency vehicle server and open xterm window
    print("Starting Socket Server on Emergency Vehicle Server\n")
    makeTerm(sta1, title="Emergency Vehicle Server",
    cmd="python3 emergency_server.py; read")

    #start Car1 server socket and open xterm window
    print("Starting Socket Server on car1 listening for crash\n")
    car1 = net.get('car1')
    makeTerm(car1, title="Crash Listener",
    cmd="python3 car1.py; read")
    print("Crash Listener on car1")

    #start crash message from car2 and open xterm window
    time.sleep(45)
    print("Sending Car2 Crash Message")
    car2 = net.get('car2')
    makeTerm(car2, title="Crash Message",
    cmd="python3 car2.py; read")

    #start Mininet CLI
    print("Running CLI\n")

    #stop Mininet CLI
    CLI(net)
    net.stop()

    os.system("pkill xterm")

if __name__ == '__main__':
    setLogLevel('info')
    topology()
