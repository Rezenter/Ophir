import sensor
import time

test = sensor.Sensor()
if test.connect():
    if test.arm():
        time.sleep(30)
        energy, time = test.disarm()
        with open('dump.txt', 'w') as dump:
            for i in range(len(energy)):
                dump.write('%.3f, %.2e\n' % (time[i], energy[i]))
        print('File written')
else:
    print('No connection!')