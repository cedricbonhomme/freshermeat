
from bootstrap import db

class User_Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.String(100))
    type = db.Column(db.String(100))

    def __repr__(self):
        return '<Name %r>' % (self.name)

    def __eq__(self, other):
        return self.name == other.name
