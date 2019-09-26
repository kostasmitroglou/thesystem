import socket
import yaml

def send_log(message,communication):
    with open('log.yml') as f:
        data=yaml.load(f,Loader=yaml.FullLoader)
        print(data)
    send_log_host = data['log']['host']
    send_log_port = data['log']['port']
    if str(communication) == "tcp" :
        try:
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect((send_log_host, send_log_port))
            send_socket.send(message)
            send_socket.close()
        except:
            print("Don't send data via tcp")
    elif str(communication) == "udp":
        try:
            send_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            send_socket.sendto(message,(send_log_host,send_log_port))
            send_socket.close()
        except:
            print("Don't send data via udp")
    else:
        print("Error send log")