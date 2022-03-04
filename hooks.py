import falcon
from logger import logger

def login_required(req, resp, resource, params):
    logger.debug('Проверка авторизации')
    raise falcon.HTTPUnauthorized
