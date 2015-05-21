__author__ = 'melvinfoo'
#script to open sockets for raspberry pis to upload images
#recontructs images and downloads them into selected folder

import socket, sys, base64

command_computer_ip = socket.gethostbyname(socket.gethostname())
host = command_computer_ip
name, rasp_pi_id = sys.argv[1], sys.argv[2]
port = 5000 + int(rasp_pi_id)


print('Launching socket {0} on IP: {1}, Port: {2}. Listening for photo connection'.format(rasp_pi_id, command_computer_ip, port))
try:
    image_listener = socket.socket()  # use which protocols
    image_listener.bind((host, port))
except socket.error:
    print('Socket {0} has already been launched.'.format(rasp_pi_id))

#argument specifies how many connections should be queued.
image_listener.listen(5)
#connection is another socket object used to send and receive data
connection, addr = image_listener.accept()
print('Got a connection from {0}, Raspberry Pi ID of: {1}'.format(str(addr), rasp_pi_id))
encoded_string = ''
while True:
    #chunks are split up to 1024 bytes
    data = connection.recv(1024)
    encoded_string = encoded_string + data  # recontructing the string
    if not data:
        break
#save the image
print('Downloaded image from Raspberry Pi {0}'.format(rasp_pi_id))
image_file = open('scans/{0}/{1}.jpg'.format(name, rasp_pi_id), 'w+')
recovered_image = base64.decodestring(encoded_string)
image_file.write(recovered_image)
image_file.close()
connection.close()
image_listener.close()
