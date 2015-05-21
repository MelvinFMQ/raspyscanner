__author__ = 'melvinfoo'
#script to control all the raspberry pis.
#runs on python 2.7

import socket,subprocess, time, os, os.path


#setup
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5000
NO_OF_PI = 16

# Get current computer's IP address
command_computer_ip = socket.gethostbyname(socket.gethostname())
# Create the socket
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Make the socket multicast-aware, and set TTL (time to live).
broadcast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)


def print_opt():
    print('')
    print('0. Start new scan')
    print('95. Align mode')
    print('96. Update Raspberry Pi Server software')
    print('97. Shutdown')
    print('98. Reboot')
    print('99. Quit')
    print('')

#function to open the sockets for the raspberry pis to upload the image.
#1 socket for 1 raspberry pi
def start_upload_sockets(name, scan):
    if scan:
        script = 'image_receiver.py'
    else:
        script = 'server_updater_sender.py'
    for i in range(1, NO_OF_PI+1):
        #name and id to open the sockets.
        subprocess.Popen(['python', script, '{0}'.format(name), '{0}'.format(i)])
    time.sleep(2)  # takes awhile to open all the ports



def count_files(name_):
    return len([name for name in os.listdir('scans/{0}/'.format(name_))])


def send_command(command):
    broadcast_socket.sendto(command, (MCAST_GRP, MCAST_PORT))


def start_scan():
    #name of the scan
    name = raw_input('Please enter name of scan: ')
    command = 'shoot'
    #create the file
    subprocess.call('mkdir scans/{0}'.format(name), shell=True)
    #open the sockets for raspberry pi to connect
    start_upload_sockets(name, True)
    print('Sending command to take photo')
    #finnally send the command
    send_command(command)
    while count_files(name) != NO_OF_PI:
        pass


def shut_down():
    print('Shutting down')
    command = 'shutdown'
    send_command(command)


def reboot():
    print('Rebooting')
    command = 'reboot'
    send_command(command)


def quit_():
    quit = raw_input('Are you sure you want to quit? y/n :')
    if quit == 'y':
        broadcast_socket.close()
        print('Bye')
        exit()
    else:
        pass


def update():
    command = 'update'
    file_location = raw_input('Location/name of new/updated file: ')
    if os.path.isfile(file_location):
        send_command(command)
        time.sleep(2)
        start_upload_sockets(file_location, False)
    else:
        print('No such file.')

def align():
    command = 'align'
    send_command(command)
    time.sleep(10)
    
options = {0: start_scan, 95: align, 96: update, 97: shut_down, 98: reboot, 99: quit_}


def main():
    while True:
        print_opt()
        try:
            user_input = raw_input('Select your choice: ')
            if user_input == '':
                print('Options cannot be empty')
            elif user_input.isalpha():
                print('Please input only numbers, no letters')
            else:
                options[int(user_input)]()
        except KeyError:
            print('No such option')


if __name__ == '__main__':
    main()
