import falcon

from exceptions import MyException
import json
import jwt
from logger import logger
import hashlib

SECRET = "DFSDDF2345msf23asdfs"

USERS = {
    "admin":
        {
            "login": "admin",
            "password": hashlib.sha256("password".encode()).hexdigest()
        }
}

# Поделиться https://github.com/falconry/falcon-policy

class AddHeaderComponent:
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('X-Request-Name', '*')
        resp.set_header('Content-Type', 'application/json')
        resp.set_header('Access-Control-Max-Age', '86400')

class Middleware:
    "Базовое представление Middleware"
    def process_request(self, req, resp):
        """
        Обрабатывает запрос до роутинга

        Так как Falcon роутит каждый запрос базируясь на значении в req.path,
        запрос может быть эффективно перенаправлен если засетить в req.path другое значение
        в методе process_request()
        """
        logger.warning('MIDDLEWARE: process_request')
        pass

    def process_resource(self, req, resp, resource, params):
        """
        Обрабатывает запрос после роутинга.
        Этот метод вызывается только когда URL реквеста совпадает с URL ведущему к ресурсу.

        resource: это объект Resource куда пришел запрос
        params: это словарь (dict) с параметрами полученными из URI
        """
        logger.warning('MIDDLEWARE: process_resource')
        pass


    def process_response(self, req, resp, resource, req_succeeded):
        """
        Этот метод вызовется после обработки ответа (после роутинга)

        req_succeeded - успешно ли обработался запрос, True если не было эксепшенов
        """
        logger.warning('MIDDLEWARE: process_response')
        pass


class AuthMiddleware(Middleware):
    def process_resource(self, req, resp, resource, params):
        logger.warning('MIDDLEWARE: process_resource')
        if req.path == '/login/':
            logger.info('MIDDLEWARE: Страница авторизации')
            data = req.get_media()
            logger.debug('Идентификация')
            if data.get('login') and data.get("password"):
                user = USERS.get(data.get('login'))
                if user and user.get("password") == hashlib.sha256(data.get("password").encode()).hexdigest():
                    # Логин и пароль корректный
                    return True
                else:
                    raise falcon.HTTPUnauthorized

        elif req.method == 'POST' or req.method == 'PUT':
            # POST требует авторизации
            if req.get_header("Authorization", required=True):
                header = req.get_header("Authorization", required=True).split(' ')
                token = header[1]

                result = jwt.decode(token, SECRET, algorithms=["HS256"])
                logger.warning(result)
                user = USERS.get(result.get('login'))

                if not user and not user.get("password") == hashlib.sha256(result.get("password").encode()).hexdigest():
                    raise falcon.HTTPUnauthorized

            else:
                # Исключение
                raise MyException('Ошибка')

        # resp.complete = True