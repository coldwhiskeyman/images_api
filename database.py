import peewee
from flask_bcrypt import check_password_hash, generate_password_hash

db = peewee.SqliteDatabase('image_api.db')


class User(peewee.Model):
    email = peewee.CharField()
    password = peewee.CharField()

    class Meta:
        database = db

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Image(peewee.Model):
    filename = peewee.CharField()
    complete = peewee.BooleanField(default=False)
    uploaded_by = peewee.ForeignKeyField(User, backref='images')

    class Meta:
        database = db

    @staticmethod
    def store_image(filename, user):
        image = Image.create(filename=filename, uploaded_by=user)
        return image.id

    @staticmethod
    def process_complete(img_id):
        image = Image.get(id=img_id)
        image.complete = True
        image.save()


if __name__ == '__main__':
    db.create_tables([Image, User])
