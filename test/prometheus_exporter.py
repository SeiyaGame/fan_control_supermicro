import os, sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import exporter

if __name__ == "__main__":

    http_port = 9495
    exporter.setup(http_port)
    print(f"HTTP server accessible on 127.0.0.1:{http_port}")

    while True:
        try:

            exporter.fetch(
                cpu_temperature = 52,
                disk_info= [
                    ('sda', 31, 'K4X9R2TQ'), ('sdb', 26, 'Q1Z3M8VW'), ('sdc', 31, 'B7F5X2L9J0H3'), ('sdd', 34, 'T6G1K7M3V2Z9'),
                    ('sde', 33, 'M3P9H4ND'), ('sdf', 35, 'V7X1Q2LB'), ('sdg', 29, 'L5N3Z8AW'), ('sdh', 33, 'Y2W4K6MS'),
                    ('sdi', 32, 'C8L7J3ZT'), ('sdj', 32, 'P9Q6M4BR'), ('sdk', 32, 'R3X7N8LQ'), ('nvme0n1', 43, 'Q7L9P2W6K3JD85')
                ],
                fan_speed= [
                    ('FAN1', 1000), ('FAN2', 'N/A'), ('FAN3', 'N/A'),
                    ('FAN4', 'N/A'), ('FAN5', 800), ('FANA', 600), ('FANB', 700)
                ],
                current_fan_speed= {'peripheral': (35, 65), 'cpu': (32, 100)}
            )
            time.sleep(1)

        except KeyboardInterrupt:
            break