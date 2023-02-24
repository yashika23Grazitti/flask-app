import logging, requests, sys
logger = logging.getLogger("flask-app")

def products_get_all():
    logger.info("Repository layer: Get all products.")
    # DB & ORM functional call.
    response = requests.get("https://fakestoreapi.com/products")
    logger.error("Products fetched from Fake API with status code = {status}".format(status = response.status_code))
    return response.json()