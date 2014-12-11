from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    position = db.Column(db.String(250), nullable=True)
    qty = db.Column(db.Integer, nullable=False)

    def __init__(self, name, position, qty):
        self.name = name
        self.position = position
        self.qty = qty

@app.route('/')
@app.route('/<name>')
def welcome_page(name=None):
    return render_template('index.html', name=name)


@app.route('/product/all')
def view_list_products():
    admin = Item.query.all()
    return render_template('list_products.html', product=admin)


@app.route('/product/<pid>')
def view_product_by_id(pid):
    admin = Item.query.filter_by(id=pid).first()
    return render_template('show_product.html', product=admin)


@app.route('/product/add')
def add_product():
    return render_template('add_product.html')


if __name__ == '__main__':
    app.run()
