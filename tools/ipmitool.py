import subprocess
import time


class Ipmitool:
    def __init__(self, path_exec="/usr/bin/ipmitool"):
        self.path_exec = path_exec

    def run_raw_ipmi_command(self, args, sleep_time=0):
        command = f"{self.path_exec} raw {args}"
        try:
            subprocess.check_output(command, shell=True, text=True)
            if sleep_time > 0:
                time.sleep(sleep_time)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}")
            print(f"Error message: {e}")
            return False

    def run_ipmi_command(self, args, sleep_time=0):
        command = f"{self.path_exec} {args}"
        try:
            output = subprocess.check_output(command, shell=True, text=True)
            if sleep_time > 0:
                time.sleep(sleep_time)
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}")
            print(f"Error message: {e}")
            return None

    def set_fan_mode(self, mode="full"):
        """
        :param mode:
            standard (0x00)
            full (0x01)
            optimal (0x02)
            heavy-IO (0x04)
        :return:
        """

        if mode == "full":
            convert_mode = "0x01"
        elif mode == "standard":
            convert_mode = "0x00"
        elif mode == "optimal":
            convert_mode = "0x02"
        elif mode == "heavy-IO":
            convert_mode = "0x04"
        else:
            print("Unsupported fan mode")
            return False

        command_args = f"0x30 0x45 0x01 {convert_mode}"
        return self.run_raw_ipmi_command(command_args, sleep_time=1)

    def set_fan_speed(self, zone, speed_percent):
        """
        :param zone:
            CPU zone default is 0x00
            Peripheral zone default is 0x01
        :param speed_percent:
            Value can be : 0 to 100
        :return:
        """
        if zone not in [0, 1]:
            print("Only CPU zone (0x00) and Peripheral zone (0x01) exist !")
            return False

        if speed_percent not in range(0, 100):
            print("Select a proper value between 0 and 100 percent !")
            return False

        command_args = f"0x30 0x70 0x66 0x01 {hex(zone)} {hex(speed_percent)}"
        return self.run_raw_ipmi_command(command_args)

    def get_fan_speed(self):

        fan_data = []

        command = f"sensor list 2>/dev/null | grep -iE FAN[0-9A-Z]+"
        command_output = self.run_ipmi_command(command)

        if not command_output:
            return fan_data

        lines = command_output.strip().split('\n')
        for line in lines:
            parts = line.split("|")
            fan_name = parts[0].strip()
            fan_speed = parts[1].strip()

            try:
                fan_speed = int(float(fan_speed))
            except ValueError:
                fan_speed = "N/A"

            fan_data.append((fan_name, fan_speed))

        return fan_data

    def get_fan_speed_bis(self):

        fan_data = []

        command = f"sdr 2>/dev/null | grep -iE FAN[0-9A-Z]+"
        command_output = self.run_ipmi_command(command)

        if not command_output:
            return fan_data

        lines = command_output.strip().split('\n')
        for line in lines:
            parts = line.split("|")
            fan_name = parts[0].strip()
            fan_speed = parts[1].strip()

            try:
                fan_speed = int(fan_speed.split()[0])
            except ValueError:
                fan_speed = "N/A"

            fan_data.append((fan_name, fan_speed))

        return fan_data

    def reset_bmc(self, reset_type="warm"):
        if reset_type in ["cold", "warm"]:
            command_args = f"bmc reset {reset_type}"
            return self.run_ipmi_command(command_args, sleep_time=5)
        else:
            print("Unsupported BMC reset type")
            return False


if __name__ == "__main__":
    import time

    ipmi = Ipmitool()
    # ipmi.set_fan_mode("full")
    # ipmi.reset_bmc()

    while True:
        try:
            start_time = time.time()  # Enregistrez le temps de début
            print(ipmi.get_fan_speed_bis())
            end_time = time.time()  # Enregistrez le temps de fin
            elapsed_time = end_time - start_time  # Calculez le temps écoulé
            print(f"Temps écoulé pour get_fan_speed_bis(): {elapsed_time} secondes")
            time.sleep(1)
        except KeyboardInterrupt:
            break
