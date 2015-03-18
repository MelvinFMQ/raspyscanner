__author__ = 'melvinfoo'
#script to open sockets for raspberry pis to upload images
#recontructs images and downloads them into selected folder

import socket
import base64
import subprocess


def get_ip():
    command = ['ip', 'addr', 'show', 'eth0']
    return_text = subprocess.check_output(command)
    start_index = return_text.find('inet') + 5
    end_index = return_text[start_index:].find('/') + start_index
    ip = return_text[start_index: end_index].replace(' ', '') 
    return ip

host = get_ip()
rasp_pi_id = host.split('.')[3]
port = 5000

print('Launched socket {0} on IP: {1}, Port: {2}. Listening for update'.format(rasp_pi_id, host, port))
update_listener = socket.socket()  # use which protocols
update_listener.bind((host, port))

update_listener.listen(5)
connection, addr = update_listener.accept()
print('Got a connection from command computer of address{0}'.format(str(addr)))
message = ''
while True:
    data = connection.recv(1024)
    message = message + data  # contructing the string
    if not data:
        break

print('Downloaded update from command computer')
file_name, encoded_data = message.split('|')

updated_file = open(file_name, 'w+')
recovered_file = base64.decodestring(encoded_data)
updated_file.write(recovered_file)
updated_file.close()
print('{0} updated/added'.format(file_name))
connection.close()
update_listener.close()
print('launching normal server again.')
cmd = ['sh', 'launcher.sh']
subprocess.Popen(cmd)
print('Exiting')
exit()
