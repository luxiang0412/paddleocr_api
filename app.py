import json

import tornado.ioloop
import tornado.web
from paddleocr import PaddleOCR

class OCRSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PaddleOCR(use_angle_cls=True, lang="ch")
        return cls._instance

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("")


class OcrHandler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json")
        files = self.request.files
        file_list = files.get("file")
        if file_list is None:
            self.set_status(400)
            json_string = json.dumps({"code": "file.not.null", "message": "file not null"})
            self.write(json_string)
            return
        file_obj = files.get("file")[0]
        if file_obj:
            filename = file_obj["filename"]
            print("filename: ", filename)
            bytes = file_obj["body"]
            ocr = OCRSingleton.get_instance()
            result = ocr.ocr(bytes, cls=True)
            json_string = json.dumps(result)
            self.write(json_string)
        else:
            self.set_status(400)
            json_string = json.dumps({"code": "file.not.null", "message": "file not null"})
            self.write(json_string)

app = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/api/ocr", OcrHandler),
])

if __name__ == "__main__":
    app.listen(8867)
    tornado.ioloop.IOLoop.current().start()