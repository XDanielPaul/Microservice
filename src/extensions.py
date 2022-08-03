from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
url_users = "https://jsonplaceholder.typicode.com/users"
url_posts = "https://jsonplaceholder.typicode.com/posts"

def extract_values(data):
    values = list(map(int, data.replace('\'', '')[1:-1].split(',')))
    return values

def filter_results(postId, userId, json_input, Posts):
    APIposts = []
    DBposts = None
    # If both fields are filled
    if postId != -1 and userId != -1:
        if not Posts.query.filter_by(userId = userId, id = postId).first():
            APIposts = [x for x in json_input if x['userId'] == int(userId) and x['id'] == int(postId)]
        else:
            DBposts = Posts.query.filter_by(userId = userId, id = postId)
    # If only userId is filled
    elif postId == -1 and userId != -1:
        if not Posts.query.filter_by(userId = userId).first():
            APIposts = [x for x in json_input if x['userId'] == int(userId)]
        else:
            # If we won't show posts from users in external API, 
            # they will be hidden through local database results and forever lost
            DBposts = Posts.query.filter_by(userId = userId)
            APIposts = [x for x in json_input if x['userId'] == int(userId)]
    # If only postID is filled
    elif postId != -1 and userId == -1:
        if not Posts.query.filter_by(id = postId).first():
            if int(postId) < 100:
                APIposts = [x for x in json_input if x['id'] == int(postId)]
                # Saving posts to database
                new_post = Posts(id = APIposts[0]['id'], userId=APIposts[0]['userId'], title=APIposts[0]['title'], body=APIposts[0]['body'])
                db.session.add(new_post)
                db.session.commit()
        else:
            DBposts = Posts.query.filter_by(id = postId)
    return APIposts, DBposts

# Jinja function checking whether query is empty
def queryempty(q):
    if (type(q) == list):
        return len(q) == 0
    elif (q == None):
        return True
    else:
        return q.first() is None