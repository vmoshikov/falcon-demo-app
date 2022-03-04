import falcon

from exceptions import MyException
import json
import jwt
from logger import logger
from passlib.hash import sha256_crypt


USERS = {
    "admin":
    {
        "login": 'admin',
        "password": sha256_crypt.encrypt('admin')
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
        pass

    def process_resource(self, req, resp, resource, params):
        """
        Обрабатывает запрос после роутинга.
        Этот метод вызывается только когда URL реквеста совпадает с URL ведущему к ресурсу.

        resource: это объект Resource куда пришел запрос
        params: это словарь (dict) с параметрами полученными из URI
        """
        logger.warning('MIDDLEWARE: process_resource')
        if req.path == '/login/':
            logger.info('MIDDLEWARE: Страница авторизации')
            data = req.get_media()
            logger.debug('Идентификация')
            print(data.get('login'), data.get('password'))
            if data.get('login') and data.get('password'):
                user = USERS.get(data.get('login'))
                print(user.get('login'), user.get('password'))
                if user:
                    if True:
                        # TODO  реализовать проверку пароля
                        pass
                    else:
                        raise falcon.HTTPUnauthorized

        elif req.get_header("Authorization", required=True):
            header = req.get_header("Authorization", required=True).split(' ')
            token = header[1]
            # TODO see token
            pass

        else:
            # Исключение
            raise MyException('Ошибка')

    def process_response(self, req, resp, resource, req_succeeded):
        """
        Этот метод вызовется после обработки ответа (после роутинга)

        req_succeeded - успешно ли обработался запрос, True если не было эксепшенов
        """
        logger.warning('MIDDLEWARE: process_response')
        pass


class AuthMiddleware(Middleware):
    def process_request(self, req, resp):
        # resp.complete = True
        logger.warning('MIDDLEWARE: process_request')