# -*- coding: utf-8 -*-
import sqlite3
import sys
import openpyxl #Remover
from subprocess import call
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont
import ipaddress
from time import gmtime, strftime #time
import threading
from threading import Thread, current_thread


'''
--bd_sqlite.py--
Function: Responsavel para manipulação e execução dos projetos.
'''

#Variaveis globais -REMOVER
#BD_SCRIPT='/rosie/www/scripts/db_scripts.db'


#-------------------------
#Função para iniciar o projeto local
def start_project(project_name, DB_SCRIPT,IMGAE_CONF):
    print ("Iniciando o projeto:", project_name)

    #Abrir banco de scripts
    print ("Banco utilizado: " + DB_SCRIPT)
    db_commands = sqlite3.connect('/rosie/www/scripts/'+DB_SCRIPT)
    cursor_commands = db_commands.cursor()

    #Abrir banco do projeto
    db_project = sqlite3.connect('/rosie/www/projects/'+project_name)
    cursor_project = db_commands.cursor()

    #Checar status da threading
    for thread_check in threading.enumerate():
        if thread_check.name == project_name:
            break

    #Iniciar coleta de evidencia
    a = db_project.execute("SELECT * FROM project;")
    for row in a:
        #Check status threading
        if thread_check._is_stopped == True:
            db_commands.close()
            db_project.close()
            sys.exit()

        #Buscar comando do db_script com base do ID_GRUPO
        cursor_commands.execute("SELECT TOOL, PAYLOAD, REGEX FROM CORE_SCRIPTS WHERE ID_GRUPO=?;", (row[1],))
        b = cursor_commands.fetchall()

        if len(b) == 0:
            cursor_commands.execute("SELECT TOOL, PAYLOAD, REGEX FROM CORE_SCRIPTS WHERE ID_GRUPO=?;", (666,))
            comando = cursor_commands.fetchall()
            for comando in comando:
                comando=comando
            #Teste protocolo UDP
            if str(row[4]) == 'udp':
                    payload=(comando[0]+' -p '+ str(row[3]) + ' -sU '+ comando[1] + ' ' + str(row[2]) +' '+ str(comando[2]) )
                    print (payload)
                    palavra = subprocess.check_output(payload, shell=True)
                    screen(palavra, project_name, str(row[1]), str(row[0]), int(IMGAE_CONF[0]), int(IMGAE_CONF[1]), tuple(IMGAE_CONF[2]), tuple(IMGAE_CONF[3]))
            else:
                payload=(comando[0] +' -p '+ str(row[3]) + ' '+ comando[1] + ' ' + str(row[2]) + ' '+ str(comando[2]) )
                print (payload)
                palavra = subprocess.check_output(payload, shell=True)
                screen(palavra, project_name, str(row[1]), str(row[0]), int(IMGAE_CONF[0]), int(IMGAE_CONF[1]), tuple(IMGAE_CONF[2]), tuple(IMGAE_CONF[3]))

        else:
            comando = b
            for comando in comando:
                comando=comando
            #Teste protocolo UDP
            if str(row[4]) == 'udp':
                    payload=(comando[0] +' -p'+ str(row[3]) + ' -sU '+ comando[1] + ' ' + str(row[2]) + ' ' + str(comando[2]))
                    print (payload)
                    palavra = subprocess.check_output(payload, shell=True)
                    screen(palavra, project_name, str(row[1]), str(row[0]), int(IMGAE_CONF[0]), int(IMGAE_CONF[1]), tuple(IMGAE_CONF[2]), tuple(IMGAE_CONF[3]))
                    #image(palavra, str(row[0]))
            else:
                payload=(comando[0] +' -p'+ str(row[3]) +' '+ str(comando[1]) + ' ' + str(row[2]) +' '+ str(comando[2]) )
                print (payload)
                palavra = subprocess.check_output(payload, shell=True)
                screen(palavra, project_name, str(row[1]), str(row[0]), int(IMGAE_CONF[0]), int(IMGAE_CONF[1]), tuple(IMGAE_CONF[2]), tuple(IMGAE_CONF[3]))
                #image(palavra, str(row[0]))
    print ("Operation done successfully")
    db_commands.close()
    db_project.close()


#-------------------------
#Função para listar todo o banco de dados de scripts
def core_scripts(DB_SCRIPT):
    db_commands = sqlite3.connect(BD_SCRIPT)
    cursor = db_commands.cursor()
    a = db_commands.execute("SELECT * FROM CORE_SCRIPTS;")
    for row in a:
       print ("ID_GRUPO = ", row[0])
       print ("TOOL = ", row[1])
       print ("PAYLOAD = ", row[2])
       print ("VALIDACAO = ", row[3])
       print ("RECOMENDACAO = ", row[4])
    print ("Operation done successfully");
    db_commands.close()

