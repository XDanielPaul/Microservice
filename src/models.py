from extensions import db

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String(100))
    body = db.Column(db.String(300))
