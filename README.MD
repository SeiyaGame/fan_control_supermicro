# Fan Control Script for Supermicro

## Resources

- [Supermicro X9/X10/X11 Fan Speed Control](https://forums.servethehome.com/index.php?resources/supermicro-x9-x10-x11-fan-speed-control.20/)

## Description

This Python script is designed to automatically control the fan speeds of a server based on the temperatures of the hard drives and the CPU. It uses IPMI tools to adjust fan speeds in response to temperature changes, ensuring optimal cooling and performance of the server.

## Features

- Dynamically adjusts fan speeds based on HDD and CPU temperatures.
- Customizable temperature thresholds for different fan speeds.
- Supports different zones (CPU and peripheral) for targeted cooling.
- Dry run mode for testing without applying changes.
- Metrics (Prometheus Exporter).

## TODO

- [x] Setting up logs
- [ ] Create a web interface to display temperature data ??
- [x] Setting up Prometheus exporter
- [ ] Restrict this script to only works on DEBIAN and TrueNAS SCALE

## Requirements

- Python 3.x
- Access to IPMI on the server. (`/usr/bin/ipmitool`)

## Installation

> [!WARNING]
> Tested only on H11SSL-i/c/nc motherboard. I need your feedback/help for the others !

Ensure Python 3.x is installed on your server.  
Install ipmitool on your server or ensure it's already installed ( Debian default path : `/usr/bin/ipmitool`)  

Then Clone the project on your folder : `git clone https://github.com/SeiyaGame/fan_control_supermicro.git`

Or download the script and run it :

> [!NOTE]
> Run the script at your own risk !

> [!WARNING]
> Make sure you are in the folder where you want to install fan_control !

```bash
cd folder_where_you_want
wget https://raw.githubusercontent.com/SeiyaGame/fan_control_supermicro/main/install_script.sh
chmod +x install_script.sh && ./install_script.sh
```

Finally, you can copy the `config.sample.py` as `config.py` and then edit the variables in the file.  
After that start the service: `service fan-control start` or run the script `python3 fan_control_script.py`

To see logs you can use the command `fan-control-logs` which is added when you run the script before !  
Or you can do it manually with `tail -f -n 15 /mnt/tank/scripts/fan_control/logs/fan_control.log`

## Usage

1. Configure the fan speed grids (**DISK_FAN_SPEED_GRID** and **CPU_FAN_SPEED_GRID**) as per your requirements.
2. Run the script: `python3 fan_control_script.py`
3. Optionally, enable dry run mode by adding `-d` or `--dry_run` to test without applying changes.
4. Optionally, you can send logs message to a webhook url by editing variables in the file `config.py` or by adding `--webhook_url 'YOUR_URL'`
5. Optionally, you can enable metrics (Prometheus Exporter) in the file `config.py` or by adding `--prometheus_enable`. Default port is `9495`

```bash
usage: fan_control_script.py [-h] [-d] [--no_console_log_stream] [--webhook_url WEBHOOK_URL] [--only_alert] [--prometheus_enable] [--prometheus_port PROMETHEUS_PORT]

Control fan speed via IPMI of Supermicro motherboard

options:
  -h, --help            show this help message and exit
  -d, --dry_run         No changes made, only to visualised
  --no_console_log_stream
                        Disable Stream log in console
  --webhook_url WEBHOOK_URL
                        Send message to a webhook url
  --only_alert          Send only alert message to the webhook url (Default: True)
  --prometheus_enable   Enable Prometheus exporter (Default: False)
  --prometheus_port PROMETHEUS_PORT (Default: 9495)
                        Listening port for Prometheus exporter
```


### Output in your console

```bash
Fan mode set to FULL
Set fan speed for the peripheral zone to 70% (0x46) (Temperature range: 35 → 37)
Set fan speed for the cpu zone to 45% (0x2d) (Temperature range: 26 → 34)
-----------
HDD ↑ 36°C (35 → 37) 70% 💨 | CPU 30°C (26 → 34) 45% 💨

FAN1(700 RPM) | FAN2(700 RPM) | FAN3(700 RPM) | FAN4 | FAN5(700 RPM) | FANA(1000 RPM) | FANB(1000 RPM)

  sda   - 32°C - S/N: ZCT3S9M0     |   sdb   - 27°C - S/N: HLH01J2B     |   sdc   - 32°C - S/N: 2244E6812B23
  sdd   - 34°C - S/N: 2244E6812A49 |   sde   - 33°C - S/N: ZR13LBZD     |   sdf   - 36°C - S/N: ZCT3S7WH
  sdg   - 31°C - S/N: 5PH7PMDE     |   sdh   - 34°C - S/N: ZCT3S1HP     |   sdi   - 34°C - S/N: 5PH7P38E
  sdj   - 34°C - S/N: 5PH7NZEE     |   sdk   - 35°C - S/N: 5PH7J96F     | nvme0n1 - 48°C - S/N: 21337W443408
```

## Truenas Scale Setup

Follow the step [here](#installation) but install the script in a dataset of your pool for exemple in `/mnt/tank/scripts/fan_control`  
Then go the Truenas scale web interface in `System Settings` -> `Advanced` -> `Init/Shutdown Scripts` and click `Add`

- Description: `Script to control fan speed`
- Type: `Command`
- Script: `cd /mnt/tank/scripts/fan_control && chmod +x setup_fan_control_supermicro.sh && ./setup_fan_control_supermicro.sh`
- When: `Post Init`
- Enable: `Yes`

## Limitations

- Currently, supports only Debian-based systems and TrueNAS Scale. (planned to restrict)
- Does not include a web interface

## Contributing

Contributions to this project are welcome. Please fork the repository and submit pull requests for any enhancements.
