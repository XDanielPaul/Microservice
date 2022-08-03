import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import Posts
from extensions import db,url_users,url_posts
import json

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C://Users//danko//Desktop//School//Python//MicroserviceAPI//Microservice//db.db'

# Initialization
db.init_app(app)
app.run(debug=True)

#with app.app_context():
#    db.create_all()

# Jinja function checking whether query is empty
def queryempty(q):
    if (type(q) == list):
        return len(q) == 0
    else:
        return q.first() is None
app.jinja_env.globals.update(queryempty=queryempty)

# Landing page
@app.route('/')
def home():
    return render_template('home.html')

# Page showing all posts
@app.route('/posts', methods=['GET','POST'])
def posts():
    posts = None
    # Retrieving information from form
    if request.form.get("filter_posts"):
        postId = request.form["postId"]
        userId = request.form["userId"]
        http_request = requests.get(url_posts)        
        json_input = http_request.json()#json.loads(http_request)

        # Filtering required results

        # If both fields are filled
        if postId != "" and userId != "":
            if not Posts.query.filter_by(userId = userId, id = postId).first():
                posts = [x for x in json_input if x['userId'] == int(userId) and x['id'] == int(postId)]
            else:
                posts = Posts.query.filter_by(userId = userId, id = postId)
        # If only userId is filled
        elif postId == "" and userId != "":
            if not Posts.query.filter_by(userId = userId).first():
                posts = [x for x in json_input if x['userId'] == int(userId)]
            else:
                posts = Posts.query.filter_by(userId = userId)
        # If only postID is filled
        elif postId != "" and userId == "":
            if not Posts.query.filter_by(id = postId).first():
                posts = [x for x in json_input if x['id'] == int(postId)]
            else:
                # TODO: PRIDAJ AJ PRISPEVKY Z API
                posts = Posts.query.filter_by(id = postId)
        # If none of the fields are filled, show all posts
        else:
            posts = Posts.query.all()

    return render_template('posts.html', posts = posts)

# Page for adding a new post
@app.route('/add_post', methods=['GET','POST'])
def add_post():

    # Add post to the database
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        new_post = Posts(userId=0, title=title, body=body)
        db.session.add(new_post)
        db.session.commit()

    return render_template('add_post.html')


