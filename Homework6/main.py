from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    date_ordered = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)


class ProductModel(BaseModel):
    name: str
    description: str
    price: float


class UserModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class OrderModel(BaseModel):
    user_id: int
    product_id: int
    date_ordered: str
    status: str


@app.route('/product', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return {'products': [product.__dict__ for product in products]}


@app.route('/product/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if product:
        return product.__dict__
    else:
        return {'message': 'Product not found.'}, 404


@app.route('/product', methods=['POST'])
def create_product():
    product = Product(**ProductModel(**request.json).dict())
    db.session.add(product)
    db.session.commit()
    return {'message': 'Product created successfully.'}, 201


@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        product_data = ProductModel(**request.json).dict(exclude_unset=True)
        for key, value in product_data.items():
            setattr(product, key, value)
        db.session.commit()
        return {'message': 'Product updated successfully.'}
    else:
        return {'message': 'Product not found.'}, 404


@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted successfully.'}
    else:
        return {'message': 'Product not found.'}, 404


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return {'users': [user.__dict__ for user in users]}


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user:
        return user.__dict__
    else:
        return {'message': 'User not found.'}, 404


@app.route('/user', methods=['POST'])
def create_user():
    user = User(**UserModel(**request.json).dict())
    db.session.add(user)
    db.session.commit()
    return {'message': 'User created successfully.'}, 201


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        user_data = UserModel(**request.json).dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user, key, value)
        db.session.commit()
        return {'message': 'User updated successfully.'}
    else:
        return {'message': 'User not found.'}, 404


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully.'}
    else:
        return {'message': 'User not found.'}, 404


@app.route('/order', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return {'orders': [order.__dict__ for order in orders]}


@app.route('/order/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = Order.query.get(order_id)
    if order:
        return order.__dict__
    else:
        return {'message': 'Order not found.'}, 404


@app.route('/order', methods=['POST'])
def create_order():
    order = Order(**OrderModel(**request.json).dict())
    db.session.add(order)
    db.session.commit()
    return {'message': 'Order created successfully.'}, 201


@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order_data = OrderModel(**request.json).dict(exclude_unset=True)
        for key, value in order_data.items():
            setattr(order, key, value)
        db.session.commit()
        return {'message': 'Order updated successfully.'}
    else:
        return {'message': 'Order not found.'}, 404


@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully.'}
    else:
        return {'message': 'Order not found.'}, 404


if __name__ == '__main__':
    app.run(debug=True)
