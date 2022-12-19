
import nmap
import sys
import os

# nm = nmap.PortScannerAsync()
nm = nmap.PortScanner(nmap_search_path=('nmap', r"D:\Program Files (x86)\Nmap"))
#
def nmap_port_scan(arguments):
    host_port = []
    nm.scan( arguments=arguments)
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()  #   80   443   8080  8090
            for port in lport:
                if nm[host][proto][port]['state'] == 'open':
                    host_port.append(str(host) + ':' + str(port))
    return host_port

__all__ = ["nmap_port_scan"]