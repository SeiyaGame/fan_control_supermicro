import concurrent.futures
import json
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

    def get_disk_list(self, exclude_name=None, exclude_none_hdd=False):
        """
        Get a list of disk names, excluding those matching a regular expression pattern.

        :param exclude_name:
            A regular expression pattern to define exclusion criteria based on name
            For example: '^(nvme*|sdi)' it ignore /dev/sdi and all /dev/nvme*

        :param exclude_none_hdd:
            Is boolean, so can be set to True or False and exclude all SSD and NVME from the list

        :return:
            A list of disk names that do not match the exclusion pattern.
        """

        command = "lsblk -d -o name,rota --json"
        disk_list_output = self.run_command(command)

        # Parse the JSON output
        disk_data = json.loads(disk_list_output)

        # Initialize the list of disk names
        disk_names = []

        # Iterate over each block device
        for device in disk_data["blockdevices"]:
            # Apply the exclusion criteria based on the name
            if exclude_name and re.match(exclude_name, device["name"]):
                continue

            # Apply the exclusion criteria based on the rotation (SSD and NVME)
            if exclude_none_hdd and not device["rota"]:
                continue

            # Add the disk name to the list if it passes the filters
            disk_names.append(device["name"])

        return disk_names

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

    def get_disk_info(self, exclude_name=None, exclude_none_hdd=False):
        disk_names = self.get_disk_list(exclude_name, exclude_none_hdd)

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
