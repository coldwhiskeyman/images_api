import os
import threading

from flask import Flask, request, send_file
from flask_restful import Api, Resource, reqparse

from database import Image
from image_processing import process_image

UPLOAD_FOLDER = 'media'

app = Flask(__name__)
api = Api(app)


class Images(Resource):
    def get(self, img_id):
        file = Image.get(id=img_id)
        if not file:
            return {'message': 'Файл не найден'}, 404
        elif not file.complete:
            return {'message': 'Обработка файла не завершена'}
        else:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.delete()
            return send_file(path)

    def post(self):
        file = request.files.get('file')
        if not file:
            return {'message': 'Не найден файл для загрузки'}, 400
        else:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            img_id = Image.store_image(file.filename)
            threading.Thread(target=process_image, args=(img_id,)).start()
            return {
                        'message': 'Файл успешно загружен',
                        'img_id': img_id,
                   }, 201


api.add_resource(Images, '/images', '/images/<int:img_id>')


if __name__ == '__main__':
    app.run(debug=True)
