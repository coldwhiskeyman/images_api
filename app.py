import os
import threading

from flask import Flask, request, send_file
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt_identity, JWTManager, jwt_required
from flask_restful import Api, Resource

from auth import LoginApi, SignupApi
from database import Image, User
from image_processing import process_image

UPLOAD_FOLDER = 'media'
SECRET_KEY = 'SECRET_KEY'

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class Images(Resource):
    @jwt_required()
    def get(self, img_id):
        file = Image.get(id=img_id)
        user_id = get_jwt_identity()
        user = User.get(id=user_id)
        if not file:
            return {'message': 'Файл не найден'}, 404
        elif file.uploaded_by != user:
            return {'message': 'Информация о загруженных файлах доступно только загрузившим их пользователям'}, 403
        elif not file.complete:
            return {'message': 'Обработка файла не завершена'}
        else:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.delete()
            return send_file(path)

    @jwt_required()
    def post(self):
        file = request.files.get('file')
        if not file:
            return {'message': 'Не найден файл для загрузки'}, 400
        else:
            user_id = get_jwt_identity()
            user = User.get(id=user_id)
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            img_id = Image.store_image(file.filename, user)
            threading.Thread(target=process_image, args=(img_id,)).start()
            return {
                        'message': 'Файл успешно загружен',
                        'img_id': img_id,
                   }, 201


api.add_resource(Images, '/images', '/images/<int:img_id>')
api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')


if __name__ == '__main__':
    app.run(debug=True)
