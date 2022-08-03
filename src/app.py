import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import Posts
from extensions import db,url_users,url_posts

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C://Users//danko//Desktop//School//Python//MicroserviceAPI//Microservice//db.db'

# Initialization
db.init_app(app)
app.run(debug=True)

#with app.app_context():
#    db.create_all()

# Landing page
@app.route('/')
def home():
    return render_template('home.html')

# Page showing all posts
@app.route('/posts')
def posts():
    response = requests.get(url_posts)
    return render_template('posts.html', posts = response.json())

# Add a new post
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


