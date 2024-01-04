import logging
import requests
from logging.handlers import RotatingFileHandler

VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]


# # Then later in your code, you can retrieve the logger like this:
# logger = logging.getLogger("NAME_OF_THE_LOGGER")
# logger.info("This is an information message.")

class Logger:

    def __init__(self, name, log_level="INFO", log_file='fan_control.log',
                 log_file_max_size_in_mb=5, log_file_max_rotation=3, webhook_url=None):
        self.name = name
        self.log_level = log_level
        self.log_file = log_file
        self.log_file_max_size_in_mb = log_file_max_size_in_mb
        self.log_file_max_rotation = log_file_max_rotation
        self.webhook_url = webhook_url
        self.logger = logging.getLogger(self.name)

    def setup(self):
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        date_format = '%d/%m/%Y %H:%M:%S'
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

        if self.log_level is None or self.log_level == "":
            raise ValueError("Log level undefined or empty. Check config please.")

        if not self.log_level.upper() in VALID_LOG_LEVELS:
            raise ValueError(f"Invalid log level: {self.log_level}")

        numeric_log_level = getattr(logging, self.log_level.upper(), None)
        if not numeric_log_level:
            raise ValueError(f"Invalid log level: {self.log_level}")

        self.logger.setLevel(numeric_log_level)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if self.webhook_url:
            webhook_handler = WebhookHandler(self.webhook_url)
            self.logger.addHandler(webhook_handler)

        if self.log_file:
            try:
                file_handler = RotatingFileHandler(
                    filename=self.log_file,
                    maxBytes=self.log_file_max_size_in_mb * 1024 * 1024,  # Bytes to Megabytes
                    backupCount=self.log_file_max_rotation,
                    encoding='utf-8'
                )
            except Exception:
                self.logger.exception("Problems setting up log file.")
                raise

            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        return self.logger


class WebhookHandler(logging.Handler):
    def __init__(self, webhook_url):
        super().__init__()
        self.webhook_url = webhook_url

        _log_format = '`%(asctime)s` - `%(levelname)s` - %(message)s'
        _date_format = '%d/%m/%Y %H:%M:%S'
        self.formatter = logging.Formatter(fmt=_log_format, datefmt=_date_format)

    def emit(self, record):
        log_entry = self.format(record)
        # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        data = {"content": log_entry}
        try:
            response = requests.post(self.webhook_url, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(f"Failed to send log to webhook: {err}")
