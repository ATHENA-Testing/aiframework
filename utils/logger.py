import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name="automation", log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    if not os.path.exists("reports/logs"):
        os.makedirs("reports/logs")
        
    # Console Handler
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)
    
    # File Handler
    fh = RotatingFileHandler("reports/logs/automation.log", maxBytes=10*1024*1024, backupCount=5)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    
    return logger

logger = setup_logger()
