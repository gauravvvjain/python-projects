import os
import logging
from typing import Optional

def setup_logger(name: str, log_file: Optional[str] = None, level=logging.INFO) -> logging.Logger:
    """Function to setup a logger."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding multiple handlers if logger is called multiple times
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if log_file:
            # Ensure the directory for the log file exists
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger

def validate_dataset_path(filepath: str) -> bool:
    """Check if the dataset file exists and is readable."""
    return os.path.exists(filepath) and os.path.isfile(filepath)

def ensure_directory_exists(directory_path: str):
    """Ensure that a directory exists."""
    os.makedirs(directory_path, exist_ok=True)
