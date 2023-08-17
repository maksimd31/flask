from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price})"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.first_name} {self.last_name}, email={self.email})"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, status={self.status})"


class ProductIn(BaseModel):
    name: str
    description: str
    price: float


class ProductOut(BaseModel):
    id: int
    name: str
    description: str
    price: float


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str


# Create
@app.route('/products', methods=['POST'])
def create_product():
    product = Product(**ProductIn(**request.json).dict())
    db.session.add(product)
    db.session.commit()
    return ProductOut(**product.__dict__).json()


@app.route('/users', methods=['POST'])
def create_user():
    user = User(**UserIn(**request.json).dict())
    db.session.add(user)
    db.session.commit()
    return UserOut(**user.__dict__).json()


@app.route('/orders', methods=['POST'])
def create_order():
    order = Order(**OrderIn(**request.json).dict())
    db.session.add(order)
    db.session.commit()
    return OrderOut(**order.__dict__).json()


# Read
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return [ProductOut(**product.__dict__).dict() for product in products]


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return [UserOut(**user.__dict__).dict() for user in users]


@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return [OrderOut(**order.__dict__).dict() for order in orders]


# Update
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    product_data = ProductIn(**request.json).dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product, key, value)
    db.session.commit()
    return ProductOut(**product.__dict__).json()


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    user_data = UserIn(**request.json).dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.session.commit()
    return UserOut(**user.__dict__).json()


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get(order_id)
    order_data = OrderIn(**request.json).dict(exclude_unset=True)
    for key, value in order_data.items():
        setattr(order, key, value)
    db.session.commit()
    return OrderOut(**order.__dict__).json()


# Delete
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return {'message': 'Product successfully deleted'}


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return {'message': 'User successfully deleted'}


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    db.session.delete(order)
    db.session.commit()
    return {'message': 'Order successfully deleted'}


if __name__ == '__main__':
    app.run(debug=True)

'''
Этот код описывает соединение с базой данных SQLite, содержащей три таблицы: Product, User и Order. 
API поддерживает следующие операции CRUD для каждой из таблиц: создание записи (Create), 
чтение записи (Read), обновление записи (Update) и удаление записи (Delete).

Чтобы запустить API, необходимо запустить файл. При этом сервер будет запущен в режиме отладки. 
Далее, можно выполнять запросы к API, используя утилиту curl или любой другой инструмент, 
поддерживающий RESTful API.

Примеры запросов:
- Создание продукта:
    ```python
    curl -X POST -H "Content-Type: application/json" --data '{"name":"Product 1", 
    "description":"Description 1", "price":10.0}' <http://localhost:5000/products>
    ```
- Получение всех пользователей: 
    ```python
    curl -X GET <http://localhost:5000/users>
    ```
- Обновление заказа:
    ```python
    curl -X PUT -H "Content-Type: application/json" --data '{"status":"delivered"}' 
    <http://localhost:5000/orders/1>
    ```  
- Удаление пользователя:
    ```python
    curl -X DELETE <http://localhost:5000/users/1>
    ```
'''