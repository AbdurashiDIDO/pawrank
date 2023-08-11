import sqlite3

from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from db import create_table
from image_insert import image_saver

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/media", StaticFiles(directory="media"), name="media")

connection = sqlite3.connect('facemash.db')
cursor = connection.cursor()


# create_table()
# image_saver()
# #
# print('Tables are create successfully and inserting images!')


@app.get("/", response_class=HTMLResponse)
async def get_results(request: Request):
    cursor.execute("SELECT * FROM images ORDER BY RANDOM() LIMIT 2")
    images = cursor.fetchmany(2)

    return templates.TemplateResponse("index.html",
                                      {"request": request, 'image1': images[0][1], 'image2': images[1][1]})


@app.post("/", response_class=HTMLResponse)
async def post_results(request: Request, image_1: str = Form(None), image_2: str = Form(None)):
    selected_image = image_1 if image_1 is not None else image_2

    cursor.execute("SELECT image_id FROM images WHERE image_url = ?", (selected_image,))
    res_id = cursor.fetchone()

    cursor.execute("SELECT ball FROM ranks WHERE image_id = ?", (res_id[0],))
    res_rank = cursor.fetchone()

    if res_rank is not None:
        ball = res_rank[0] + 1
        cursor.execute("UPDATE ranks SET ball = ? WHERE image_id = ?", (ball, res_id[0]))
    else:
        cursor.execute("INSERT INTO ranks (image_id, ball) VALUES (?, ?)", (res_id[0], 1))

    connection.commit()

    cursor.execute("SELECT image_url FROM images WHERE image_url != ? ORDER BY RANDOM() LIMIT 2",
                   (selected_image,))
    images = cursor.fetchall()

    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       'image1': image_1 if image_1 else images[0][0],
                                       'image2': image_2 if image_2 else images[1][0]})


@app.get("/rating", response_class=HTMLResponse)
async def get_rating(request: Request):
    cursor.execute("SELECT image_url FROM ranks INNER JOIN images ON ranks.image_id = images.image_id LIMIT 5")
    images = cursor.fetchall()

    return templates.TemplateResponse("rating.html",
                                      {"request": request, 'images': images})
