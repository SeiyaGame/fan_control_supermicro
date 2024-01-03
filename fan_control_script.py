import os
import time
from ipmitool import Ipmitool
from disk_monitor import DiskMonitor
from cpu_monitor import CPUMonitor

# Fan speed control grid based on hard drive temperatures
disk_fan_speed_grid = {
    (0, 27): 40,  # Temperature from 0°C to 30°C: 40%
    (28, 30): 50,  # Temperature from 28°C to 30°C: 50%
    (31, 34): 60,  # Temperature from 31°C to 34°C: 60%
    (35, 37): 70,  # Temperature from 35°C to 37°C: 70%
    (38, 40): 80,  # Temperature from 38°C to 40°C: 80%
    (41, 45): 90,  # Temperature from 41°C to 45°C: 90%
    (46, 60): 100,  # Temperature from 46°C to 650°C: 100%
}

# Fan speed control grid based on CPU temperatures
cpu_fan_speed_grid = {
    (0, 25): 30,  # Temperature from 0°C to 25°C: 30%
    (26, 34): 45,  # Temperature from 26°C to 34°C: 45%
    (35, 40): 55,  # Temperature from 35°C to 40°C: 55%
    (41, 50): 60,  # Temperature from 41°C to 50°C: 60%
    (51, 60): 70,  # Temperature from 51°C to 60°C: 70%
    (61, 80): 85,  # Temperature from 61°C to 80°C: 85%
    (81, 100): 100  # Temperature from 61°C to 100°C: 100%
}


# TODO: Create a web interface to display temperature data??
# TODO: Create a Prometheus exporter??
# TODO: This script only works on DEBIAN and TrueNAS SCALE

class CaseFanController:
    def __init__(self, ipmitool, disk_monitor, cpu_monitor,
                 disk_fan_speed_grid, cpu_fan_speed_grid , loop_sleep_time=30):
        self.ipmitool = ipmitool
        self.disk_monitor = disk_monitor
        self.cpu_monitor = cpu_monitor
        self.disk_fan_speed_grid = disk_fan_speed_grid
        self.cpu_fan_speed_grid = cpu_fan_speed_grid
        self.dry_run = False

        self.loop_sleep_time = loop_sleep_time

        self.highest_hdd_temperature = -1
        self.cpu_temperature = -1

        self.current_fan_speed = dict()

    def set_fan_speed_by_temperature(self, zone, temperature, fan_speed_grid):
        current_temp_range, current_fan_speed = self.current_fan_speed.get(zone, ((-1, -1), None))

        for temp_range, fan_speed_percent in fan_speed_grid.items():
            if temp_range[0] <= temperature <= temp_range[1]:

                if current_fan_speed is None or current_fan_speed != fan_speed_percent:
                    self.current_fan_speed[zone] = temp_range, fan_speed_percent

                    print(f"Set fan speed for the {zone} zone to {fan_speed_percent}% ({hex(fan_speed_percent)}) "
                          f"(Temperature range: {temp_range[0]} → {temp_range[1]})")

                    if not self.dry_run:
                        if zone == 'cpu':
                            self.ipmitool.set_fan_speed(0, fan_speed_percent)
                        elif zone == 'peripheral':
                            self.ipmitool.set_fan_speed(1, fan_speed_percent)
                        else:
                            print(f"The zone {zone} doesn't exist or implemented yet !")

                return

    def set_peripheral_fan_speed_by_temperature(self, temperature):
        self.set_fan_speed_by_temperature('peripheral', temperature, self.disk_fan_speed_grid)

    def set_cpu_fan_speed_by_temperature(self, temperature):
        self.set_fan_speed_by_temperature('cpu', temperature, self.cpu_fan_speed_grid)

    def set_dry_run(self, dry_run):
        self.dry_run = dry_run

    def get_highest_hdd_temperature(self):
        highest_temperature = -1

        disk_info = self.disk_monitor.get_disk_info(exclude="^nvme")

        for name, temperature, serial in disk_info:
            if temperature > highest_temperature:
                highest_temperature = temperature

        return highest_temperature

    def print_info(self):
        # Get current fan speeds
        fan_speeds = self.ipmitool.get_fan_speed_bis()

        # Get disk information
        disk_info = self.disk_monitor.get_disk_info()

        peripheral_temp_range, peripheral_fan_speed = self.current_fan_speed['peripheral']
        cpu_temp_range, cpu_fan_speed = self.current_fan_speed['cpu']

        text_to_print = (
            f"-----------\n"
            f"HDD ↑ {self.highest_hdd_temperature}°C ({peripheral_temp_range[0]} → {peripheral_temp_range[1]}) {peripheral_fan_speed}% 💨 | "
            f"CPU {self.cpu_temperature}°C ({cpu_temp_range[0]} → {cpu_temp_range[1]}) {cpu_fan_speed}% 💨 \n\n"
        )

        fan_speeds_str = " | ".join([f"{fan[0]}({fan[1]} RPM)" if fan[1] != "N/A" else f"{fan[0]}" for fan in fan_speeds])
        text_to_print += fan_speeds_str + "\n\n"

        for i in range(0, len(disk_info), 3):
            group = disk_info[i:i + 3]
            disk_info_str = ""
            for disk in group:
                formatted_info = "{:^7} - {}°C - S/N: {:<12}".format(disk[0], disk[1], disk[2])
                disk_info_str += formatted_info + " | "
            text_to_print += disk_info_str[:-3] + "\n"

        print(text_to_print)

    def loop(self):

        print("Fan mode set to FULL")
        if not self.dry_run:
            self.ipmitool.set_fan_mode("full")

        try:
            while True:

                # Get the highest HDD temperature
                self.highest_hdd_temperature = self.get_highest_hdd_temperature()

                # Get CPU temperature
                self.cpu_temperature = self.cpu_monitor.get_cpu_temperature()

                # Set FAN speed in function of hdd temperature
                self.set_peripheral_fan_speed_by_temperature(self.highest_hdd_temperature)

                # Set FAN speed in function of cpu temperature
                self.set_cpu_fan_speed_by_temperature(self.cpu_temperature)

                self.print_info()

                if self.dry_run:
                    print("Dry Run Mode - No changes made.\n")

                time.sleep(self.loop_sleep_time)
                os.system('cls' if os.name == 'nt' else 'clear')

        except KeyboardInterrupt:
            return


def main():
    try:
        disk_monitor = DiskMonitor()
        ipmitool = Ipmitool()
        cpu_monitor = CPUMonitor()

        case_fan_controller = CaseFanController(ipmitool, disk_monitor, cpu_monitor,
                                                disk_fan_speed_grid, cpu_fan_speed_grid)

        # case_fan_controller.set_dry_run(True)

        case_fan_controller.loop()

    except Exception as e:
        print(f"An unknown error occurred : {e}")


if __name__ == "__main__":
    main()
