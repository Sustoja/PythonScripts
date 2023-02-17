#!/bin/sh

fswatch -o  /Library/Preferences/com.apple.wifi.known-networks.plist | xargs -n1 -I {} /Users/ja/PycharmProjects/DNSCasa/cambiaDNS.sh &
/Users/ja/PycharmProjects/DNSCasa/cambiaDNS.sh
