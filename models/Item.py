from stockManagement import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    position = db.Column(db.String(250), nullable=True)
    qty = db.Column(db.Integer, nullable=False)

    def __init__(self, name, position, qty):
        self.name = name
        self.position = position
        self.qty = qty