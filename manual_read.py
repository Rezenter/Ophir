import sensor

test = sensor.Sensor()
if test.connect():
    if test.arm():
        data = test.disarm()
        if len(data) > 0 and len(data[0]) > 0:  # if any data available, print the first one from the batch
            print('Reading = {0}, TimeStamp = {1}, Status = {2} '.format(data[0][0], data[1][0], data[2][0]))
        else:
            print('no data! ')
        print('OK')