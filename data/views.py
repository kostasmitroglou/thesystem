from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from data.models import Data
from django.contrib.auth import logout
from .forms import  UserForm
from django.core.mail import send_mail
import datetime
from django.template import Context
import logging
import sqlite3
# Create your views here.

def data_index(request):
    if request.method == "POST":
        server_name = request.POST['server_name']
        database_sqlite = sqlite3.connect("db.sqlite3")
        cursor = database_sqlite.cursor()
        cursor.execute("insert into search_data VALUES ('%s','%s')" % (str(datetime.datetime.now()), str(server_name),))
        database_sqlite.commit()
        database_sqlite.close()
        data_index_ip_address = request.META.get('REMOTE_ADDR')
        logging.basicConfig(filename='logging/data_index.log', level=logging.DEBUG)
        log = str(server_name)+"|"+str(data_index_ip_address) + "|"+ str(datetime.datetime.now()) + " \n"
        logging.info(log)
        database_sqlite = sqlite3.connect("db.sqlite3")
        cursor = database_sqlite.cursor()
        cursor.execute("select * from data_data where server_name='%s'" %(server_name))
        context = cursor.fetchall()
        print(context)
        database_sqlite.close()
        if len(context)>0:
            return HttpResponse(context)
        else:
            search_data="Didn't find server name:"+server_name
            return HttpResponse(search_data)
    else:
        data_index_ip_address = request.META.get('REMOTE_ADDR')
        log = str(data_index_ip_address) + "|" + str(datetime.datetime.now()) + " \n"
        logging.basicConfig(filename='logging/data_index.log', level=logging.DEBUG)
        logging.info(log)

        datas = Data.objects.all()
        context = {
            'datas' : datas
        }
        print(context)
        return render(request,'data_index.html',context)

def data_detail(request,pk):
    email_to="test@test"
    data_index_ip_address = request.META.get('REMOTE_ADDR')
    data = Data.objects.get(pk=pk)
    email_content="IP Address:"+str(data.ip_address)+"\n"
    email_content+="Port:"+str(data.system_port)+"\n"
    email_content+="System Username:"+str(data.system_username)+"\n"
    email_content+="System Password:"+str(data.system_password)+"\n"
    logging.basicConfig(filename='logging/data_detail_log.log', level=logging.DEBUG)
    log = str(pk) + "|" + str(data_index_ip_address) +  "|" + str(
        datetime.datetime.now()) + " \n"
    logging.info(log)
    send_mail("Take Credential Alert",log,"django@test",[email_to,str(data.system_owner)])
    try:
        import zeep
        wsdl = 'http://localhost:9000/?wsdl'
        client = zeep.Client(wsdl=wsdl)
    except:

        log = "WSDL Client Create Error|" + str(data_index_ip_address) + "|" + str(
            datetime.datetime.now()) + " \n"
        logging.basicConfig(filename='logging/error.log', level=logging.DEBUG)
        logging.error(log)
    now = datetime.datetime.now()
    now_plus = now + datetime.timedelta(minutes=int(1))
    print(now)
    print(now_plus)
    plus_last_time = str(now_plus.strftime("%Y%m%d%H%M"))
    try:
        if (client.service.test_api_key('web_service') == "Successful"):
            client.service.run_process(pk, data.ip_address, data.system_username, data.system_password, data.system_port,
                                       plus_last_time)
    except:
        log = "WSDL Client Error|" + str(data_index_ip_address) + "|" + str(
            datetime.datetime.now()) + " \n"
        logging.basicConfig(filename='logging/error.log', level=logging.DEBUG)
        logging.error(log)
    return redirect('data_index')







