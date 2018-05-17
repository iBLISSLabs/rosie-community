# -*- coding: utf-8 -*-
#System
import os
import sys
import json
import sqlite3
import re
import threading
from threading import Thread, current_thread

#libs do sistema
sys.path.append('/rosie/www/libraries')
import libraries.bd_sqlite
import libraries.projetos

#Flask
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, flash, Markup
from flask import send_from_directory
#
from werkzeug import secure_filename

#--- Global Variables
UPLOAD_FOLDER = '/rosie/www/files/'
EXTENSIONS = set(['txt'])

#--- Scripts Directory
UPLOAD_FOLDER_DB = '/rosie/www/scripts/'
EXTENSIONS_DB = set(['db'])

#---------------------------------------------------------
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_DB']= UPLOAD_FOLDER_DB
app.config.from_pyfile('config.py')
app.secret_key = 'rosie'

#=========================================================
#                       Functions
#=========================================================

#Checar se o arquivo e da extenção permitida
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in EXTENSIONS

#Checar se o arquivo e da extenção permitida
def allowed_db(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in EXTENSIONS_DB

def create_project(name):
    print (name, file=sys.stderr)
    data = [{"name": "bootstrap-table","commits": "10","attention": "122","uneven": "An extended Bootstrap table"},
            {"name": "multiple-select","commits": "288","attention": "20","uneven": "A jQuery plugin"},
            {"name": "Testing","commits": "340","attention": "20","uneven": "For test"}]
    #return render_template('table.html', data=data)

    return data

#Função para retornar banco de scripts
def db_files():
    files = os.listdir('/rosie/www/scripts/')
    extensao = (".db")
    itens = []
    for arquivo in files:
        if arquivo.endswith(extensao):
            itens.append(arquivo)
    return itens
#=========================================================
#                       Paginas
#=========================================================

#Home
@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')


#Pagina para criação de projetos
@app.route('/nprojects', methods=['GET','POST'])
def project():
        if request.method == 'POST':
            file = request.files['file']
            name = request.form['name']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                libraries.bd_sqlite.csv_project(name, filename)
                return render_template('home.html')
            else:
                return render_template('erros/invalido.html')
        return render_template('nprojects.html')

#Pagina para gerenciamento de projetos
@app.route('/projects', methods=['GET','POST'])
def nproject():
    itens = os.listdir('/rosie/www/projects/')
    IMGAE_CONF = []
    IMGAE_CONF.append(app.config['SCREEN_HEIGHT'])
    IMGAE_CONF.append(app.config['SCREEN_WIDTH'])
    IMGAE_CONF.append(app.config['SCREEN_BACKGROUND'])
    IMGAE_CONF.append(app.config['COLOR_TEXT'])

    #Status dos projetos
    projetos_status = {}
    for i in itens:
        for thread_check in threading.enumerate():
            if thread_check.name == i:
                projetos_status[i] = 'Running'
            else:
                projetos_status[i] = 'STOPPED'

    if request.method == 'POST':
        #Iniciar projeto
        if 'project' in request.form:
            projeto = request.form['project']
            check_job = False
            #Checar se existe threads para o mesmo projeto
            for thread_check in threading.enumerate():
                if thread_check.name == projeto:
                    check_job = True
                    break

            if check_job:
                flash('Running project, please wait!')
            else:
                thread_project = threading.Thread(target=libraries.projetos.start_project,name=projeto,args=(projeto, app.config['DB_SCRIPT'],IMGAE_CONF,))
                thread_project.start()
                flash('Project ' + projeto + ' running!!')
                projetos_status[projeto] = 'Running'
            return render_template('projects.html', itens=projetos_status)
        #Download do projeto
        elif 'download' in request.form:
            projeto = request.form['download']
            print ("Iniciando download do projeto:", projeto)
            return send_from_directory(directory=app.config['PROJECTS'], filename=projeto, as_attachment=True )
        #Stop project
        if 'stop' in request.form:
                projeto = request.form['stop']
                check_job = False
                #Checar se existe threads para o mesmo projeto
                for thread_check in threading.enumerate():
                    if thread_check.name == projeto:
                        check_job = True
                        break
                if check_job:
                    thread_check._is_stopped = True
                    flash('Stoped project.')
                    print('Stoped project')
                    for i in itens:
                        for thread_check in threading.enumerate():
                            if thread_check.name == i:
                                projetos_status[i] = 'STOPPED'
                    return render_template('projects.html', itens=projetos_status)
                else:
                    flash('Project not running!')
                    return render_template('projects.html', itens=projetos_status)
    return render_template('projects.html', itens=projetos_status)

#Pagina para configuração do sistema
@app.route('/config', methods=['GET', 'POST'])
def config():

    itens = db_files()
    path = app.config['SCRIPTS_ROSIE'] #Remover path

    if request.method ==  'POST':
        #Download db_scripts
        if 'download' in request.form:
            download_db = request.form['download']
            print ("Iniciando download do arquivo:", download_db)
            return send_from_directory(directory=app.config['SCRIPTS_ROSIE'], filename=download_db, as_attachment=True )

        #Remover db_scripts
        elif 'dell' in request.form: #Remover DB
            dell_db = request.form['dell']
            if dell_db.endswith('.db'):
                os.remove(path+dell_db)
            print("Arquivo removido")
            itens = db_files()
            return render_template('config.html', itens=itens)

        #Upload db_scripts
        elif 'upload' in request.form:
            print ('Iniciando UPLOAD')
            file = request.files['file']
            if file and allowed_db(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER_DB'], filename))
                itens = db_files()
                return render_template('config.html', itens=itens)
            else:
                return render_template('erros/invalido_db.html')
        #Set default BD_SCRIPT
        elif 'default' in request.form:
            default_db = request.form['default']
            app.config['DB_SCRIPT'] = default_db
            flash('Default DB was updated to: ' + app.config['DB_SCRIPT'])
            return render_template('config.html', itens=itens)
            #O arquivo de configuração não e modificado.
        elif 'aplicar' in request.form:
            font_hex = request.form['font']
            rgb = tuple(int(font_hex.lstrip('#')[i:i+2], 16) for i in (0, 2 ,4))
            app.config['COLOR_TEXT'] = (int(rgb[0]),int(rgb[1]),int(rgb[2]))
            background_hex = request.form['background']
            rgb_background = tuple(int(background_hex.lstrip('#')[i:i+2], 16) for i in (0, 2 ,4))
            app.config['SCREEN_BACKGROUND'] = (int(rgb_background[0]),int(rgb_background[1]),int(rgb_background[2]),0)
            app.config['SCREEN_HEIGHT'] = request.form['height']
            app.config['SCREEN_WIDTH'] = request.form['width']
            return render_template('config.html', itens=itens)

    return render_template('config.html', itens=itens)

#Pagina para criação de scripts
@app.route('/scripts', methods=['GET','POST'])
def scripts():
    if request.method ==  'POST':
        #id_grupo = request.form['IDGRUPO']
        #flash("flash test!!!!", 'info')
        #print (id_grupo)

        #Consultar ID
        if 'IDGRUPO' in request.form:
            id_grupo = request.form['IDGRUPO']
            comando = libraries.bd_sqlite.querry_id_grupo(id_grupo, app.config['DB_SCRIPT'])
            if comando is None:
                flash("ID not found in the database: "+app.config['DB_SCRIPT'])
            else:
                flash(comando)
            return render_template('scripts.html')
        #Remover ID Grupo
        elif 'REMOVE' in request.form:
            id_grupo = request.form['REMOVE']
            msg = libraries.bd_sqlite.querry_remove_id(id_grupo, app.config['DB_SCRIPT'])
            flash(msg)
            return render_template('scripts.html')
        #Inserir ID Grupo
        elif 'Regex' in request.form:
            id_grupo = request.form['ID']
            #id_grupo = request.form['Tool']
            payload = request.form['Payload']
            regex = request.form['Regex']
            msg = libraries.bd_sqlite.querry_add_id(id_grupo, 'nmap', payload, regex, app.config['DB_SCRIPT'])
            flash(msg)
            return render_template('scripts.html')
    return render_template('scripts.html')
#---------------------------------------------------------
#Tratamento de erros
#Erro 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('erros/404.html'), 404


#=========================================================
#                   Start aplicação
#=========================================================
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
