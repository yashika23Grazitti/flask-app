import logging, requests, sys
from pyconman import ConfigLoader

config = ConfigLoader.get_config()
logger = logging.getLogger(config.get("service"))

def products_get_all():
    logger.info("Repository layer: Get all products.")
    # DB & ORM functional call.
    response = requests.get("https://fakestoreapi.com/products")
    logger.error("Products fetched from Fake API with status code = {status}".format(status = response.status_code))
    return response.json()