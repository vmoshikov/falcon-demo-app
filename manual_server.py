from wsgiref.simple_server import make_server
from manage import app

if __name__ == '__main__':

    with make_server('localhost', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever(0.5)
Î