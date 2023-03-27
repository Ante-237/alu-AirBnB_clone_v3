#!/usr/bin/env bash
# code creat directory structures install nginx

if ! which nginx > /dev/null; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/


sudo echo "<html><head><title> Test page</title></head><body><p> This is a test page. </p></body></html>" | sudo tee /data/web_static/releases/test/index.html


sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sed -i '/listen 80 default_server;/a \ \n    location /hbnb_static {\n        alias /data/web_static/current/;\n        index index.html;\n    }' /etc/nginx/sites-available/default

service nginx restart
