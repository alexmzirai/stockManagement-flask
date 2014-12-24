from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, logout_user, roles_accepted

app = Flask(__name__)
app.config['DEBUG'] = True
# Configure Flask-SQLAlchemy - sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///item.db'
# Secret key used for the session key
app.config['SECRET_KEY'] = 'super-secret'

app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = 'super-secret'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_POST_REGISTER_VIEW'] = '/'
app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/error'
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    position = db.Column(db.String(250), nullable=True)
    qty = db.Column(db.Integer, nullable=False)

    def __init__(self, name, position, qty):
        self.name = name
        self.position = position
        self.qty = qty


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
#@app.before_first_request
#def create_user():
#    db.create_all()
#    user_datastore.create_user(email='oformby', password='password')
#    user_datastore.create_role(name='admin', description='admin')
#    db.session.commit()


@app.route('/')
@app.route('/<name>')
def welcome_page(name="Flask Warehouse"):
    return render_template('index.html', name=name)


@app.route('/product/all')
def view_list_products():
    items = Item.query.all()
    return render_template('list_products.html', product=items)


@app.route('/product/<pid>')
def view_product_by_id(pid):
    admin = Item.query.filter_by(id=pid).first()
    return render_template('show_product.html', product=admin)


@app.route('/product/add')
@roles_accepted('admin')
def add_product():
    user_datastore.add_role_to_user(user='oformby', role='admin')
    db.session.commit()
    return render_template('add_product.html')


@app.route('/add/product', methods=['POST'])
@roles_accepted('admin')
def add_product_form():
    name = request.form['name']
    qty = request.form['qty']
    storage = request.form['storage']

    admin = Item(name, storage, qty)
    db.session.add(admin)
    db.session.commit()
    return render_template('add_product.html')


@app.route('/error')
def show_error_page():
    return render_template('error.html')


@app.route('/logout')
def user_logout():
    logout_user()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
