import logging
import sys

def setup_logger(name: str = "skylark_bi") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.formatters if hasattr(logging, "formatters") else None
        log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(log_format)
        logger.addHandler(handler)
    return logger

logger = setup_logger()
