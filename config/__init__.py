import toml
import os
from dotenv import load_dotenv

load_dotenv()

config_name = os.environ.get("CONFIG")

if config_name is None:
    raise Exception("CONFIG not specified")

config = toml.load("{}/{}/config.toml".format(os.path.dirname(__file__), config_name))
