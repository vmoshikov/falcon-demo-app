from views import BooksController, BookController, Authorisation
from exceptions import MyException
from middlewares import AuthMiddleware, AddHeaderComponent
import falcon
from passlib.hash import sha256_crypt

middlewares = [
    AddHeaderComponent(),
    AuthMiddleware()
]

app = falcon.App(middleware=middlewares)

# app.add_route('/tests/', None)
app.add_route('/login/', Authorisation())
app.add_route('/books/', BooksController())
app.add_route('/books/{book_id}', BookController())

app.add_error_handler(MyException, MyException.handle)
