import os

from flask import Flask, request, send_file
from flask_restful import Api, Resource

from image_processing import FILES_IN_WORK, process_image

UPLOAD_FOLDER = 'media'

app = Flask(__name__)
api = Api(app)


class Images(Resource):
    def get(self, filename):
        if filename not in FILES_IN_WORK:
            return {'message': 'Файл не найден'}, 404
        elif not FILES_IN_WORK[filename]:
            return {'message': 'Обработка файла не завершена'}
        else:
            path = os.path.join(UPLOAD_FOLDER, filename)
            return send_file(path)

    def post(self):
        file = request.files.get('file')
        if not file:
            return {'message': 'Не найден файл для загрузки'}, 400
        else:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            return {'message': 'Файл успешно загружен'}, 201


api.add_resource(Images, '/images', '/images/<filename>')


if __name__ == '__main__':
    app.run(debug=True)
