# Nome: Rosie Community
# Versão: 0.0.1
# Autor: Pupilo
# Descrição:
# Imagem Community para a aplicação de retestes automatizados de vulnerabilidades.
# docker run -it --name rosie-community -p 80:80 -v /$PATH/Evidencias:/Evidencias rosie:X.X /bin/bash

#Imagem base
FROM python
MAINTAINER Pupilo <willian.mayan@ibliss.com.br>

#Pacotes base
RUN apt-get update && apt-get install -y \
	python-flask\
	python-flask-autoindex\
	sqlite3\
	nmap

#Dependencias python
RUN pip install Flask-Bootstrap openpyxl

#Dependencias
RUN pip install 'Pillow >=2.0.0,<=3.0.0'
RUN pip install sshtunnel >=0.1.2

LABEL Description="Rosie Community."
WORKDIR /root

#Instalando sistema
COPY entrypoint.sh /root
#Descometar a linha abaixo após homologar!
#RUN chmod +x /root/entrypoint.sh
