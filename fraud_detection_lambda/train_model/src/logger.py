import logging

def get_logger(name=__name__):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger