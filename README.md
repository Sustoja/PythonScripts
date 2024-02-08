# Python Scripts

## Scripts para automatizar tareas


### Empleo Público
Web Scraping para extraer las ofertas de empleo público del BOE, el Ayuntamiento de Madrid y la 
Comunidad de Madrid. El resumen de cada boletín lo envía por correo a la dirección que se le indique, en 
HTML y con enlaces directos para la descarga de los PDF correspondientes.

<p align="center">
<img src="https://github.com/Sustoja/PythonScripts/blob/main/images/CorreoBOE.jpg?raw=true" width="800">
</p>

Para automatizar el envío diario de las ofertas de empleo se puede programar un cron similar a este:

`2 9 * * * python3 /etc/scriptsJA/EmpleoPublico/empleoPublico.py > /dev/null`

---

### My IP
Chequea la dirección IP publica y envía un correo con la nueva si el proveedor de Internet nos la ha
cambiado. Lo empleo para actualizar el cliente VPN con el que accedo a la red de casa sin necesidad de registrarme 
en un servicio externo de DNS dinámico como, por ejemplo, [Duck DNS](http://www.duckdns.org).

El script lo programo con un cron para que se ejecute cada hora. Me aseguro de que funciona correctamente integrandolo
en el cuadro de mandos de [Uptime Kuma](https://github.com/louislam/uptime-kuma), que se ocupa de avisarme si falla
cualquiera de los servicios monitorizados (Internet, DNS, NAS...)

<p align="center">
<img src="https://github.com/Sustoja/PythonScripts/blob/main/images/CronCheckUptime.jpg?raw=true" width="800">
</p>

El "latido" que indica que el script se ejecuta correctamente cada hora se integra en el propio cron mediante una
llamada a una URL que proporciona Uptime Kuma y que es individual para cada servicio monitorizado:

`@hourly python3 /etc/scriptsJA/My_IP/my_IP.py > /dev/null && curl -fsS -o /dev/null  http://uptime.casa/api/push/EP8eDjOCYv?`

---

### DNS Casa
Cambia el servidor DNS configurado en macOS en función de la red Wi-Fi a la que estemos conectados. Por ejemplo,
en casa usamos un servidor Pi-Hole para evitar la publicidad pero cuando estamos fuera utilizamos un servidor
DNS público.

---

### Network Devices
Detecta todos los equipos con ssh activado y genera un prototipo de fichero 'hosts' que se puede 
adaptar facilmente para usarlo como inventario para [Ansible](https://github.com/Sustoja/Ansible).

---

## Scripts para probar tecnologías y algoritmos

### Cifrado Simétrico
Cifra y descifra cualquier fichero usando clave simétrica proporcionada por el usuario.

### Criptografía
Ejemplos de tecnología blockchain básica y de compresión de datos.
