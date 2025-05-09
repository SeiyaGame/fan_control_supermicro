# Fan speed control grid based on hard drive temperatures
DISK_FAN_SPEED_GRID = {
    (0, 27): 40,  # Temperature from 0°C to 30°C: 40%
    (28, 30): 50,  # Temperature from 28°C to 30°C: 50%
    (31, 34): 60,  # Temperature from 31°C to 34°C: 60%
    35: 65,  # Temperature reach 35°C: 65%
    36: 70,  # Temperature reach 36°C: 70%
    37: 75,  # Temperature reach 37°C: 75%
    (38, 40): 80,  # Temperature from 38°C to 40°C: 80%
    (41, 45): 90,  # Temperature from 41°C to 45°C: 90%
    (46, 60): 100,  # Temperature from 46°C to 650°C: 100%
}

# Fan speed control grid based on CPU temperatures
CPU_FAN_SPEED_GRID = {
    (0, 25): 30,  # Temperature from 0°C to 25°C: 30%
    (26, 34): 45,  # Temperature from 26°C to 34°C: 45%
    (35, 40): 55,  # Temperature from 35°C to 40°C: 55%
    (41, 45): 60,  # Temperature from 41°C to 45°C: 60%
    46: 65,  # Temperature reach 46°C: 65%
    47: 70,  # Temperature reach 47°C: 70%
    (48, 60): 70,  # Temperature from 50°C to 60°C: 75%
    (61, 80): 85,  # Temperature from 61°C to 80°C: 85%
    (81, 100): 100  # Temperature from 61°C to 100°C: 100%
}

# If you want to send log to a webhook, put the URL here !
WEBHOOK_URL = None

# Send a webhook notification when DISK reach a certain temperature
NOTIFICATION_DISK_REACH_HIGH_TEMPERATURE = 40
NOTIFICATION_DISK_REACH_LOW_TEMPERATURE = 10

# Send a webhook notification at least every X minutes if temperature is reach
NOTIFICATION_SEND_EVERY_MINUTE = 5

# Enable prometheus metrics
PROMETHEUS_ENABLE = False
# Http port for prometheus metrics Default: 9495
PROMETHEUS_PORT = 9495