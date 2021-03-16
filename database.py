import peewee

db = peewee.SqliteDatabase('image_api.db')


class Image(peewee.Model):
    filename = peewee.CharField()
    complete = peewee.BooleanField(default=False)

    class Meta:
        database = db

    @staticmethod
    def store_image(filename):
        image = Image.create(filename=filename)
        return image.id

    @staticmethod
    def process_complete(img_id):
        image = Image.get(id=img_id)
        image.complete = True
        image.save()


if __name__ == '__main__':
    db.create_tables([Image])
