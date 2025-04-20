import argparse
import logging
import os.path
import pathlib
import traceback
import time
import requests
from tools.ipmitool import Ipmitool
from tools.disk_monitor import DiskMonitor
from tools.cpu_monitor import CPUMonitor
from tools.config_validator import ConfigValidator
from datetime import datetime, timedelta
from logger import Logger

BASE_DIR = pathlib.Path(__file__).parent
LOG_DIR = os.path.join(BASE_DIR, "logs")
config_file = os.path.join(BASE_DIR, "config.py")

if os.path.exists(config_file):
    from config import *
else:
    print("No configuration file exists, copy the existing file 'config.sample.py' "
          "to 'config.py' and change the values in this file!")
    exit(1)

logger = logging.getLogger("fan_control")


def send_webhook_notification(message):
    try:
        response = requests.post(WEBHOOK_URL, json={"content": message})
        response.raise_for_status()
        logger.info("Notification sent successfully.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send notification: {e}")


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

        self.highest_disk_temperature = -1
        self.cpu_temperature = -1

        self.ipmi_fan_speed = list()
        self.disk_info = list()

        self.current_fan_speed = dict()
        self.notification_sent = False
        self.last_notification_time = datetime.min  # Initialisation

    def check_disk_temperature_and_notify(self):
        now = datetime.now()
        time_since_last_notification = now - self.last_notification_time

        disk_reach_high_temp = [disk for disk in self.disk_info if disk[1] >= NOTIFICATION_DISK_REACH_HIGH_TEMPERATURE]
        disk_reach_low_temp = [disk for disk in self.disk_info if disk[1] <= NOTIFICATION_DISK_REACH_LOW_TEMPERATURE]
        disk_reach_temp = disk_reach_high_temp + disk_reach_low_temp

        notification_disk_message = f"⚠️WARNING⚠️ | {len(disk_reach_temp)} disk reach temperature limit (↑{NOTIFICATION_DISK_REACH_HIGH_TEMPERATURE}°C | ↓{NOTIFICATION_DISK_REACH_LOW_TEMPERATURE}°C) !"
        notification_disk_message += "\n"

        for i in range(0, len(disk_reach_temp), 2):
            disk_info_str = " | ".join(
                "{:^7} - {}°C - S/N: {:<12}".format(disk[0], disk[1], disk[2])
                for disk in disk_reach_temp[i:i + 2]
            )
            notification_disk_message += disk_info_str + "\n"

        if disk_reach_temp:
            if not self.notification_sent or time_since_last_notification > timedelta(minutes=NOTIFICATION_SEND_EVERY_MINUTE):
                send_webhook_notification(notification_disk_message)
                self.notification_sent = True
                self.last_notification_time = now
        elif self.notification_sent and time_since_last_notification > timedelta(minutes=NOTIFICATION_SEND_EVERY_MINUTE):
            self.notification_sent = False  # Reset notification status

    def set_fan_speed_by_temperature(self, zone, temperature, fan_speed_grid):
        current_temp_range, current_fan_speed = self.current_fan_speed.get(zone, ((-1, -1), None))

        def update_fan_speed(temp_grid, fan_speed_percent_grid):
            if current_fan_speed is None or current_fan_speed != fan_speed_percent_grid:
                self.current_fan_speed[zone] = temp_grid, fan_speed_percent_grid

                fan_speed_status = f"Set fan speed for the {zone} zone to {fan_speed_percent_grid}% ({hex(fan_speed_percent_grid)}) "

                if isinstance(temp_grid, int):
                    label = "Temperature reach" if temp_grid == temperature else "Fallback to"
                    fan_speed_status += f"({label}: {temp_grid})"

                elif isinstance(temp_grid, tuple):
                    in_range = temp_grid[0] <= temperature <= temp_grid[1]
                    label = "Temperature range" if in_range else "Fallback range"
                    fan_speed_status += f"({label}: {temp_grid[0]} → {temp_grid[1]})"

                logger.info(fan_speed_status)

                if not self.dry_run:
                    if zone == 'cpu':
                        self.ipmitool.set_fan_speed(0, fan_speed_percent_grid)
                    elif zone == 'peripheral':
                        self.ipmitool.set_fan_speed(1, fan_speed_percent_grid)
                    else:
                        logger.warning(f"The zone {zone} doesn't exist or is not implemented yet!")

        # Fist Attempt
        for temp_grid, fan_speed_percent_grid in fan_speed_grid.items():
            if isinstance(temp_grid, tuple) and temp_grid[0] <= temperature <= temp_grid[1]:
                update_fan_speed(temp_grid, fan_speed_percent_grid) ; return
            elif isinstance(temp_grid, int) and temperature == temp_grid:
                update_fan_speed(temp_grid, fan_speed_percent_grid) ; return

        # Fallback to Lower value
        last_temp, last_fan_speed = None, None
        for temp_grid, fan_speed_percent_grid in fan_speed_grid.items():
            if isinstance(temp_grid, tuple) and temp_grid[1] < temperature:
                last_temp, last_fan_speed = temp_grid, fan_speed_percent_grid
            elif isinstance(temp_grid, int) and temp_grid < temperature:
                last_temp, last_fan_speed = temp_grid, fan_speed_percent_grid

        if last_temp and last_fan_speed:
            update_fan_speed(last_temp, last_fan_speed) ; return

        # Unexpected value, set fan speed to the maximum
        logger.warning(f"No fallback rules found for {zone} at {temperature}°C")
        update_fan_speed(temperature, 100)

    def set_peripheral_fan_speed_by_temperature(self, temperature):
        self.set_fan_speed_by_temperature('peripheral', temperature, self.disk_fan_speed_grid)

    def set_cpu_fan_speed_by_temperature(self, temperature):
        self.set_fan_speed_by_temperature('cpu', temperature, self.cpu_fan_speed_grid)

    def set_dry_run(self, dry_run):
        self.dry_run = dry_run

    def get_highest_disk_temperature(self):
        return max(self.disk_info, key=lambda x: x[1])

    def print_info(self):

        peripheral_temp, peripheral_fan_speed = self.current_fan_speed['peripheral']
        cpu_temp, cpu_fan_speed = self.current_fan_speed['cpu']

        text_to_print = "-----------\n"

        if isinstance(peripheral_temp, tuple):
            text_to_print += f"HDD ↑ {self.highest_disk_temperature}°C ({peripheral_temp[0]} → {peripheral_temp[1]}) {peripheral_fan_speed}% 💨 | "
        else:
            text_to_print += f"HDD ↑ {self.highest_disk_temperature}°C {peripheral_fan_speed}% 💨 | "

        if isinstance(cpu_temp, tuple):
            text_to_print += f"CPU {self.cpu_temperature}°C ({cpu_temp[0]} → {cpu_temp[1]}) {cpu_fan_speed}% 💨 \n\n"
        else:
            text_to_print += f"CPU {self.cpu_temperature}°C {cpu_fan_speed}% 💨 \n\n"

        fan_speeds_str = " | ".join([f"{fan[0]}({fan[1]} RPM)" if fan[1] != "N/A" else f"{fan[0]}" for fan in self.ipmi_fan_speed])
        text_to_print += fan_speeds_str + "\n\n"

        for i in range(0, len(self.disk_info), 3):
            disk_info_str = " | ".join(
                "{:^7} - {}°C - S/N: {:<12}".format(disk[0], disk[1], disk[2])
                for disk in self.disk_info[i:i + 3]
            )
            text_to_print += disk_info_str + "\n"

        logger.info(text_to_print)

    def loop(self):

        try:
            logger.info("Fan mode set to FULL")
            if not self.dry_run:
                self.ipmitool.set_fan_mode("full")

            while True:

                # Get current fan speeds
                self.ipmi_fan_speed = self.ipmitool.get_fan_speed_bis()

                # Get disk information
                self.disk_info = self.disk_monitor.get_disk_info(exclude_none_hdd=True)

                # Get the highest disk temperature
                self.highest_disk_temperature = self.get_highest_disk_temperature()[1]

                # Get CPU temperature
                self.cpu_temperature = self.cpu_monitor.get_cpu_temperature()

                # Set FAN speed in function of disk temperature
                self.set_peripheral_fan_speed_by_temperature(self.highest_disk_temperature)

                # Set FAN speed in function of cpu temperature
                self.set_cpu_fan_speed_by_temperature(self.cpu_temperature)

                # Check if the disk temperature exceeds the threshold and send a notification if necessary
                self.check_disk_temperature_and_notify()

                self.print_info()

                if self.dry_run:
                    logger.info("Dry Run Mode - No changes made.\n")

                time.sleep(self.loop_sleep_time)

        except KeyboardInterrupt:
            return

        except Exception:
            logger.error(traceback.format_exc())
            self.ipmitool.set_fan_mode("standard")


