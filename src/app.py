import requests
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import Posts
from commands import restart_tables
from extensions import db,url_users,url_posts, queryempty, filter_results, extract_values
import json
import os

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath("../db.db")
app.jinja_env.globals.update(queryempty=queryempty)
app.cli.add_command(restart_tables)

# Initialization
db.init_app(app)


# Landing page
@app.route('/')
def home():
    return render_template('home.html')

# Page showing all posts
@app.route('/posts', methods=['GET','POST'])
def posts():

    APIposts = None
    DBposts = None
    postId = -1
    userId = -1
    postToEdit = -1

    # Getting External API data
    http_request = requests.get(url_posts)        
    json_input = http_request.json()

    # Retrieving information from form
    if request.form.get("filter_posts"):

        if (request.form["postId"]== ""):
            postId = -1
        else:
            postId = request.form["postId"]
        if (request.form["userId"] == ""):
            userId = -1
        else:
            userId = request.form["userId"]

        # Filtering required results
        APIposts,DBposts = filter_results(postId, userId, json_input, Posts)
    elif request.form.get("edit_button"):
        postToEdit, postId, userId = extract_values(request.form["edit_button"])
        APIposts,DBposts = filter_results(postId, userId, json_input, Posts)
    # Deleting a post
    elif request.form.get("delete_button"):
        post_to_delete, postId, userId = extract_values(request.form["delete_button"])
        # Deleting a post from database
        post = Posts.query.filter_by(id = int(post_to_delete)).first()
        db.session.delete(post)
        db.session.commit()
        # Retaining filtered results
        APIposts,DBposts = filter_results(postId, userId, json_input, Posts)
    elif request.form.get("confirm_button"):
        id_to_edit, postId, userId = extract_values(request.form["confirm_button"])
        post = Posts.query.filter_by(id = int(id_to_edit)).first()
        post.title = request.form["title"]
        post.body = request.form["body"]
        db.session.commit()
        APIposts,DBposts = filter_results(postId, userId, json_input, Posts)
        postToEdit = -1
    elif request.form.get("cancel_button"):
        postId, userId = extract_values(request.form["confirm_button"])
        APIposts,DBposts = filter_results(postId, userId, json_input, Posts)
        postToEdit = -1



    context = {
        'postToEdit' : postToEdit,
        'postID': postId,
        'userID': userId,
        'APIposts': APIposts,
        'DBposts': DBposts
    }

    return render_template('posts.html', **context)

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

if __name__ == "__main__":
    app.run(debug=True)
