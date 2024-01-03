import concurrent.futures
import logging
import os
import re
import subprocess

logger = logging.getLogger("fan_control")


class DiskMonitor:

    def __init__(self):
        pass

    @staticmethod
    def run_command(command):
        try:
            return subprocess.check_output(command, shell=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing command: {command}")
            logger.error(f"Error message: {e}")
            return None

    def get_disk_list(self, exclude=None):
        """
        Get a list of disk names, excluding those matching a regular expression pattern.

        :param exclude:
            A regular expression pattern to define exclusion criteria.
            For example, to exclude all 'nvme' disks and only include 'sdi', use: '^(nvme|sdi)'.
        :return:
            A list of disk names that do not match the exclusion pattern.
        """

        command = "lsblk -d -o NAME"
        command += f"| grep -vE {exclude}" if exclude else ''

        disk_list_output = self.run_command(command)
        if disk_list_output:
            return disk_list_output.strip().split('\n')[1:]  # Exclude the header line
        else:
            return []

    def get_disk_smartctl(self, disk_name):
        command = f"smartctl -iA {os.path.join('/dev', disk_name)}"
        smartctl_output = self.run_command(command)
        return smartctl_output if smartctl_output else None

    @staticmethod
    def get_disk_temperature(smartctl_output):
        try:
            # HDD, SSD
            disk_temp = re.search(r'.*Temperature_Celsius.*', smartctl_output)[0]
            return int(disk_temp.split()[9])
        except TypeError:
            pass

        try:
            # NVME
            disk_temp = re.search(r'Temperature:.*', smartctl_output)[0]
            return int(disk_temp.split()[1])
        except TypeError:
            pass

        return -1

    @staticmethod
    def get_disk_serial_number(smartctl_output):
        serial_number_match = re.search(r'Serial Number:\s*(\S+)', smartctl_output)
        if serial_number_match:
            return serial_number_match.group(1)
        else:
            return 'UNDEFINED'

    def get_disk_info(self, exclude=None):
        disk_names = self.get_disk_list(exclude)

        def fetch_disk_info(disk_name):
            smartctl_output = self.get_disk_smartctl(disk_name)
            if smartctl_output:
                temperature = self.get_disk_temperature(smartctl_output)
                serial_number = self.get_disk_serial_number(smartctl_output)
                return disk_name, temperature, serial_number
            else:
                return None

        # Utilisez ThreadPoolExecutor pour exécuter les appels get_disk_smartctl en parallèle
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(fetch_disk_info, disk_names))

        # Filtrer les résultats None (en cas d'erreur)
        disk_info = [result for result in results if result is not None]

        return disk_info


if __name__ == "__main__":

    import time

    disk_monitor = DiskMonitor()

    while True:
        try:
            start_time = time.time()  # Enregistrez le temps de début
            print(disk_monitor.get_disk_info())
            end_time = time.time()  # Enregistrez le temps de fin
            elapsed_time = end_time - start_time  # Calculez le temps écoulé
            print(f"Temps écoulé pour get_disk_info(): {elapsed_time} secondes")
            time.sleep(1)
        except KeyboardInterrupt:
            break
