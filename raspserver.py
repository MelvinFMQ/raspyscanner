__author__ = 'melvinfoo'
#script that makes raspberry pi listen for trigger
#one command is given, raspberry pi takes the photo and
#uploads it back to the broadcaster through tcp.
#version: 1.4

import socket
import struct
import base64
import subprocess
import time

print('Running version 1.4')
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5000

def get_ip():
    command = ['ip', 'addr', 'show', 'eth0']
    return_text = subprocess.check_output(command)
    start_index = return_text.find('inet') + 5
    end_index = return_text[start_index:].find('/') + start_index
    ip = return_text[start_index: end_index].replace(' ', '')
    return ip

LOCAL_IP = get_ip()
rasp_pi_id = int(LOCAL_IP.split('.')[3]) - 100

trigger_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
trigger_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
trigger_socket.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
trigger_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def send_photo(host, port, encoded_image):
    print('Connecting to Host: {0}, Port: {1}'.format(host, port))
    image_socket = socket.socket()
    image_socket.connect((host, port))
    #python3.4 input gives a unicode string, encode to change to byte string
    #just use 2.7
    #split photo into 1024 byte chucks
    print('Sending photo')
    for i in range((len(encoded_image)//1024)+1):
        message = encoded_image[i*1024:(i+1)*1024]
        image_socket.send(message)
    image_socket.close()
    print('Sent')



while True:
    data, command_computer_ip = trigger_socket.recvfrom(1024)
    print('{0} command received from {1}'.format(data, command_computer_ip))
    command_computer_ip = str(command_computer_ip[0])
    command = data
    if command == 'shutdown':
        print('Shutting down')
        cmd = 'sudo shutdown -h now'
        subprocess.call(cmd, shell=True)
    elif command == 'reboot':
        print('Rebooting')
        cmd = 'sudo reboot -h'
        subprocess.call(cmd, shell=True)
    elif command == 'update':
        print('Updating')
        cmd = ['sh', 'update_launcher.sh']
        subprocess.Popen(cmd)
        exit()
    elif command == 'align':
        print('Align mode on')
        cmd = 'raspistill -t 10000 -o cam.jpg'
        subprocess.call(cmd, shell = True)
    else:
        print('Shooting photo')
        cmd = 'raspistill -o cam.jpg'
        subprocess.call(cmd, shell=True)
        try:
            with open('cam.jpg', 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read())
                send_photo(command_computer_ip, 5000+rasp_pi_id, encoded_image)
            with open('log.txt', 'a') as logfile:
                logfile.write('Took photo sucessfully at {0}, which was sent to {1} \n'.format(time.strftime('%a, %d %b %Y %H:%M:%S'), command_computer_ip))
        except Exception as e:
            with open('log.txt', 'a') as logfile:
                logfile.write('Exception occured at {0}: {1} \n'.format(time.strftime('%a, %d %b %Y %H:%M:%S'), e))










