import time
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.cpu_monitor import CPUMonitor


if __name__ == "__main__":

    cpu_monitor = CPUMonitor()

    while True:
        try:
            start_time = time.time()
            print(cpu_monitor.get_cpu_temperature())
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Time elapsed for get_cpu_temperature(): {elapsed_time} second(s)")
            time.sleep(1)
        except KeyboardInterrupt:
            break
