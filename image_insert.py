from glob import glob

from db import cursor, connection

your_path = 'media'

ext = ['*.jpg', '*.png']


def image_saver():
    images = []
    for item in [your_path + '/' + e for e in ext]:
        images += glob(item)

    insert_image_query = """ INSERT INTO images
                                     (image_url) VALUES (?)"""

    for image in images:
        if image not in [i[0] for i in cursor.execute('SELECT image_url FROM images')]:
            cursor.execute(insert_image_query, (image,))
        else:
            continue

    connection.commit()
    connection.close()

