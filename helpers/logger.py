import logging
import os
from logging import config as loggin_config

import yaml

if not os.getenv("CI"):
    # https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19#issuecomment-1039405731
    with open("logging.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        loggin_config.dictConfig(config)

logger = logging.getLogger("CORE")
logger.info("CORE started!")
