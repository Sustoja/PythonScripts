# Script para cambiar el servidor DNS según si estamos conectados a la Wi-Fi de casa o no.
# En la de casa usamos la IP del docker con Pi-Hole para evitar la publicidad
# Octubre 2024
#!/bin/sh

#ssid=$(networksetup -getairportnetwork en0 | awk -F ": " '{print $2}') Esta versión dejó de funcionar con MacOS Sequoia (17-9-2024)
ssid=$(system_profiler SPAirPortDataType | awk '/Current Network Information/ {getline; print substr($1, 1, length($1) - 1); exit}')

if [ "$ssid" = "patsus23" ]; then
    networksetup -setdnsservers Wi-Fi 192.168.1.23
else
    networksetup -setdnsservers Wi-Fi 1.1.1.1
fi
