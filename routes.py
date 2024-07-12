from flask import render_template, redirect, session
from extensions import app, db, login_manager, login_user, current_user, logout_user
from forms import AddProduct, LogIn, Register, AddOffer
import os
from models import Product, Offer, User, ProductCategory
from werkzeug.security import generate_password_hash, check_password_hash

def get_cart_items():
 return session.get('cart', []) 
    
@app.route("/")
def home():
    cart_items = len(get_cart_items())
    return render_template("home.html", products = Product.query.all(), offers = Offer.query.all(), cart_items=cart_items)

@app.route("/products/<int:category_id>")
@app.route("/products")
def products(category_id):
    if category_id:
        products = ProductCategory.query.get(category_id).products
    return render_template("products.html", products = products)

@app.route("/about_us")
def about():
    return render_template("about_us.html")


@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html", id=product_id)

    return render_template("product.html", product=product)

@app.route("/offer/<int:offer_id>")
def offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return render_template("404.html", id=offer_id)

    return render_template("offer.html", offer=offer)


@app.route("/add_product", methods = ["POST", "GET"])
def add_product():
        form = AddProduct()

        if form.validate_on_submit():
            new_product = Product(
                                  name=form.name.data,
                                  image_url=form.image_url.data,
                                  price=form.price.data,
                                  text=form.text.data,
                                  category_id = form.category_id.data
                                )
            db.session.add(new_product)
            db.session.commit()

            return redirect("/")

        else:
            print(form.errors)
        return render_template("add_product.html", form=form)

@app.route("/add_offer", methods = ["POST", "GET"])
def add_offer():
        form = AddOffer()

        if form.validate_on_submit():
            new_offer = Offer(name=form.name.data, image_url=form.image_url.data, price=form.price.data, text=form.text.data)
            db.session.add(new_offer)
            db.session.commit()

            return redirect("/")

        else:
            print(form.errors)
        return render_template("add_offer.html", form=form)


@app.route("/edit_offer/<int:offer_id>", methods=['POST', 'GET'])
def edit_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return render_template("404.html")
    form = AddOffer(name=offer.name, text=offer.text, image_url=offer.image_url, price=offer.price)
    if form.validate_on_submit():

        offer.name = form.name.data
        offer.price = form.price.data
        offer.text = form.text.data
        offer.image_url = form.image_url.data

        db.session.commit()

        return redirect("/")

    return render_template("edit_offer.html", form=form)

@app.route("/edit_product/<int:product_id>", methods=['POST', 'GET'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")
    form = AddProduct(name=product.name,
                      text=product.text,
                      image_url=product.image_url,
                      price=product.price,
                      category_id=product.category_id
                      )
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.text = form.text.data
        product.image_url = form.image_url.data
        product.category_id = form.category_id.data

        db.session.commit()

        return redirect("/")

    return render_template("edit_product.html", form=form)


@app.route("/delete_product/<int:product_id>", methods=['GET', 'DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")

    db.session.delete(product)
    db.session.commit()

    return redirect("/")

@app.route("/delete_offer/<int:offer_id>", methods=['GET', 'DELETE'])
def delete_offer(offer_id):
    offer = Offer.query.get(offer_id)
    if not offer:
        return render_template("404.html")

    db.session.delete(offer)
    db.session.commit()

    return redirect("/")


@app.route("/register", methods = ['POST', 'GET'])
def register():

    form = Register()

    if form.validate_on_submit():
        new_user = User(
                        username = form.username.data,
                        email = form.email.data,
                        password  = generate_password_hash(form.password.data)
                        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect("/")

    return render_template("register.html", form=form)

@app.route("/login", methods = ['Post', 'GET'])
def login():

    form = LogIn()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        else:
            print(form.errors)

    return render_template("login.html", form=form)

@app.route("/logout", methods = ['Post', 'GET'])
def logout():
    logout_user()
    return redirect("/")

@app.route("/search/<string:product_name>")
def search(product_name):
    products = Product.query.filter(Product.name.ilike(f"%{product_name}%")).all()

    return render_template("search_results.html", products=products)

@app.route("/cart")
def cart():
 cart_product_ids = get_cart_items()
 length = len(cart_product_ids)
 if cart_product_ids:
     products = Product.query.filter(Product.id.in_(cart_product_ids)).all()
 else:
     products = []
 return render_template('cart.html', products=products, cart_items=length)

@app.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
def add_to_cart(item_id):
 cart = session.get('cart', [])
 cart.append(item_id)
 session['cart'] = cart
 return redirect("/")

@app.route('/remove_from_cart/<int:item_id>')
def remove_from_cart(item_id):
 cart = session.get('cart', [])
 if item_id in cart:
     cart.remove(item_id)
     session['cart'] = cart
 return redirect("/cart")
    
@app.route("/success")
def success():
    return render_template("success.html")






