#!/usr/bin/env bash
# sets up nginx web servers for the deployment of web_static
apt-get -y update
apt-get -y install nginx
ufw allow 'Nginx HTTP'
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
chown -R "ubuntu:ubuntu" /data/
echo "Hi Max" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
sed -i '1,/error.log;/!d' /etc/nginx/nginx.conf
echo "
        server {
                listen 80 default_server;
                listen [::]:80 default_server;
                root /var/www/html;
                index index.html index.htm index.nginx-debian.html;
                server_name _;
                rewrite /redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;
                error_page 404 /custom_404.html;
                location = /custom_404.html {
                        root /var/www/html;
                        internal;
                }
                location / {
                        try_files \$uri \$uri/ =404;
                }
                location /hbnb_static {
                        alias /data/web_static/current/;
                }
        }
}" | sudo tee -a /etc/nginx/nginx.conf
service nginx start
service nginx restart
