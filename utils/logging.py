import logging
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with a specified name and save logs in the 'log' folder.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger.
    """
    # Ensure the 'log' folder exists
    if not os.path.exists('log'):
        os.makedirs('log')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the default log level to DEBUG

    # Create a formatter that includes the timestamp, log level, and message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a console handler to log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the log level for the console
    console_handler.setFormatter(formatter)

    # Create a file handler to save logs to a file in the 'log' folder
    log_file_path = os.path.join('log', 'app.log')
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')  # Ensure UTF-8 encoding
    file_handler.setLevel(logging.DEBUG)  # Set the log level for the file
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
