# Script to change DNS server depending on what Wi-Fi we are
# connected to: a Pi-Hole server at home, a public DNS elsewhere
# Feb. 2023

import macwifi as wifi
import os
import pync

# Check Wi-Fi SSID and decide what DNS server applies
ssid = wifi.get_ssid()
if ssid == 'patsus23':
    newdns = '192.168.1.23'
else:
    newdns = '1.1.1.1'

# Change DNS server in macOS and notify the user
command = 'networksetup -setdnsservers Wi-Fi '
os.system(command + newdns)
pync.notify("Wi-Fi: " + ssid + '\n' + "DNS: " + newdns, title='Python')
