from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "URI database" 
app.secret_key = "secret-key"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'Users'
    username = db.Column(db.String(225), nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    cart = db.relationship('Cart', backref='user')

    def __init__(self, username, password, email):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email


class Products(db.Model):
    __tablename__ = 'Products'
    name = db.Column(db.String(255), nullable=False, primary_key=True)
    description = db.Column(db.String(1000))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    __tablename__ = 'Cart'
    user_username = db.Column(db.String(225), db.ForeignKey('Users.username'), primary_key=True)
    product_name = db.Column(db.String(255), db.ForeignKey('Products.name'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, user_username, product_name):
        self.user_username= user_username
        self.product_name = product_name

@app.route('/')
def index():
    products = Products.query.all()
    return render_template("index.html", products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user"] = username
            return redirect("/")
        return redirect("/login")
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm_password = request.form['confirmPassword']
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")
        if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
            return render_template("register.html", error="Username or email already exists")
        new_user = Users(username=username, password=generate_password_hash(password), email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route('/admin')
def admin():
    if session.get("admin", False):
        return render_template("admin.html")
    return redirect("/login")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/cart')
def cart():
    if session.get("user", False):
        user_username = session.get("user")
        carts = Cart.query.filter_by(user_username=user_username).all()
        products = []
        for cart in carts:
            user_product = Products.query.filter_by(name=cart.product_name).first()
            products.append((user_product, cart.quantity, round(user_product.price * cart.quantity, 2)))
        return render_template("cart.html", username=session.get("user", False), products=products)
    return redirect("/login")

@app.route('/add-cart', methods=["POST"])
def add_cart():
    if session.get("user", False):
        user_username = session.get("user")
        product_name = request.form['product_name']
        cart = Cart.query.filter_by(user_username=user_username, product_name=product_name).first()
        if cart:
            cart.quantity += 1
        else:
            new_cart = Cart(user_username=user_username, product_name=product_name)
            db.session.add(new_cart)
        db.session.commit()
        return redirect("/")
    return redirect("/login")

@app.route('/increase-cart', methods=["POST"])
def increase_cart():
    user_username = session.get("user")
    product_name = request.form['product_name']
    cart = Cart.query.filter_by(user_username=user_username, product_name=product_name).first()
    if cart.quantity > 0:
        cart.quantity += 1
    db.session.commit()
    return redirect("/cart")

@app.route('/decrease-cart', methods=["POST"])
def decrease_cart():
    user_username = session.get("user")
    product_name = request.form['product_name']
    cart = Cart.query.filter_by(user_username=user_username, product_name=product_name).first()
    if cart.quantity > 0:
        cart.quantity -= 1
    db.session.commit()
    return redirect("/cart")

@app.route('/remove-cart', methods=["POST"])
def remove_cart():
    user_username = session.get("user")
    product_name = request.form['product_name']
    cart = Cart.query.filter_by(user_username=user_username, product_name=product_name).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect("/cart")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run()
