class ConfigValidator:
    REQUIRED_VARS = [
        "WEBHOOK_URL",
        "DISK_FAN_SPEED_GRID",
        "CPU_FAN_SPEED_GRID",
        "NOTIFICATION_DISK_REACH_HIGH_TEMPERATURE",
        "NOTIFICATION_DISK_REACH_LOW_TEMPERATURE",
        "NOTIFICATION_SEND_EVERY_MINUTE",
        "PROMETHEUS_ENABLE",
        "PROMETHEUS_PORT",
    ]

    def __init__(self):
        import config
        self.config = config

    def validate(self):
        self.check_required_vars()
        self.validate_webhook()
        self.validate_temp_thresholds()
        self.validate_fan_grids()
        self.validate_prometheus_exporter()
        print("✅ Configuration is valid ✅")

    def check_required_vars(self):
        for var in self.REQUIRED_VARS:
            if not hasattr(self.config, var):
                raise AttributeError(f"❌ Missing required config variable: {var}")

    def validate_webhook(self):
        value = self.config.WEBHOOK_URL
        assert (
            value is None or (isinstance(value, str) and value.startswith("http"))
        ), "WEBHOOK_URL must be a valid URL or set to None if not used !"

    def validate_prometheus_exporter(self):
        value = self.config.PROMETHEUS_PORT
        assert (
            isinstance(value, int) and 1024 <= value <= 65535
        ), "PROMETHEUS_PORT must be between 1024 and 65535"

        assert isinstance(self.config.PROMETHEUS_ENABLE, bool), "PROMETHEUS_ENABLE must be set to True or False if not used !"

    def validate_temp_thresholds(self):
        assert isinstance(self.config.NOTIFICATION_DISK_REACH_HIGH_TEMPERATURE, int), "NOTIFICATION_DISK_REACH_HIGH_TEMPERATURE must be an int"
        assert isinstance(self.config.NOTIFICATION_DISK_REACH_LOW_TEMPERATURE, int), "NOTIFICATION_DISK_REACH_LOW_TEMPERATURE must be an int"
        assert isinstance(self.config.NOTIFICATION_SEND_EVERY_MINUTE, int) and self.config.NOTIFICATION_SEND_EVERY_MINUTE > 0, "NOTIFICATION_SEND_EVERY_MINUTE must be a positive int"

    def validate_fan_grids(self):
        for name in ["DISK", "CPU"]:
            grid = getattr(self.config, f"{name}_FAN_SPEED_GRID")
            assert isinstance(grid, dict) and grid, f"{name}_FAN_SPEED_GRID must be a non-empty dict"

            for temperature, fan_speed in grid.items():
                assert isinstance(fan_speed, int) and 0 <= fan_speed <= 100, f"Fan speed for {name}_FAN_SPEED_GRID must be between 0 and 100"

                if isinstance(temperature, tuple):
                    assert len(temperature) == 2 and all(isinstance(i, int) for i in temperature), f"{name}_FAN_SPEED_GRID temp range must be tuple of 2 int"
                    assert temperature[0] <= temperature[1], (
                        f"{name}_FAN_SPEED_GRID range {temperature} is invalid ! "
                        f"The first value (min) must be less than or equal to the second value (max)"
                    )
                elif not isinstance(temperature, int):
                    raise ValueError(
                        f"{name}_FAN_SPEED_GRID key {temperature} is invalid. "
                        f"Expected either an integer (exact temperature) or a tuple (min_temp, max_temp)."
                    )

            # TODO: Better way to handle these two check
            # Check that ranges are sorted by ascending temperature
            keys = list(grid.keys())

            def get_min_temp(key):
                return key if isinstance(key, int) else key[0]

            min_values = [get_min_temp(k) for k in keys]
            if min_values != sorted(min_values):
                raise ValueError(
                    f"{name}_FAN_SPEED_GRID keys must be ordered by ascending temperature.\n"
                    f"Expected: {[k for _, k in sorted(zip(min_values, keys))]}\n"
                    f"Found:    {keys}"
                )

            # Check overlapping temperature ranges
            ranges = [(k, k) if isinstance(k, int) else k for k in keys]

            for i in range(len(ranges) - 1):
                current_start, current_end = ranges[i]
                next_start, next_end = ranges[i + 1]

                if next_start <= current_end:
                    raise ValueError(
                        f"{name}_FAN_SPEED_GRID has overlapping temperature ranges: "
                        f"{keys[i]} overlaps with {keys[i + 1]}"
                    )
