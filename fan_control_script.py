import argparse
import logging
import time
from tools.ipmitool import Ipmitool
from tools.disk_monitor import DiskMonitor
from tools.cpu_monitor import CPUMonitor
from logger import Logger
from config import *

logger = logging.getLogger("fan_control")


class CaseFanController:
    def __init__(self, ipmitool, disk_monitor, cpu_monitor,
                 disk_fan_speed_grid, cpu_fan_speed_grid, loop_sleep_time=30):
        self.ipmitool = ipmitool
        self.disk_monitor = disk_monitor
        self.cpu_monitor = cpu_monitor

        self.disk_fan_speed_grid = disk_fan_speed_grid
        self.cpu_fan_speed_grid = cpu_fan_speed_grid

        self.dry_run = False

        self.loop_sleep_time = loop_sleep_time

        self.highest_hdd_temperature = -1
        self.cpu_temperature = -1

        self.ipmi_fan_speed = list()
        self.disk_info = list()

        self.current_fan_speed = dict()

    def set_fan_speed_by_temperature(self, zone, temperature, fan_speed_grid):
        current_temp_range, current_fan_speed = self.current_fan_speed.get(zone, ((-1, -1), None))

        for temp_range, fan_speed_percent in fan_speed_grid.items():
            if temp_range[0] <= temperature <= temp_range[1]:

                if current_fan_speed is None or current_fan_speed != fan_speed_percent:
                    self.current_fan_speed[zone] = temp_range, fan_speed_percent

                    logger.info(f"Set fan speed for the {zone} zone to {fan_speed_percent}% ({hex(fan_speed_percent)}) "
                                f"(Temperature range: {temp_range[0]} → {temp_range[1]})")

                    if not self.dry_run:
                        if zone == 'cpu':
                            self.ipmitool.set_fan_speed(0, fan_speed_percent)
                        elif zone == 'peripheral':
                            self.ipmitool.set_fan_speed(1, fan_speed_percent)
                        else:
                            logger.warning(f"The zone {zone} doesn't exist or implemented yet !")

                return

    def set_peripheral_fan_speed_by_temperature(self, temperature):
        self.set_fan_speed_by_temperature('peripheral', temperature, self.disk_fan_speed_grid)

    def set_cpu_fan_speed_by_temperature(self, temperature):
        self.set_fan_speed_by_temperature('cpu', temperature, self.cpu_fan_speed_grid)

    def set_dry_run(self, dry_run):
        self.dry_run = dry_run

    def get_highest_hdd_temperature(self):
        return max(self.disk_info, key=lambda x: x[1])[1]

    def print_info(self):

        peripheral_temp_range, peripheral_fan_speed = self.current_fan_speed['peripheral']
        cpu_temp_range, cpu_fan_speed = self.current_fan_speed['cpu']

        text_to_print = (
            f"-----------\n"
            f"HDD ↑ {self.highest_hdd_temperature}°C ({peripheral_temp_range[0]} → {peripheral_temp_range[1]}) {peripheral_fan_speed}% 💨 | "
            f"CPU {self.cpu_temperature}°C ({cpu_temp_range[0]} → {cpu_temp_range[1]}) {cpu_fan_speed}% 💨 \n\n"
        )

        fan_speeds_str = " | ".join([f"{fan[0]}({fan[1]} RPM)" if fan[1] != "N/A" else f"{fan[0]}" for fan in self.ipmi_fan_speed])
        text_to_print += fan_speeds_str + "\n\n"

        for i in range(0, len(self.disk_info), 3):
            group = self.disk_info[i:i + 3]
            disk_info_str = ""
            for disk in group:
                formatted_info = "{:^7} - {}°C - S/N: {:<12}".format(disk[0], disk[1], disk[2])
                disk_info_str += formatted_info + " | "
            text_to_print += disk_info_str[:-3] + "\n"

        logger.info(text_to_print)

    def loop(self):

        logger.info("Fan mode set to FULL")
        if not self.dry_run:
            self.ipmitool.set_fan_mode("full")

        try:
            while True:

                # Get current fan speeds
                self.ipmi_fan_speed = self.ipmitool.get_fan_speed_bis()

                # Get disk information
                self.disk_info = self.disk_monitor.get_disk_info(exclude="^nvme")

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
                    logger.info("Dry Run Mode - No changes made.\n")

                time.sleep(self.loop_sleep_time)

        except KeyboardInterrupt:
            return


def parser_setup():
    parser = argparse.ArgumentParser(description='Control fan speed via IPMI of Supermicro motherboard')
    parser.add_argument('-d', '--dry_run', action='store_true', help='No changes made, only to visualised')
    parser.add_argument('--no_console_log_stream', action='store_true', default=True, help='Disable Stream log in console')
    parser.add_argument('--discord_webhook', type=str, default=None, help='Send all logs also to webhook discord')

    return parser.parse_args()


def main():
    try:
        disk_monitor = DiskMonitor()
        ipmitool = Ipmitool()
        cpu_monitor = CPUMonitor()

        args = parser_setup()
        dry_run = args.dry_run
        discord_webhook = args.discord_webhook
        no_console_log_stream = args.no_console_log_stream

        logger = Logger("fan_control", "INFO", webhook_url=discord_webhook).setup()
        if not no_console_log_stream:
            logger.enable_stream_console()

        case_fan_controller = CaseFanController(ipmitool, disk_monitor, cpu_monitor,
                                                disk_fan_speed_grid, cpu_fan_speed_grid)

        case_fan_controller.set_dry_run(dry_run)

        print("Start of the service")
        case_fan_controller.loop()
        print("End of the service")

    except Exception as e:
        print(f"An unknown error occurred : {e}")
        exit(1)


if __name__ == "__main__":
    main()
