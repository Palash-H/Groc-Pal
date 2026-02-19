from flask import Flask, render_template, request, redirect, url_for
from flask import flash, session
from models import db, User, Product, Cart, Category, Order, Transaction
from functools import wraps
import datetime

from flask import Blueprint

bprint = Blueprint("main", __name__)

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to login first to continue")
            return redirect(url_for('main.login'))
        return func(*args, **kwargs)
    return inner

def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to login first to continue")
            return redirect(url_for('main.login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash('You are not authorized to make changes!')
            return redirect(url_for('main.homepage'))
        return func(*args, **kwargs)
    return inner

# @bprint.route("/")
# @auth_required
# def home():
#     return render_template('home.html', user = User.query.get(session['user_id']))




@bprint.route("/admin")
@admin_required
def admindash():
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('You are not authorized to view this page, redirecting you to dashboard')
        return redirect(url_for('main.homepage'))
    return render_template("admin_dash.html", user = user, categories = Category.query.all())

@bprint.route("/login")
def login():
    return render_template("login.html")

@bprint.route('/login', methods = ["POST"])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        flash("Username or password is needed for login!")
        return redirect(url_for('main.login'))
    user = User.query.filter_by(username = username).first()
    if not user:
        flash('User is not registered!')
        return redirect(url_for('main.login'))
    if not user.check_password(password):
        flash("Password is incorrect!")
        return redirect(url_for('main.login'))
    session['user_id']  = user.id
    return redirect(url_for('main.homepage'))

@bprint.route("/register")
def register():
    return render_template("register.html")

@bprint.route("/register", methods = ['POST'])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    if username == '' or password == '':
        flash('Username or Password cannot be Empty!')
        return redirect(url_for('main.register'))
    if User.query.filter_by(username = username).first():
        flash("User already exists!, Login to access")
        return redirect(url_for('main.register'))
    user = User(username = username, password = password, name = name)
    db.session.add(user)
    db.session.commit()
    flash("User Successfully registered, Welcome aboard")
    return redirect(url_for('main.login'))

@bprint.route("/logout")
def logout():
    session.clear()
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('main.login'))


@bprint.route('/profile')
@auth_required
def profile():

    return render_template('profile.html', user = User.query.get(session['user_id']))

@bprint.route('/profile', methods = ["POST"])
@auth_required
def profile_post():
    user = User.query.get(session['user_id'])
    username = request.form.get('username')
    name = request.form.get('name')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    if username == '' or password == '' or cpassword == '':
        flash('Username or Password cannot be Empty.')
        return redirect(url_for('main.profile'))
    if not user.check_password(cpassword):
        flash('Incorrect Password')
        return redirect(url_for('main.profile'))
    if User.query.filter_by(username = username).first() and username != user.username:
        flash("Username already taken, try another.")
        return redirect(url_for('main.profile'))
    
    user.username = username
    user.name = name
    user.password = password


    db.session.commit()
    flash('Profile is updated successfully')
    return redirect(url_for('main.profile'))

@bprint.route("/")
@auth_required
def homepage():
    user = User.query.get(session['user_id'])
    categories = Category.query.all()
    if user.is_admin:
        return redirect(url_for('main.admindash'))
        # return redirect(url_for('main.admin'))
    else:
        parameter = request.args.get("parameter")
        query = request.args.get('query')
        parameters = {
            'category':'Category Name',
            'product':'Product Name',
            'price':'Max Price'
        }
        if not parameter or not query:    
            return render_template("index.html", user = user, categories = categories, parameters = parameters)
        if parameter=="category":
            categories = Category.query.filter(Category.name.ilike('%'+ query + '%')).all()
            return render_template('index.html', user = user, categories = categories, query = query, parameter=parameter, parameters=parameters)
        if parameter=="product":
            return render_template('index.html', user = user, categories = Category.query.all(), name = query, query = query, parameter=parameter, parameters=parameters)
        if parameter=="price":
            return render_template('index.html', user = user, categories = Category.query.all(), price = float(query), query = query, parameter=parameter, parameters=parameters)
    return render_template('index.html', user = user, categories = Category.query.all(), parameters = parameters)

    
# Add to cart newly added

@bprint.route('/cart/<int:product_id>/add', methods = ["POST"])
@auth_required
def add_to_cart(product_id):
    quantity = request.form.get('quantity')
    if not quantity or quantity=='':
        flash('Quantity cannot be empty.')
        return(redirect(url_for('main.homepage')))
    if quantity.isdigit()==False:
        flash('Quantity must be a number')
        return (redirect(url_for('main.homepage')))
    quantity=int(quantity)
    if quantity<=0:
        flash('Quantity must be greater than 0')
        return (redirect(url_for('main.homepage')))
    product = Product.query.get(product_id)
    if not product:
        flash('Product does not exist')
        return (redirect(url_for('main.homepage')))
    if product.quantity< quantity:
        flash('Quantity must be less than or equal to ' + str(product.quantity)+'.')
        return(redirect(url_for('main.homepage')))
    cart =  Cart.query.filter_by(user_id = session['user_id']).filter_by(product_id = product_id).first()
    if cart:
        if cart.quantity+quantity> product.quantity:
            flash('Quantity must be less than or equal to '+ str(product.quantity-cart.quantity) + '.')
            return (redirect(url_for('main.homepage')))
        cart.quantity+=quantity
        db.session.commit()
        flash('Product added to Cart Successfully!')
        return (redirect(url_for('main.homepage')))
    cart = Cart(user_id = session['user_id'], product_id =product_id, quantity = quantity)
    db.session.add(cart)
    db.session.commit()
    flash('Product Added to cart Successfully.')
    return redirect(url_for('main.homepage'))


    # return "add to cart for product id: "+ str(product_id) + " quantity: "+ str(quantity)


@bprint.route("/cart")
@auth_required
def cart():
    carts = Cart.query.filter_by(user_id = session['user_id']).all()
    total = sum([c.product.price*c.quantity for c in carts])
    return render_template('cart.html', user = User.query.get(session['user_id']), carts = carts, total = total)


@bprint.route('/cart/<int:product_id>/delete', methods = ["POST"])
@auth_required
def delete_from_cart(product_id):
    cart = Cart.query.filter_by(user_id = session['user_id']).filter_by(product_id=product_id).first()
    if not cart:
        flash('Product does not exist in the cart')
        return redirect(url_for('main.cart'))
    db.session.delete(cart)
    db.session.commit()
    flash('Product successfully deleted from the cart.')
    return redirect(url_for('main.cart'))



@bprint.route('/categories/add')
@admin_required
def add_categories():
    return render_template("/category/add.html", user = User.query.get(session['user_id']))

@bprint.route('/categories/add', methods = ["POST"])
@admin_required
def add_categories_post():
    name = request.form.get('name')
    
    if name == '':
        flash('Name cannot be Empty')
        return redirect(url_for('main.add_categories'))
    if Category.query.filter_by(name = name).first():
        flash('Category Already Exists!')
        return redirect(url_for('main.admindash'))
    if len(name)>64:
        flash('Cannot be greater than 64 characters.')
        return redirect(url_for('main.add_categories'))
    category = Category(name = name)
    db.session.add(category)
    db.session.commit()
    flash('Category Added Successfully.')
    return redirect(url_for('main.admindash'))


@bprint.route('/categories/<int:id>/details')
@admin_required
def show_category(id):
    category = Category.query.get(id)
    return render_template('category/show.html', user = User.query.get(session['user_id']), category = Category.query.get(id))



@bprint.route('/product/add')
@admin_required
def add_product():
    catid = -1
    args = request.args
    if 'catid' in args:
        if Category.query.get(int(args.get('catid'))):
            catid = int(args.get('catid'))


    # category = Category.query.get(id)
    return render_template('/product/add.html',
                           user = User.query.get(session['user_id']), 
                           catid = catid,
                           categories = Category.query.all(),
                           now = datetime.datetime.now().strftime("%Y-%m-%d"))

import re
@bprint.route('/product/add', methods = ["POST"])
@admin_required
def add_product_post():
    name = request.form.get('name')
    price = request.form.get('price')
    category = request.form.get('category')
    quantity = request.form.get('quantity')
    man_date = request.form.get('manufacture_date')
    if name =='':
        flash('Name cannot be empty!')
        return redirect(url_for('main.add_product'))
    if len(name)>64:
        flash('Name cannot exceed 64 chars')
        return redirect(url_for('main.add_product'))
    if quantity =='' :
        flash('Quantity cannot be empty ')
        return redirect(url_for('main.add_product'))
    if quantity.isdigit()== False:
        flash('Quantity must be a number')
        return redirect(url_for('main.add_product'))
    quantity= int(quantity)

    if price =='':
        flash('Price cannot be empty')
        return redirect(url_for('main.add_product'))
    if not re.match(r'^\d+(\.\d+)?$', price):
        flash('Price must be a number')
        return redirect(url_for('main.add_product'))
    price = float(price)
    if category== '':
        flash('Category cannot be empty!')
        return redirect(url_for('main.add_product'))
    category = Category.query.get(category)
    if not category:
        flash('Category does not exist.')
        return redirect(url_for('main.add_product'))
    if man_date == '':
        flash('Manufacture date cannot be empty')
        return redirect(url_for('main.add_product'))
    try:
        man_date = datetime.datetime.strptime(man_date, '%Y-%m-%d')
    except ValueError:
        flash('Invalid Manufacture Date')
        return redirect(url_for('main.add_product'))
    product = Product(name=name, quantity=quantity,price=price,category = category, man_date =man_date)
    db.session.add(product)
    db.session.commit()
    flash('Product Added Successfully')
    return redirect(url_for('main.show_category', id = category.id))

    
    


@bprint.route('/product/<int:id>/edit')
@admin_required
def edit_product(id):
    product = Product.query.get(id)
    return render_template('/product/edit.html', user = User.query.get(session['user_id']),
                           product = Product.query.get(id),
                           categories = Category.query.all(),
                           now = datetime.datetime.now().strftime("%Y-%m-%d"),
                           manufacture_date = product.man_date.strftime("%Y-%m-%d")
                           )

@bprint.route('/product/<int:id>/edit', methods = ["POST"])
@admin_required
def edit_product_post(id):
    name = request.form.get('name')
    price = request.form.get('price')
    category = request.form.get('category')
    quantity = request.form.get('quantity')
    man_date = request.form.get('manufacture_date')
    if name =='':
        flash('Name cannot be empty!')
        return redirect(url_for('main.add_product'))
    if len(name)>64:
        flash('Name cannot exceed 64 chars')
        return redirect(url_for('main.add_product'))
    if quantity =='' :
        flash('Quantity cannot be empty ')
        return redirect(url_for('main.add_product'))
    if quantity.isdigit()== False:
        flash('Quantity must be a number')
        return redirect(url_for('main.add_product'))
    quantity= int(quantity)

    if price =='':
        flash('Price cannot be empty')
        return redirect(url_for('main.add_product'))
    if not re.match(r'^\d+(\.\d+)?$', price):
        flash('Price must be a number')
        return redirect(url_for('main.add_product'))
    price = float(price)
    if category== '':
        flash('Category cannot be empty!')
        return redirect(url_for('main.add_product'))
    category = Category.query.get(category)
    if not category:
        flash('Category does not exist.')
        return redirect(url_for('main.add_product'))
    if man_date == '':
        flash('Manufacture date cannot be empty')
        return redirect(url_for('main.add_product'))
    try:
        man_date = datetime.datetime.strptime(man_date, '%Y-%m-%d')
    except ValueError:
        flash('Invalid Manufacture Date')
        return redirect(url_for('main.add_product'))
    product = Product.query.get(id)
    product.name = name
    product.quantity = quantity
    product.price = price
    product.category = category
    product.man_date = man_date
    db.session.commit()
    flash('Product Updated Successfully')
    return redirect(url_for('main.show_category', id = category.id))


@bprint.route('/product/<int:id>/delete')
@admin_required
def delete_product(id):
    # category = Category.query.get(id)
    product = Product.query.get(id)
    if not product:
        flash('Product does not exist!')
        return redirect(url_for('main.admindash'))
    
    return render_template('/product/delete.html', user = User.query.get(session['user_id']), product = product)

@bprint.route('/product/<int:id>/delete', methods = ["POST"])
@admin_required
def delete_product_post(id):
    # category = Category.query.get(id)
    product = Product.query.get(id)
    if not product:
        flash('Product does not exist!')
        return redirect(url_for('main.admindash'))
    db.session.delete(product)
    db.session.commit()
    flash('Product Deleted Successfully')
    return redirect(url_for('main.admindash'))


@bprint.route('/categories/<int:id>/edit')
@admin_required
def edit_category(id):
    return render_template('/category/edit.html', user = User.query.get(session['user_id']), category = Category.query.get(id))

@bprint.route('/categories/<int:id>/edit', methods = ["POST"])
@admin_required
def edit_category_post(id):
    category = Category.query.get(id)
    name = request.form.get('name')
    if name == '':
        flash('Category name cannot be empty.')
        return redirect(url_for('main.edit_category', id = id))
    if len(name)> 64:
        flash('Category name should be under 64 chars')
        return redirect(url_for('main.edit_category', id = id))
    category.name = name
    db.session.commit()
    flash('Category updated successfully.')
    return redirect(url_for('main.admindash'))


@bprint.route('/categories/<int:id>/delete')
@admin_required
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        flash('Category does not exist!')
        return redirect(url_for('main.admindash'))
    return render_template('category/delete.html', user = User.query.get(session['user_id']), category = category)

@bprint.route('/categories/<int:id>/delete', methods = ["POST"])
@admin_required
def delete_category_post(id):
    category = Category.query.get(id)
    if not category:
        flash('Category does not exist!')
        return redirect(url_for('main.admindash'))
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully')
    return redirect(url_for('main.admindash'))

@bprint.route('/cart/checkout', methods = ["POST"])
@auth_required
def place_order():
    items = Cart.query.filter_by(user_id = session['user_id']).all()
    if not items:
        flash('Cart is Empty')
        return redirect(url_for('main.cart'))
    for item in items:
        if item.quantity> item.product.quantity:
            flash('Quantity of '+ item.product.name + 'must be less than or equal to '+ str(item.product.quantity + "."))
            return redirect(url_for('main.cart'))
    transaction = Transaction(user_id = session['user_id'], total = 0)
    for item in items:
        item.product.quantity -= item.quantity
        order = Order(product_id = item.product_id, quantity = item.quantity, price = item.product.price, transaction = transaction)
        db.session.add(order)
        transaction.orders.append(order)
        transaction.total += order.price * order.quantity
        db.session.delete(item)
        db.session.commit()
    flash('Order placed successfully')
    return redirect(url_for('main.orders'))
    
@bprint.route("/orders")
@auth_required
def orders():
    user = User.query.get(session['user_id'])
    transactions = Transaction.query.filter_by(user_id = session['user_id']).order_by(Transaction.datetime.desc()).all()
    # total = sum([transaction])
    return render_template('orders.html', user = user, transactions = transactions)