#-------------------------
#Função recebe um ID_GROUP consulta o BD de scripts e traz o payload
def teste_attack(ID_GROUP,DB_SCRIPT):
    db_commands = sqlite3.connect(BD_SCRIPT)
    cursor = db_commands.cursor()
    a = db_commands.execute("SELECT TOOL, PAYLOAD, REGEX FROM CORE_SCRIPTS WHERE ID_GRUPO=?;", (ID_GROUP,))
    linha = a.fetchall()
    for linha in linha:
        comando=linha
    db_commands.close()
    #print(comando)
    #print("Comando: tool + payload:\n", comando[1])
    payload=(comando[0]+' '+ comando[1] + ' ' + '192.168.6.1 -p 22')
    palavra = subprocess.check_output(payload, shell=True)
    image(palavra, 666)

#-------------------------
#Função para buscar comando no banco
#Em desenvolvimento [BUG]
def return_string_attack(ID_GROUP, DB_PROJECT):
    #Buscar ID no bando de comandos
    db_commands = sqlite3.connect('../db/commanddb')
    cursor = db_commands.cursor()
    #SELECT ID_GROUP, STRING_COMMAND FROM CORE_SCRIPT WHERE = ?;
    a = db_commands.execute("""
    SELECT ID_GROUP FROM CORE_SCRIPT WHERE = ?
    """, (ID_GROUP))
    print (a)
    db_commands.close()

#-------------------------
#Função para transformar um texto em imagem
def image(string_text, id_vul):
    evidencia = Image.new('RGB', (480,300))
    d = ImageDraw.Draw(evidencia)
    d.text((0,0), string_text, fill=(255,255,255))
    evidencia.save('/rosie/www/evidencias/'+str(id_vul)+'.png')
    #out.show()

#-------------------------
#Função para transformar um evidencias do GAT em imagem
def screen(STRING_TEXT, PROJECT, ID_GROUP, ID_VUL, HEIGHT, WIDTH, BACKGROUND, COLOR_TEXT):
    #---------------------------------------------------
    #Iniciar tratamento de parametros
    #---------------------------------------------------
    evidencia = Image.new('RGB', (HEIGHT,WIDTH), tuple(BACKGROUND) )
    PROJECT = PROJECT.replace('.db','')
    d = ImageDraw.Draw(evidencia)
    #date = 'Date: '+strftime("%d-%m-%Y %H:%M:%S", gmtime())
    #d.text((0,0), STRING_TEXT, fill=(R_TEXT,G_TEXT,B_TEXT))
    d.text((0,0), STRING_TEXT, fill=tuple(COLOR_TEXT))
    #Validar se pasta do projeto existe, nao existente cira uma nova pasta
    if not os.path.exists('/rosie/www/evidencias/'+str(PROJECT)):
        os.mkdir('/rosie/www/evidencias/'+str(PROJECT))
    #Checa se a pasta do id_grupo existe, nao existente cira uma nova pasta
    if not os.path.exists('/rosie/www/evidencias/'+str(PROJECT)+'/'+str(ID_GROUP)):
        os.mkdir('/rosie/www/evidencias/'+str(PROJECT)+'/'+str(ID_GROUP))

    path = '/rosie/www/evidencias/'+str(PROJECT)+'/'+str(ID_GROUP)+'/'
    evidencia.save(path+str(ID_VUL)+'.png')

#-------------------------
#Função para alterar o status da vulnerabilidade no banco
def vul_update( ID, STATUS, DB_PROJECT ):
    conn = sqlite3.connect('../projects/'+DB_PROJECT+'.db')
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE project
    SET ESTADO = ?
    WHERE ID = ?
    """, (STATUS, ID))
    conn.commit()
    conn.close()

#-------------------------
#Função para abrir um projeto existente
def listarbd(a):
    pont = a.cursor()
    a = pont.execute("SELECT * FROM CORE_SCRIPT;")

    for row in a:
       print ("ID = ", row[0])
       print ("COMANDO = ", row[1])
       print ("DESCRIÇÃO = ", row[2])
       print ("")
    print ("Operation done successfully")

    a.close()

def open_p( project ):
    #opp = raw_input("Projeto:")
    opp = project
    print ("Localizando projeto " + opp)
    op_project = sqlite3.connect('../projects/' + opp + '.db')
    #op_project = sqlite3.connect('../db/' + opp)
    listarbd(op_project)
