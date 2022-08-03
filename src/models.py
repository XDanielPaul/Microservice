from extensions import db

i = 100
def mydefault():
    global i
    i += 1
    return i


class Posts(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, default=mydefault)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(100))
    body = db.Column(db.String(300))
