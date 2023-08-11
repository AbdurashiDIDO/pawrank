import sqlite3

connection = sqlite3.connect('pawrank.db')
cursor = connection.cursor()


# Example: Create a new table
def create_table():
    create_table_image = '''
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY,
            image_url TEXT NOT NULL
        )
    '''

    cursor.execute(create_table_image)

    create_table_rank = '''
            CREATE TABLE IF NOT EXISTS ranks (
                rank_id INTEGER PRIMARY KEY,
                image_id INTEGER NOT NULL,
                ball INTEGER NOT NULL,
                CONSTRAINT fk_image  
                FOREIGN KEY (image_id) REFERENCES image (image_id) 
            )
        '''

    cursor.execute(create_table_rank)

    connection.commit()
