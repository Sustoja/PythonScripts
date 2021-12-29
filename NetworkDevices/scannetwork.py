# Script to scan open ports. Output by console
# It also creates a file 'hosts.txt'
# with all boxes where ssh is enabled
# so Ansible 'hosts' can be easily configured.
#
# Must be run with root privileges (sudo)

import nmap

# Range of addresses and ports to scan
cidr = '192.168.1.0/24'
ports = '22,80,443'

nm = nmap.PortScanner()
nm.scan(hosts=cidr, arguments=f"-sS -p {ports}")
sshservers = []

for host in sorted(nm.all_hosts(), key=lambda x: tuple(map(int, x.split('.')))):
    print('----------------------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    try:
        if 'mac' in nm[host]['addresses']:
            v = list(nm[host]['vendor'].values())
            print(v[0])
    except:
        pass
    # print('State : %s' % nm[host].state())
    for proto in nm[host].all_protocols():
        # print('----------')
        # print('Protocol : %s' % proto)
        lport = nm[host][proto].keys()
        # lport.sort()
        for port in lport:
            # print ('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
            if (port == 22) and (nm[host][proto][port]['state'] == 'open'):
                sshservers.append('%s - %s (%s)' % (host, v[0], nm[host].hostname()))

hostsfile = open("hosts.txt", "w")
for server in sshservers:
    hostsfile.write(server + "\n")
hostsfile.close()
