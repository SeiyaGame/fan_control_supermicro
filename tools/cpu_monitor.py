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
        temps = psutil.sensors_temperatures().get(self.sensor_module, [])

        # No CPU temp found
        if not temps:
            return -1

        # Tctl or Package id (AMD / Intel)
        for sensor in temps:
            if sensor.label.startswith(("Tctl", "Package id")):
                return int(sensor.current)

        # Sum of all cores in case Tctl or Package id not exist (AMD / Intel)
        core_temps = [s.current for s in temps if s.label.startswith(("Core", "Tccd"))]
        if core_temps:
            return int(sum(core_temps) / len(core_temps))

        # Nothing match but temperature found
        return -1
