import json, os
import falcon
import requests
from logger import logger
from exceptions import MyException
from repository import JsonRepository
from hooks import login_required
from falcon import Request, Response
import jwt

SECRET = "DFSDDF2345msf23asdfs"

books = JsonRepository()


def compare_ops(op, f_val, i_val):
    if op == 'gte':
        if i_val >= f_val:
            logger.debug('Больше или равно')
            return True

    elif op == 'lte':
        if i_val <= f_val:
            logger.debug('Меньше или равно')
            return True


class Authorisation:
    """
    Контроллер авторизации
    """
    def on_post(self, req: Request, resp: Response):
        data = req.get_media()
        logger.debug('Аутентификация')
        token = jwt.encode(data, key=SECRET)
        resp.text = json.dumps({'token': token})
        resp.status = falcon.HTTP_200


# @falcon.before(login_required)
class BookController:
    """
    Контроллер работы с конкретной книгой
    """
    def on_get(self, req: Request, resp: Response, book_id):
        book = books.get_by_id(int(book_id))

        if book:
            resp.text = json.dumps(book)
            resp.status = falcon.HTTP_200
        else:
            raise MyException

    def on_put(self, req: Request, resp: Response, book_id):
        data = req.get_media()
        books.update(int(book_id), data)
        books.commit()

        resp.text = json.dumps(books.get_by_id(int(book_id)))
        resp.status = falcon.HTTP_202

    def on_delete(self, req: Request, resp: Response, book_id):
        books.remove(int(book_id))
        # books.commit()


class BooksController:
    """
    Контроллер работы со списком книг
    """
    filtering_fields = ("year", "pages")

    def on_get(self, req: Request, resp: Response):
        # Получение фильтров
        offset = req.get_param_as_int('offset')
        limit = req.get_param_as_int('limit')

        # Фильтрация
        filtered_books = []

        books_list = books.get_list()

        # for b in books_list:
        #     if req.get_param('year'):
        #         filter_year_ops, filter_year = req.get_param('year').split(':')
        #         if compare_ops(filter_year_ops, int(filter_year), int(b.get('year'))):
        #             filtered_books.append(b)
        #
        #     for fb in filtered_books:
        #         if req.get_param('pages'):
        #             filter_pages_ops, filter_pages = req.get_param('pages').split(':')
        #             if compare_ops(filter_pages_ops, int(filter_pages), int(fb.get('pages'))):
        #                 continue

        resp.text = json.dumps(filtered_books)
        resp.status = falcon.HTTP_200

    def on_post(self, req: Request, resp: Response):
        new_id = books.get_last_id() + 1
        data = req.get_media()
        data['id'] = new_id

        books.append(data)
        # books.commit()

        resp.text = json.dumps(data)
        resp.status = falcon.HTTP_201
