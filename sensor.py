import win32com.client


class Sensor:
    diffuser = 1  # diffuser (0, ('N/A',))
    measurement_mode = 1  # MeasMode (1, ('Power', 'Energy'))
    pulse_length = 0 # PulseLengths (0, ('30uS', '1.0mS'))
    measurement_range = 2  #Ranges (2, ('10.0J', '2.00J', '200mJ', '20.0mJ', '2.00mJ', '200uJ'))
    wavelength = 3  #Wavelengths (3, (' 193', ' 248', ' 532', '1064', '2100', '2940'))
    def __init__(self):
        self.OphirCOM = None
        self.DeviceHandle = None
        self.connected = False

    def connect(self):
        self.connected = False
        self.OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
        # Stop & Close all devices
        self.OphirCOM.StopAllStreams()
        self.OphirCOM.CloseAll()
        # Scan for connected Devices
        DeviceList = self.OphirCOM.ScanUSB()
        if len(DeviceList) == 0:
            return False
        Device = DeviceList[0]
        self.DeviceHandle = self.OphirCOM.OpenUSBDevice(Device)  # open first device
        exists = self.OphirCOM.IsSensorExists(self.DeviceHandle, 0)
        if exists:
            print('diffuser', self.OphirCOM.GetDiffuser(self.DeviceHandle, 0))
            print('MeasMode', self.OphirCOM.GetMeasurementMode(self.DeviceHandle, 0))
            print('PulseLengths', self.OphirCOM.GetPulseLengths(self.DeviceHandle, 0))
            print('Ranges', self.OphirCOM.GetRanges(self.DeviceHandle, 0))
            print('Wavelengths', self.OphirCOM.GetWavelengths(self.DeviceHandle, 0))

            #self.OphirCOM.StopStream(self.DeviceHandle, 0)
            #self.OphirCOM.SetDiffuser(self.DeviceHandle, 0, self.diffuser)
            self.OphirCOM.SetMeasurementMode(self.DeviceHandle, 0, self.measurement_mode)
            self.OphirCOM.SetPulseLength(self.DeviceHandle, 0, self.pulse_length)
            self.OphirCOM.SetRange(self.DeviceHandle, 0, self.measurement_range)
            self.OphirCOM.SetWavelength(self.DeviceHandle, 0, self.wavelength)
            self.connected = True
            print('connect OK')
            return True

    def arm(self):
        if self.connected:
            exists = self.OphirCOM.IsSensorExists(self.DeviceHandle, 0)
            if exists:
                self.OphirCOM.StartStream(self.DeviceHandle, 0)  # start measuring
                return True
            print('Not exists!')
        else:
            print('Sensor is not connected!')
        return False

    def disarm(self):
        if self.connected:
            exists = self.OphirCOM.IsSensorExists(self.DeviceHandle, 0)
            if exists:
                data = self.OphirCOM.GetData(self.DeviceHandle, 0)
                self.OphirCOM.StopStream(self.DeviceHandle, 0)

                meas = []
                time = []
                for i in range(0, len(data[0]), 2):
                    meas.append(data[0][i])
                    time.append(data[1][i] - data[1][0])
                return meas, time
            print('Not exists!')
        else:
            print('Sensor is not connected!')
        return []

    def __del__(self):
        if self.OphirCOM is not None:
            self.OphirCOM.StopAllStreams()
            self.OphirCOM.CloseAll()
            self.OphirCOM = None
        print('destroyed')
