import logging
from configs.config_loader import ConfigLoader

config = ConfigLoader.get_config()
logger = logging.getLogger(config.get("service"))

from repositories.products_repo import products_get_all

def get_all_products():
    logger.info("Service layer: Get all products.")
    products = None
    try:
        products = products_get_all()
    except:
        raise Exception("There are some issue fetching pro")

    logger.warning("There are some warning in the logic.")
    return products