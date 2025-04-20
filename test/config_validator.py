import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.config_validator import ConfigValidator

if __name__ == '__main__':
    config_validator = ConfigValidator()
    config_validator.validate()