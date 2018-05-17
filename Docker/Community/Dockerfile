# Nome: Rosie
# Versão: 0.0.2 Rosie Community
# Autor: Pupilo
# Descrição
#  Imagem para desenvolvimento da aplicação de retestes automatizados de vulnerabilidades.
# Modo de uso:
# docker run --rm -it -v $PATH/evidencias:/rosie/www/evidencias -p 80:80 rosie-community:0.2 /bin/bash

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

LABEL Description="Container para reteste de vulnerabilidades."
WORKDIR /root

#Instalando sistema
COPY entrypoint.sh /root
RUN chmod +x /root/entrypoint.sh
COPY rosie.tar.gz /root
RUN tar -xvf rosie.tar.gz
RUN mv rosie /
RUN rm -rf rosie.tar.gz
RUN ln -s /evidencias /rosie/www/scripts
ENTRYPOINT ["./entrypoint.sh"]
