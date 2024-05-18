# Fan speed control grid based on hard drive temperatures
disk_fan_speed_grid = {
    (0, 27): 40,  # Temperature from 0°C to 30°C: 40%
    (28, 30): 50,  # Temperature from 28°C to 30°C: 50%
    (31, 34): 60,  # Temperature from 31°C to 34°C: 60%
    (35, 37): 70,  # Temperature from 35°C to 37°C: 70%
    (38, 40): 80,  # Temperature from 38°C to 40°C: 80%
    (41, 45): 90,  # Temperature from 41°C to 45°C: 90%
    (46, 60): 100,  # Temperature from 46°C to 650°C: 100%
}

# Fan speed control grid based on CPU temperatures
cpu_fan_speed_grid = {
    (0, 25): 30,  # Temperature from 0°C to 25°C: 30%
    (26, 34): 45,  # Temperature from 26°C to 34°C: 45%
    (35, 40): 55,  # Temperature from 35°C to 40°C: 55%
    (41, 50): 60,  # Temperature from 41°C to 50°C: 60%
    (51, 60): 70,  # Temperature from 51°C to 60°C: 70%
    (61, 80): 85,  # Temperature from 61°C to 80°C: 85%
    (81, 100): 100  # Temperature from 61°C to 100°C: 100%
}

# If you want to send log to discord, put the URL here !
DISCORD_WEBHOOK_LOGS = ""
