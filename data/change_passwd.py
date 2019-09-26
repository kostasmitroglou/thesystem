import paramiko
import sqlite3
import datetime
import sys
import subprocess
import logging


ERROR_LOG_PATH = "../logging/error.log"
PASSWORD_CHANGE_LOG_PATH = "../logging/password_change.log"

def change_passwd(ip,username,password,port,new_password,id):
    if port=="22":
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(ip, username=username, password=password,timeout=10)
            except:
                log = "SSH server connection error via paramiko |" + str(datetime.datetime.now()) + "\n"
                logging.basicConfig(filename=ERROR_LOG_PATH, level=logging.DEBUG)
                logging.info(log)
            try:
                pass_change="echo "+str(username)+":"+str(new_password)+"|chpasswd"
                print(password)
                ssh.exec_command(pass_change)
            except:
                log = "SSH server doesn't run a command via paramiko |" + str(datetime.datetime.now()) + "\n"
                logging.basicConfig(filename=ERROR_LOG_PATH, level=logging.DEBUG)
                logging.info(log)
        finally:
            ssh.close()
    elif port=="445" or port=="3389":
        from pypsexec.client import Client
        c = Client(ip, username=username, password=password)
        c.connect()
        try:
            c.create_service()
            command="net user "+str(username)+" "+str(new_password)
            stdout, stderr, rc = c.run_executable("cmd.exe",
                                                  arguments=command)
            print(stdout)
        finally:
            c.remove_service()
            c.disconnect()
    try:
        database_sqlite = sqlite3.connect("../db.sqlite3")
        cursor = database_sqlite.cursor()
        cursor.execute("update data_data set system_password=? where id=?", (str(new_password), id))
        database_sqlite.commit()
        database_sqlite.close()
        log = str(id)+"|Password changed|" + str(datetime.datetime.now()) + " \n"
        logging.basicConfig(filename=PASSWORD_CHANGE_LOG_PATH, level=logging.DEBUG)
        logging.info(log)
    except:
        log = "Password update error on database|" + str(datetime.datetime.now()) + " \n"
        logging.basicConfig(filename=ERROR_LOG_PATH, level=logging.DEBUG)
        logging.info(log)
        log = str(id)+"|"+str(new_password)+"|Password didn't changed|" + str(datetime.datetime.now()) + " \n"
        logging.basicConfig(filename=PASSWORD_CHANGE_LOG_PATH, level=logging.DEBUG)
        logging.info(log)


change_passwd(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])