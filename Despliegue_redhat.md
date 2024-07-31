# Configuración Flet Environment

Subir la carpeta StrataGenAI a la carpeta de usuario del servidor. con este formato:

```
 StrataGenAI
├──  assets
│   ├──  favicon.png
│   ├──  icons
│   │   ├──  favicon.png
│   │   ├──  loading-animation.png
│   │   └──  loading-animation2.png
│   ├──  index.html
│   └──  manifest.json
├──  default
├──  flet.service
├──  main.py
├──  readme.md
├──  requirements.txt
└──  test_requests.py
```

Instalamos python 3.8

```bash
sudo yum update -y
sudo yum install python38 -y
```

comprimimos la carpeta StrataGenAI en un archivo tar.gz con el comando:

```bash
tar -czvf StrataGenAI.tar.gz StrataGenAI
```

subimos el archivo . tar.gz a la carpeta de usuario del servidor

descomprimimos el archivo .tar.gz con el comando:

```bash
tar -xzvf StrataGenAI.tar.gz
```

- Navegamos a la carpeta StrataGenAI y Crear un virtualenv e instalar requisitos:

```bash
    cd StrataGenAI
    sudo pip3.8 install -r requirements.txt
```

Para dar permisos de ejecución a todos los archivos de la carpeta StrataGenAI

```bash
sudo chmod +x -R StrataGenAI/
```

Para dar permisos de lectura, escritura y ejecución a todos los archivos de la carpeta StrataGenAI

```bash
sudo chmod 777 -R StrataGenAI/
```

Navegar a la carpeta StrataGenAI

```bash
cd StrataGenAI
```

- consultamos el usuario y el grupo al que pertenecemos

```bash
groups
```

devolvera algo como esto:

```bash
francopaolo_rossi adm video google-sudoers
```

- modificamos el usuario, el grupo, y los paths en el archivo flet.service para que coincidan con los nuestros y lo guardamos

```bash
cd /etc/systemd/system
sudo nano flet.service # vi flet.service
```

Archivo `flet.service`

```bash
[Unit]
Description=Flet Server
After=network.target

[Service]
User=francopaolo_rossi
Group=google-sudoers
WorkingDirectory=/home/francopaolo_rossi/StrataGenAI
#Environment="PATH=/home/francopaolo_rossi/StrataGenAI/.venv/bin"
ExecStart=/usr/bin/python3.8 /home/francopaolo_rossi/StrataGenAI/main.py --serve-in-foreground

[Install]
WantedBy=multi-user.target
```

Habilite el servidor Flet

```bash
#cd /etc/systemd/system
sudo ln -s /home/B000001/StrataGenAI/flet.service
sudo systemctl start flet
sudo systemctl enable flet
sudo systemctl status flet
```

# instalacion de Nginx en RHEL 8

```bash
# actualizamos la lista de paquetes
sudo yum update -y

# instalamos nginx
sudo yum install nginx -y

```

Para aplicar ajustes al firewall para HTTP y HTTPS, siga estos pasos:

Verifique el estado actual del firewall.

```bash
sudo firewall-cmd --state
```

Si el firewall está activo, el comando devolverá algo como esto:

```bash
running
```

Abrimos los puertos 80 y 443 en el firewall para permitir el tráfico HTTP y HTTPS.

```bash
sudo firewall-cmd --permanent --add-port={80/tcp,443/tcp}
sudo firewall-cmd --reload
```

Habilite el servicio nginx para que se inicie automáticamente al arrancar el sistema:

```bash
sudo systemctl enable nginx
```

Inicie el servicio nginx:

```bash
sudo systemctl start nginx
```

Verifique el estado del servicio nginx:

```bash
sudo systemctl status nginx
```

Compruebe que el servicio nginx está activado:

```bash
sudo systemctl is-enabled nginx
```

recibira algo como esto:

```bash
enabled
```

Compruebe que el servicio nginx está en ejecución:

```bash
sudo systemctl is-active nginx
```

recibira algo como esto:

```bash
active
```

Establezca el parámetro booleano httpd_can_network_connect SELinux en 1 para configurar que SELinux permita a NGINX reenviar el tráfico:

```bash
sudo setsebool -P httpd_can_network_connect 1
```

reiniciamos el servicio nginx:

```bash
sudo systemctl restart nginx
```

Para verificar que el servidor web se está ejecutando, abra su navegador web y vaya a la dirección IP pública de su servidor.

http://stratagenai-prod.gcp.cloudteco.com.ar

Si la instalación fue exitosa, verá la página de inicio de Nginx, que se ve así:

![Alt text](https://assets.digitalocean.com/articles/lemp_centos8/nginx_default_page.png)

# Configuración de Nginx

- Navegamos a la carpeta de configuración de nginx

```bash
cd /etc/nginx
```

- Creamos una copia de seguridad del archivo nginx.conf

```bash
sudo cp nginx.conf nginx.conf.bak
```

- Editamos el archivo nginx.conf

```bash
sudo nano nginx.conf
```

- Editamos las siguientes lineas:

```bash

location / {
        proxy_pass         http://127.0.0.1:8502/;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection keep-alive;
        proxy_set_header   Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
}
location /ws {
        proxy_pass         http://127.0.0.1:8502/ws;
        proxy_http_version 1.1;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;

	}
```

- Guardamos el archivo nginx.conf

- Recargamos el servicio nginx

```bash
sudo systemctl reload nginx
```

## Certificado SSL para Nginx con Let's Encrypt y Certbot en RHEL 8 utilizando snap

- El repositorio EPEL se puede agregar a un sistema RHEL 8 con el siguiente comando:

```bash
sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
sudo dnf upgrade
```

- Instalamos snapd

```bash
sudo yum install snapd -y
```

- Habilitamos el servicio snapd

```bash
sudo systemctl enable --now snapd.socket
```

- Habilitamos el servicio snapd

```bash
sudo ln -s /var/lib/snapd/snap /snap
```

- instalamos certbot

```bash
sudo snap install --classic certbot
```

- Ejecutamos el siguiente comando para que cerbot pueda ejecutarse en el sistema

```bash
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

- Ejecutamos el siguiente comando para obtener un certificado SSL y configurar Nginx para usarlo

```bash
sudo certbot --nginx
```

- seguimos las instrucciones de certbot para configurar el certificado SSL automaticamente en nginx y redirigir el trafico de http a https solicitara un correo electronico y un dominio para el certificado SSL

- Reiniciamos el servicio nginx

```bash
sudo systemctl restart nginx
```

- para renovar automaticamente el certificado SSL ejecutamos el siguiente comando

```bash
sudo certbot renew --dry-run
```

- El comando para renovar certbot se instala en una de las siguientes ubicaciones:

```bash
/etc/crontab/
/etc/cron.*/*
systemctl list-timers
```

- Verificamos que el certificado SSL este funcionando correctamente

```bash
https://server_domain_or_IP
```
