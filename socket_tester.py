import socket
from time import sleep

HOST = '192.168.10.55'
PORT = 8888

connected = False
ready: bool = False
armed: bool = False
fired: bool = False

while 1:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.settimeout(0.1)
        try:
            if ready and not fired:
                #s.sendall('arm 0 11111'.encode('utf-8'))
                s.sendall(('arm %d %d' % (False, 11111)).encode('utf-8'))
                fired = True
            elif armed:
                sleep(10)
                s.sendall(b'disarm')
                armed = False
            elif connected:
                s.sendall(b'status')
                data = s.recv(64)
                if len(data) > 0:
                    status = int.from_bytes(bytes=data, byteorder='big', signed=True)
                    if status == -1:
                        connected = False
                        ready = False
                        armed = False
                    elif status == 0:
                        connected = True
                        ready = True
                        armed = False
                    elif status == 1:
                        connected = True
                        ready = False
                        armed = True
                    elif status == 2:
                        connected = True
                        ready = False
                        armed = False
                        print('sensor dead time')
                    print('Status', status)
            else:
                print('Connecting...')
                s.sendall(b'connect')
                sleep(1)
                connected = True

        except socket.timeout:
            print('timeout')
        #s.close()
    sleep(0.5)
print('exit')
