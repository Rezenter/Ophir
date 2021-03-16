import win32com.client


class Sensor:
    measurement_range = 4

    def __init__(self):
        self.OphirCOM = None
        self.DeviceHandle = None
        self.connected = False
        print('Init OK')

    def connect(self):
        self.connected = False
        self.OphirCOM = win32com.client.Dispatch("OphirLMMeasurement.CoLMMeasurement")
        # Stop & Close all devices
        self.OphirCOM.StopAllStreams()
        self. OphirCOM.CloseAll()
        # Scan for connected Devices
        DeviceList = self.OphirCOM.ScanUSB()
        if len(DeviceList) == 0:
            return
        Device = DeviceList[0]
        self.DeviceHandle = self.OphirCOM.OpenUSBDevice(Device)  # open first device
        exists = self.OphirCOM.IsSensorExists(self.DeviceHandle, 0)
        if exists:
            self.OphirCOM.SetRange(self.DeviceHandle, 0, self.measurement_range)
            self.connected = True
            print('connect OK')
            return

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
                return data
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