def parser_setup():
    parser = argparse.ArgumentParser(description='Control fan speed via IPMI of Supermicro motherboard')
    parser.add_argument('-d', '--dry_run', action='store_true', help='No changes made, only to visualised')
    parser.add_argument('--no_console_log_stream', action='store_true', default=False, help='Disable Stream log in console')
    parser.add_argument('--webhook_url', type=str, default=None, help='Send message to a webhook url')
    parser.add_argument('--only_alert', action='store_true', default=True, help='Send only alert message to the webhook url')

    return parser.parse_args()


def main():
    try:
        args = parser_setup()
        dry_run = args.dry_run
        webhook_url = args.webhook_url or WEBHOOK_URL
        only_alert = args.only_alert
        no_console_log_stream = args.no_console_log_stream

        ConfigValidator().validate()

        log_file = os.path.join(LOG_DIR, 'fan_control.log')
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        if only_alert:
            logger = Logger("fan_control", "INFO", log_file=log_file)
        else:
            logger = Logger("fan_control", "INFO", webhook_url=webhook_url, log_file=log_file)

        logger.setup()

        if not no_console_log_stream:
            logger.enable_stream_console()

        disk_monitor = DiskMonitor()
        ipmitool = Ipmitool()
        cpu_monitor = CPUMonitor()

        case_fan_controller = CaseFanController(ipmitool, disk_monitor, cpu_monitor,
                                                DISK_FAN_SPEED_GRID, CPU_FAN_SPEED_GRID)

        case_fan_controller.set_dry_run(dry_run)

        print("Start of the service")
        case_fan_controller.loop()
        print("End of the service")

    except Exception as e:
        print(f"An unknown error occurred : {e}")
        print(traceback.format_exc())
        exit(1)


if __name__ == "__main__":
    main()
