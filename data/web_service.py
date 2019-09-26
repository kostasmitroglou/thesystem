from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
flag=False
import subprocess
class WebService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def test_api_key(ctx, api_key):
        global flag
        if api_key=="web_service":
            flag=True
            return "Successful"
        else:
            flag=False
            return "Not Successful"

    @rpc(Integer,Unicode,Unicode,Unicode,Unicode,Unicode)
    def run_process(ctx, id, ip_address,username,password,port,runtime):
        global flag
        CHANGE_PASSWD_PATH = "/opt/thesystem-develop/data/change_passwd.py"
        import random
        if flag==True:
            print(id)
            s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!-"
            passlen = 8
            new_password = "".join(random.sample(s, passlen))
            run_command = "/usr/bin/python3.6 "+CHANGE_PASSWD_PATH+" " + str(ip_address) + " " + str(username) + " " + str(password) + " " + str(port) + " " + str(new_password) + " " + str(id) + "|at -t " + str(runtime)
            print(run_command)
            subprocess.call(run_command,shell=True)


application = Application([WebService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)
if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)
    logging.info("listening to http://127.0.0.1:9000")
    logging.info("wsdl is at: http://localhost:9000/?wsdl")
    server = make_server('127.0.0.1', 9000, wsgi_application)
    server.serve_forever()