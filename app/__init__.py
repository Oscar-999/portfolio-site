import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from hashlib import md5

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in testing mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )
    
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
    {'name': 'Timeline', 'endpoint': 'timeline'},
    {'name': 'Hobbies', 'endpoint': 'hobbies'}
]

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

app.route('/')

@app.route('/timeline')
def timeline():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        timeline_post = TimelinePost.create(name=name, email=email, content=content)
        return model_to_dict(timeline_post)
    else:
        timeline_posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        return render_template('timeline.html', title="Timeline", timeline_posts=timeline_posts, pages=pages)


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

@app.route('/api/timeline_post/<int:id>', methods=['DELETE'])
def delete_post(id):
    timeline_post = TimelinePost.get(TimelinePost.id == id)
    timeline_post.delete_instance()
    return jsonify({'status': 'success', 'message': 'Post deleted successfully.'})

app.jinja_env.filters['md5'] = lambda x: md5(x.encode('utf-8')).hexdigest()

@app.context_processor
def inject_pages():
    return dict(pages=pages)
