import clr
import sys
# from os.path import abspath as os_abspath

class HWMonitor:
    def __init__(self):
        self.hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD']

    @classmethod
    def initialize_openhardwaremonitor(cls):
        sys.path.append(r'OpenHardwareMonitor\OpenHardwareMonitorLib.dll')
        clr.AddReference('OpenHardwareMonitorLib')

        from OpenHardwareMonitor import Hardware

        handle = Hardware.Computer()
        handle.MainboardEnabled = True
        handle.CPUEnabled = True
        handle.RAMEnabled = True
        handle.GPUEnabled = True
        handle.HDDEnabled = True
        handle.Open()
        return handle

    def fetch_stats(self, handle):
        for i in handle.Hardware:
            i.Update()
            for sensor in i.Sensors:
                self.parse_sensor(sensor)
            for j in i.SubHardware:
                j.Update()
                for subsensor in j.Sensors:
                    self.parse_sensor(subsensor)

    def parse_sensor(self, sensor):
        if sensor.Value:
            if str(sensor.SensorType) == 'Temperature':
                result = u'{} {} Temperature Sensor #{} {} - {}\u00B0C' \
                    .format(self.hwtypes[sensor.Hardware.HardwareType],
                            sensor.Hardware.Name, sensor.Index,
                            sensor.Name, sensor.Value
                            )
                print(result)


    def lol(self):
        sys.path.append(r'../OpenHardwareMonitorLib.dll')
        # full_path = os_abspath(r'OpenHardwareMonitor/OpenHardwareMonitorLib.dll')
        # print(full_path)

        clr.AddReference("OpenHardwareMonitorLib")
        from OpenHardwareMonitor.Hardware import Computer
        c = Computer()
        c.CPUEnabled = True  # get the Info about CPU
        c.GPUEnabled = True  # get the Info about GPU
        c.Open()
        while True:
            for a in range(0, len(c.Hardware[0].Sensors)):
                # print(c.Hardware[0].Sensors[a].Identifier)
                if "/temperature" in str(c.Hardware[0].Sensors[a].Identifier):
                    print(c.Hardware[0].Sensors[a].get_Value())
                    c.Hardware[0].Update()


