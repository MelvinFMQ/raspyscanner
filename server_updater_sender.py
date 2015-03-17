import socket
import sys
import base64

file_name, rasp_pi_id = sys.argv[1], sys.argv[2]
host = '192.168.1.1{0:0>#2}'.format(int(rasp_pi_id))  # up to 99 raspberry pis
port = 5000


def connect():
    print('Connecting to Host: {0}, Port: {1}'.format(host, port))
    file_socket = socket.socket()
    file_socket.connect((host, port))
    return file_socket


def send(file_socket):
    #python3.4 input gives a unicode string, encode to change to byte string
    #just use 2.7 to make it simplier
    #split photo into 1024 byte chucks
    with open(file_name, 'rb') as updated_file:
        encoded_file = base64.b64encode(updated_file.read())
        encoded_string = file_name + '|' + encoded_file
        print('Sending updated file to Raspberry Pi {0}'.format(rasp_pi_id))
        for i in range((len(encoded_string)//1024)+1):
            message = encoded_string[i*1024:(i+1)*1024]
            file_socket.send(message)
        print('Sucessfully Sent to Raspberry Pi {0}'.format(rasp_pi_id))
        file_socket.close()

try:
    connected_socket = connect()
    send(connected_socket)
except socket.error as e:
    if not str(e).find('Errno 60'):
        print('Unknown error when connecting to Raspberry pi {0}: {1}'.format(rasp_pi_id, e))
    else:
        print('Having problems connecting to Raspberry Pi {0} ethernet is probably loose'.format(rasp_pi_id))