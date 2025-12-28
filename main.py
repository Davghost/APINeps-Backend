import os
from factory import create_app

config_name = os.environ.get("CONFIG_CLASS", "config.DevelopmentConfig")
app = create_app(config_name)