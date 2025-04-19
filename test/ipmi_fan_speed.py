import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from test_data import fan_sensor_list_bis,fan_sensor_list


def get_fan_speed_bis(data):

    lines = data.strip().split('\n')
    for line in lines:
        parts = line.split("|")
        fan_name = parts[0].strip()
        fan_speed = parts[1].strip()

        try:
            fan_speed = int(fan_speed.split()[0])
        except ValueError:
            fan_speed = "N/A"

        print((fan_name, fan_speed))


def get_fan_speed(data):

    lines = data.strip().split('\n')
    for line in lines:
        parts = line.split("|")
        fan_name = parts[0].strip()
        fan_speed = parts[1].strip()

        try:
            fan_speed = int(float(fan_speed))
        except ValueError:
            fan_speed = "N/A"

        print((fan_name, fan_speed))


if __name__ == "__main__":
    print("\nGet fan sensor:")
    get_fan_speed(fan_sensor_list)

    print("\nGet fan sensor bis:")
    get_fan_speed_bis(fan_sensor_list_bis)