def add_server(request):
    data_index_ip_address = request.META.get('REMOTE_ADDR')
    if request.method == "POST":
        try:
            data_operating_system = request.POST['operating_system']
            data_ip_address = request.POST['ip_address']
            data_system_port = request.POST['system_port']
            data_system_owner = request.POST['system_owner']
            data_system_username = request.POST['system_username']
            data_system_password = request.POST['system_password']
            data_system_description = request.POST['system_description']
            data_server_name = request.POST['server_name']
        except:

            log = "Add server POST data error|" + str(data_index_ip_address)  + "|" + str(
                datetime.datetime.now()) + " \n"
            logging.basicConfig(filename='logging/error.log', level=logging.DEBUG)
            logging.error(log)
        try:
            data = Data(
                operating_system=data_operating_system,
                ip_address=data_ip_address,
                system_port=data_system_port,
                system_owner=data_system_owner,
                system_username=data_system_username,
                system_password=data_system_password,
                system_description=data_system_description,
                server_name=data_server_name
            )
            data.save()
            log = "Add server|" + str(data_ip_address)+"|"+str(data_index_ip_address) +  "|" + str(
                datetime.datetime.now()) + " \n"
            logging.basicConfig(filename='logging/add_server.log', level=logging.DEBUG)
            logging.info(log)
        except:
            log = "Add server to save database error|" + str(data_index_ip_address) + "|" + str(
                datetime.datetime.now()) + " \n"
            logging.basicConfig(filename='logging/error.log', level=logging.DEBUG)
            logging.error(log)
        add_server_page="Add server:"+data_server_name
        return HttpResponse(add_server_page)
    return render(request,'add_server.html')


def logout_user(request):
    logout_user_ip_address = request.META.get('REMOTE_ADDR')
    log = str(logout_user_ip_address) + "|" + str(datetime.datetime.now()) + " \n"
    logging.basicConfig(filename='logging/logout.log', level=logging.DEBUG)
    logging.info(log)
    try:
        logout(request)
    except:
        log = "Logout error|" + str(logout_user_ip_address)  + "|" + str(
            datetime.datetime.now()) + " \n"
        logging.basicConfig(filename='logging/error.log', level=logging.DEBUG)
        logging.error(log)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }

    return render(request, 'login_user.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        database_sqlite = sqlite3.connect("db.sqlite3")
        cursor = database_sqlite.cursor()
        cursor.execute("""select * from login where username='%s' and password='%s'""" % (username,password,))
        login_data=cursor.fetchone()
        database_sqlite.close()
        if login_data is not None:
            login_user_ip_address=request.META.get('REMOTE_ADDR')
            log=str(username)+"|"+str(login_user_ip_address)+"|"+str(datetime.datetime.now())+" \n"
            logging.basicConfig(filename='logging/login.log', level=logging.DEBUG)
            logging.info(log)
            return redirect('data_index')
        else:
            log ="Invalid login|" + str(username) + "|" + str(
                datetime.datetime.now()) + " \n"
            logging.basicConfig(filename='logging/error.log', level=logging.DEBUG)
            logging.error(log)
            return render(request, 'login_user.html', {'error_message': 'Invalid login'})
    return render(request, 'login_user.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        database_sqlite = sqlite3.connect("db.sqlite3")
        cursor = database_sqlite.cursor()
        cursor.execute("insert into login VALUES ('%s','%s','%s')" %(username,password,email,))
        database_sqlite.commit()
        database_sqlite.close()
        return render(request, 'login_user.html')
    else:
        return render(request,'signup.html')

def show_search(request):
    database_sqlite = sqlite3.connect("db.sqlite3")
    cursor = database_sqlite.cursor()
    cursor.execute("select * from search_data")
    datas=cursor.fetchall()
    database_sqlite.close()
    print(datas)
    return HttpResponse(datas)

def show_server_data(request):
    database_sqlite = sqlite3.connect("db.sqlite3")
    cursor = database_sqlite.cursor()
    cursor.execute("select * from data_data")
    datas=cursor.fetchall()
    database_sqlite.close()
    print(datas)
    return HttpResponse(datas)

def check_users(request):
    if request.method == 'POST':
        username = request.POST['username']
        database_sqlite = sqlite3.connect("db.sqlite3")
        cursor = database_sqlite.cursor()
        cursor.execute("""select * from login where username='%s'""" % (username,))
        login_data=cursor.fetchone()
        database_sqlite.close()

        if login_data:
            log_data = "User:"+str(login_data)
        else:
            log_data="Not user"
        database_sqlite.close()
        return HttpResponse(log_data)
    else:
        return render(request,'check_users.html')

def run_command(request):
    if request.method == 'POST':
        command = request.POST['command']
        from subprocess import check_output
        result = check_output(command,shell=True)
        return HttpResponse(result)
    else:
        return render(request, 'run_command.html')