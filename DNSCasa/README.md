# Cambio automático del DNS en MacOS

Se trata de un sistema compuesto por un demonio del sistema operativo y un script que configura un servidor DNS u otro
según el nombre de la red wifi a la que está conectado el ordenador.

En mi caso, esto hace que en casa utilice el DNS del servidor Pi-Hole en mi red local para eliminar los
anuncios al navegar por la web, mientras que fuera utilice un servidor DNS público (Cloudflare, por ejemplo).

## JA_DNS_Daemon.plist
Fichero de configuración del agente de usuario que es interpretados por el servicio 
[launchd](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html#//apple_ref/doc/uid/10000172i-SW7-BCIEDDBJ). 
Una vez definido, se pone en marcha de la siguiente manera (no hace falta sudo):
```shell

chmod 600 JA_DNS_Daemon.plist
cp JA_DNS_Daemon.plist /Library/LaunchAgents
launchctl load /Library/LaunchAgents/JA_DNS_Daemon.plist
```

Si lo tenemos que modificar, por ejemplo durante las pruebas, hay que desactivarlo con **unload**, editarlo 
y volverlo a activar con **load**: 
```shell

launchctl unload /Library/LaunchAgents/JA_DNS_Daemon.plist

vi /Library/LaunchAgents/JA_DNS_Daemon.plist

launchctl load /Library/LaunchAgents/JA_DNS_Daemon.plist
```

## JA_DNS_Daemon.sh
Script de shell que comprueba el nombre de la wifi y actualiza el DNS. Actualizado para MacOS Sequoia.
