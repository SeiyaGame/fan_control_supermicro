# Fan speed control grid based on hard drive temperatures
disk_fan_speed_grid = {
    (0, 23): 40,
    (25, 30): 50,
    (32, 34): 60,
    35: 65,
    37: 75,
    (38, 40): 80,
    (42, 45): 90,
    (46, 60): 100,
}

# Fan speed control grid based on CPU temperatures
cpu_fan_speed_grid = {
    (0, 24): 0,
    38: 20,
    40: 25,
    45: 30,
    50: 40,
    60: 50,
    70: 60,
    80: 100
}

# Fan speed control grid based on hard drive temperatures
# disk_fan_speed_grid = {
#     (0, 27): 40,  # Temperature from 0°C to 30°C: 40%
#     (28, 30): 50,  # Temperature from 28°C to 30°C: 50%
#     (31, 34): 60,  # Temperature from 31°C to 34°C: 60%
#     35: 65,  # Temperature reaches 35°C: 65%
#     36: 70,  # Temperature reaches 36°C: 70%
#     37: 75,  # Temperature reaches 37°C: 75%
#     (38, 40): 80,  # Temperature from 38°C to 40°C: 80%
#     (41, 45): 90,  # Temperature from 41°C to 45°C: 90%
#     (46, 60): 100,  # Temperature from 46°C to 65°C: 100%
# }
#
# # Fan speed control grid based on CPU temperatures
# cpu_fan_speed_grid = {
#     (0, 25): 30,  # Temperature from 0°C to 25°C: 30%
#     (26, 34): 45,  # Temperature from 26°C to 34°C: 45%
#     (35, 40): 55,  # Temperature from 35°C to 40°C: 55%
#     (41, 45): 60,  # Temperature from 41°C to 45°C: 60%
#     46: 65,  # Temperature reaches 46°C: 65%
#     47: 70,  # Temperature reaches 47°C: 70%
#     (48, 60): 70,  # Temperature from 50°C to 60°C: 75%
#     (61, 80): 85,  # Temperature from 61°C to 80°C: 85%
#     (81, 100): 100  # Temperature from 61°C to 100°C: 100%
# }

self_current_fan_speed = dict()
self_dry_run = False

def set_fan_speed_by_temperature(zone, temperature, fan_speed_grid):
    current_temp_range, current_fan_speed = self_current_fan_speed.get(zone, ((-1, -1), None))
    # current_temp_range, current_fan_speed = self.current_fan_speed.get(zone, ((-1, -1), None))

    def update_fan_speed(temp_grid, fan_speed_percent_grid):
        if current_fan_speed is None or current_fan_speed != fan_speed_percent_grid:
            self_current_fan_speed[zone] = temp_grid, fan_speed_percent_grid
            # self.current_fan_speed[zone] = temp_grid, fan_speed_percent_grid

            fan_speed_status = f"Set fan speed for the {zone} zone to {fan_speed_percent_grid}% ({hex(fan_speed_percent_grid)}) "

            if isinstance(temp_grid, int):
                label = "Temperature reach" if temp_grid == temperature else "Fallback to"
                fan_speed_status += f"({label}: {temp_grid})"

            elif isinstance(temp_grid, tuple):
                in_range = temp_grid[0] <= temperature <= temp_grid[1]
                label = "Temperature range" if in_range else "Fallback range"
                fan_speed_status += f"({label}: {temp_grid[0]} → {temp_grid[1]})"

            print(fan_speed_status)
            # logger.info(fan_speed_status)

            # if not self.dry_run:
            if not self_dry_run:
                if zone == 'cpu':
                    print(f"self.ipmitool.set_fan_speed(0, {fan_speed_percent_grid})")
                    # self.ipmitool.set_fan_speed(0, fan_speed_percent_grid)
                elif zone == 'peripheral':
                    print(f"self.ipmitool.set_fan_speed(1, {fan_speed_percent_grid})")
                    # self.ipmitool.set_fan_speed(1, fan_speed_percent_grid)
                else:
                    print(f"The zone {zone} doesn't exist or is not implemented yet!")
                    # logger.warning(f"The zone {zone} doesn't exist or is not implemented yet!")

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
    print(f"No fallback rules found for {zone} at {temperature}°C")
    # logger.warning(f"No fallback rules found for {zone} at {temperature}°C")
    update_fan_speed(temperature, 100)


if __name__ == '__main__':

    for temp in [18, 24, 32, 35, 36, 101, -5]:

        # Reset dict to ignore last set value
        self_current_fan_speed = dict()

        print(f'\nTest set_fan_speed_by_temperature for peripheral with {temp}°C :')
        set_fan_speed_by_temperature("peripheral", temp, disk_fan_speed_grid)

        print(f'\nTest set_fan_speed_by_temperature for CPU with {temp}°C :')
        set_fan_speed_by_temperature("cpu", temp, cpu_fan_speed_grid)