import re
import psutil

RE_CPU_MODEL = re.compile(r'^model name\s*:\s*(.*)', flags=re.M)
RE_CPU_VENDOR = re.compile(r'^vendor_id\s*:\s*(.*)', flags=re.M)


class CPUMonitor:

    def __init__(self):
        self.vendor = self.get_cpu_vendor()
        self.cpu_model = self.get_cpu_model_name()
        self.sensor_module = "coretemp" if "INTEL" in self.vendor else "k10temp"

    @staticmethod
    def get_cpu_model_name():
        with open('/proc/cpuinfo', 'r') as f:
            model = RE_CPU_MODEL.search(f.read())
            return model.group(1) if model else None

    @staticmethod
    def get_cpu_vendor():
        with open('/proc/cpuinfo', 'r') as f:
            vendor_name = RE_CPU_VENDOR.search(f.read())
            vendor_name = vendor_name.group(1) if vendor_name else None

        if "amd" in vendor_name.casefold():
            return "AMD"
        elif "intel" in vendor_name.casefold():
            return "INTEL"

        return vendor_name

    def get_cpu_temperature(self):
        temperature_data = psutil.sensors_temperatures()
        if temperature_data:
            for sensor_name, sensor_info in temperature_data.items():
                if sensor_name.startswith(self.sensor_module):
                    for temp_info in sensor_info:
                        if temp_info.label.startswith(("Tctl", "Package id")):
                            return int(float(temp_info.current))
        return -1
