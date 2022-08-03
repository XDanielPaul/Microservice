import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import Posts
from commands import restart_tables
from extensions import db,url_users,url_posts
import json

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C://Users//danko//Desktop//School//Python//MicroserviceAPI//Microservice//db.db'

# Initialization
db.init_app(app)
app.cli.add_command(restart_tables)
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

        # Getting External API data
        http_request = requests.get(url_posts)        
        json_input = http_request.json()

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
                # If we won't show posts from users in external API, 
                # they will be hidden through local database results and forever lost
                dbposts = Posts.query.filter_by(userId = userId)
                posts = [x for x in json_input if x['userId'] == int(userId)]
                for dbpost in dbposts:
                    posts.append({"userId": dbpost.userId, "id": dbpost.id, "title": dbpost.title, "body": dbpost.body})
        # If only postID is filled
        elif postId != "" and userId == "":
            if not Posts.query.filter_by(id = postId).first():
                posts = [x for x in json_input if x['id'] == int(postId)]
                # Saving posts to database
                new_post = Posts(userId=posts[0]['userId'], title=posts[0]['title'], body=posts[0]['body'])
                db.session.add(new_post)
                db.session.commit()

    return render_template('posts.html', posts = posts)

# Page for adding a new post
@app.route('/add_post', methods=['GET','POST'])
def add_post():

    user_found = 0
    # Add post to the database
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        userId = request.form["userId"]

        # Getting external API data
        http_request = requests.get(url_users)        
        json_input = http_request.json()

        # If userId exists in recieved data from external API, create a new post
        if [x for x in json_input if x['id'] == int(userId)]:
            new_post = Posts(userId=userId, title=title, body=body)
            db.session.add(new_post)
            db.session.commit()
            user_found = 1
        else:
            user_found = 2

        

    return render_template('add_post.html', user_found = user_found)


