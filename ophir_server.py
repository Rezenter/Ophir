import socket
from sensor import Sensor
import msgpack

HOST: str = '192.168.10.55'
PORT: int = 8888
PACKET_SIZE: int = 64
db_path: str = '//192.168.10.41/d/data/db/'

sensor: Sensor = Sensor()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(1)
    s.bind((HOST, PORT))
    s.listen()
    print('Ophir server started. Waiting for commands...')
    while True:
        try:
            try:
                conn, addr = s.accept()
                with conn:
                    #print('connected')
                    data = conn.recv(PACKET_SIZE)
                    if data == b'status':
                        conn.sendall(sensor.status().to_bytes(length=1, byteorder='big', signed=True))
                    elif data == b'connect':
                        sensor.connect()
                    elif len(data) > 3:
                        if data[:3] == b'arm':
                            cmd = data[4:].decode('utf-8').split()
                            if len(cmd) == 2:
                                is_plasma: bool = int(cmd[0]) != 0
                                shotn: int = int(cmd[1])
                                sensor.arm(is_plasma=is_plasma, shotn=shotn)
                        elif data == b'disarm':
                            #print('disarming')
                            meas = sensor.disarm()
                            path = db_path
                            if sensor.is_plasma:
                                path += 'plasma/'
                            else:
                                path += 'debug/'
                            path += 'ophir/%05d.msgpk' % sensor.shotn
                            with open(path, 'wb') as file:
                                if len(meas) > 0:
                                    msgpack.dump(meas, file)
                            print('Ophir got %d shots' % len(meas))
                    else:
                        conn.sendall(b'Wrong CMD')
                    conn.close()
            except TimeoutError:
                pass
        except KeyboardInterrupt:
            #s.close()  # redundant due to "with"
            sensor.__del__()
            break

print('server exit')
