# -*- coding: utf-8 -*-
import sqlite3
import sys
import csv

'''
--bd_sqlite.py--
Function: Responsavel para manipulação do banco de dado sqlite
'''

#Variaveis globais

#Função para criar projeto importando CSV
def csv_project( p_name, file_name ):
    conn = sqlite3.connect('/rosie/www/projects/' + p_name + '.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE project(
    ID_EVIDENCE INTERGER NOT NULL PRIMARY KEY,
    ID_GROUP TEXT NOT NULL,
    IP INTERGER NOT NULL,
    PORT INTERGER NOT NULL,
    PROTOCOL TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE info_project(
    TIPO TEXT NOT NULL,
    STATUS TEXT NOT NULL,
    ID_INTERRUPT INTERGER
    );
    """)

    project_info = [ 'CSV', 'STOP']
    cursor.executemany("""
            INSERT INTO info_project (TIPO,STATUS)
            VALUES (?,?)""",[project_info])
    conn.commit()
    #Preencher o banco
    print("Nome do arquivo:", file_name )
    path = '/rosie/www/files/'+file_name
    f = open(path, 'r')
    with f:
        read = csv.DictReader(f)
        for row in read:
            value_insert = [row['ID_EVIDENCE'], row['ID_GROUP'], row['IP'], row['PORT'], row['PROTOCOL']]
            cursor.executemany("""
                    INSERT INTO project (ID_EVIDENCE,ID_GROUP,IP,PORT,PROTOCOL)
                    VALUES (?,?,?,?,?)""",[value_insert])
            conn.commit()
    print("Dados inseridos com sucesso")
    conn.close()
    return 0

#-------------------------
#Função para listar o banco de dados de comandos
def list_commanddb():
    db_commands = sqlite3.connect('../db/commanddb')
    cursor = db_commands.cursor()
    a = db_commands.execute("SELECT * FROM CORE_SCRIPT;")
    for row in a:
       print ("ID = ", row[0])
       print ("COMANDO = ", row[1])
       print ("DESCRIÇÃO = ", row[2])
       print ("")
    print ("Operation done successfully");
    db_commands.close()

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


#Consuldar ID GRUPO
def querry_id_grupo(ID_GRUPO, DBSCRIPT):
    db_commands = sqlite3.connect('/rosie/www/scripts/'+DBSCRIPT)
    cursor = db_commands.cursor()
    a = db_commands.execute("SELECT TOOL, PAYLOAD, REGEX FROM CORE_SCRIPTS WHERE ID_GRUPO=?;", (ID_GRUPO,))
    linha = a.fetchall()
    if not linha:
        return None
    else:
        for linha in linha:
            comando=linha
        db_commands.close()
        return comando

#Adicionar script ap BD
def querry_add_id(ID_GRUPO, TOOL, PAYLOAD, REGEX, DBSCRIPT):
    #print (ID_GRUPO, TOOL, PAYLOAD, REGEX, DBSCRIPT)
    db_commands = sqlite3.connect('/rosie/www/scripts/'+DBSCRIPT)
    cursor = db_commands.cursor()
    #Verificar ID
    a = db_commands.execute("SELECT ID_GRUPO FROM CORE_SCRIPTS WHERE ID_GRUPO=?;", (ID_GRUPO,))
    linha = a.fetchall()
    if not linha:
        print("Nulo inserir os dados")
        valor = []
        valor.append(ID_GRUPO)
        valor.append(TOOL)
        valor.append(PAYLOAD)
        valor.append(REGEX)
        cursor.executemany("""INSERT INTO CORE_SCRIPTS (ID_GRUPO, TOOL, PAYLOAD, REGEX)VALUES (?,?,?,?)""", [valor])
        db_commands.commit()
        db_commands.close()
        msg = "ID inserted successfully!!"
        return msg
    else:
        db_commands.close()
        msg = "ID GROUP already exists!!"
        return msg

#Adicionar script ap BD
def querry_remove_id(ID_GRUPO, DBSCRIPT):
    db_commands = sqlite3.connect('/rosie/www/scripts/'+DBSCRIPT)
    cursor = db_commands.cursor()
    #Verificar ID
    a = db_commands.execute("SELECT ID_GRUPO FROM CORE_SCRIPTS WHERE ID_GRUPO=?;", (ID_GRUPO,))
    linha = a.fetchall()
    if not linha:
        db_commands.close()
        msg = "ID " + ID_GRUPO + " not found in the " + DBSCRIPT
        return msg
    else:
        cursor.execute("""DELETE FROM CORE_SCRIPTS WHERE ID_GRUPO=?;""", (ID_GRUPO,))
        db_commands.commit()
        db_commands.close()
        msg = "ID removed!!"
        return msg
