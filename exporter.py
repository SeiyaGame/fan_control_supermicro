import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "lib")))

from prometheus_client import start_http_server, Gauge

DEFAULT_PREFIX = "fan_control_supermicro"

DISK_TEMPERATURE = Gauge(
    name=f"{DEFAULT_PREFIX}_disk_temperature",
    documentation="Temperature of disk",
    labelnames=['name', 'serial_number']
)

CPU_TEMPERATURE = Gauge(
    name=f"{DEFAULT_PREFIX}_cpu_temperature",
    documentation="Temperature of CPU",
)

IPMI_FAN_SPEED = Gauge(
    name=f"{DEFAULT_PREFIX}_ipmi_fan_speed",
    documentation="Ipmi fan speed recovery",
    labelnames=['name']
)

FAN_SPEED_BY_ZONE = Gauge(
    name=f"{DEFAULT_PREFIX}_fan_speed_by_zone",
    documentation="Fan speed for the current zone in percent",
    labelnames=['zone'],
)


def fetch(disk_info, fan_speed, current_fan_speed):
    for name, temperature, serial_number in disk_info:
        DISK_TEMPERATURE.labels(name=name, serial_number=serial_number).set(temperature)

    for name, temperature in fan_speed:
        if temperature == 'N/A':
            temperature = -1

        IPMI_FAN_SPEED.labels(name=name).set(temperature)

    for key in current_fan_speed.keys():
        temp_range, fan_speed = current_fan_speed[key]
        FAN_SPEED_BY_ZONE.labels(zone=key).set(fan_speed)


def setup(exporter_port=9495):
    start_http_server(exporter_port)