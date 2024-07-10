import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user = os.getenv("MYSQL_USER"), password = os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)

print(mydb)
# List of pages, update this list for dynamic page adding

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

pages = [
    {'name': 'Home', 'endpoint': 'index'},
    {'name': 'Hobbies', 'endpoint': 'hobbies'}
]

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    # Next step, create a specific hobbies file to read from
    hobbies_list = ['Reading', 'Hiking', 'Programming', 'Photography']
    hobbies_images = [
        './static/img/hobby1.jpg',
        './static/img/hobby1.jpg',
        './static/img/hobby1.jpg',
        './static/img/hobby1.jpg'
    ]
    return render_template('multi_items.html', title="Hobbies", items=hobbies_list, images=hobbies_images)


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.context_processor
def inject_pages():
    return dict(pages=pages)
