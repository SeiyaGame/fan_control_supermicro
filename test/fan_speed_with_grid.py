# Fan speed control grid based on hard drive temperatures
disk_fan_speed_grid = {
    (0, 24): 0,
    25: 13,
    35: 18,
    40: 30,
    45: 35,
    50: 50,
    60: 100
}

disk_fan_speed_grid_not_order = {
    25: 13,
    60: 100,
    45: 35,
    35: 18,
    40: 30,
    50: 50,
    (0, 24): 0
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
self_dry_run = True

def set_fan_speed_by_temperature(zone, temperature, fan_speed_grid):
    current_temp_range, current_fan_speed = self_current_fan_speed.get(zone, ((-1, -1), None))

    def update_fan_speed(temp_grid, fan_speed_percent_grid):
        if current_fan_speed is None or current_fan_speed != fan_speed_percent_grid:
            self_current_fan_speed[zone] = temp_grid, fan_speed_percent_grid

            fan_speed_status = f"Set fan speed for the {zone} zone to {fan_speed_percent_grid}% ({hex(fan_speed_percent_grid)}) "

            if isinstance(temp_grid, int):
                fan_speed_status += f"(Temperature reach: {temp_grid})"
            elif isinstance(temp_grid, tuple):
                fan_speed_status += f"(Temperature range: {temp_grid[0]} → {temp_grid[1]})"

            print(fan_speed_status)
            # logger.info(fan_speed_status)

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

    for temp_grid, fan_speed_percent_grid in fan_speed_grid.items():
        if isinstance(temp_grid, tuple):
            if temp_grid[0] <= temperature <= temp_grid[1]:
                update_fan_speed(temp_grid, fan_speed_percent_grid)
                return
        elif isinstance(temp_grid, int):
            if temperature == temp_grid:
                update_fan_speed(temp_grid, fan_speed_percent_grid)
                return


if __name__ == '__main__':
    print('Test set_fan_speed_by_temperature for peripheral:')
    set_fan_speed_by_temperature("peripheral", 35, disk_fan_speed_grid)

    print('Test set_fan_speed_by_temperature for CPU:')
    set_fan_speed_by_temperature("cpu", 35, disk_fan_speed_grid)