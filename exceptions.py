import json
import falcon


class MyException(Exception):
    @staticmethod
    def handle(req, resp, exc, params):
        resp.set_header("X-Custom-Header", "Error")
        resp.status = falcon.HTTP_502
        resp.text = json.dumps({"message": "My custom error"})
