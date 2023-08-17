# filename hm6
# from email_valedator import validate_email, EmailNotValidError
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, EmailStr, validator, ValidationError
# from email_validator import validate_email, EmailNotValidError
from typing import List

app = FastAPI()


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    order_status: str


# Таблица товаров
products_db = [
    Product(id=1, name='Товар 1', description='Описание товара 1', price=100),
    Product(id=2, name='Товар 2', description='Описание товара 2', price=200),
    Product(id=3, name='Товар 3', description='Описание товара 3', price=300),
]

# Таблица пользователей
users_db = [
    User(id=1, first_name='Иван', last_name='Иванов', email='ivan@mail.com', password='password1'),
    User(id=2, first_name='Петр', last_name='Петров', email='petr@mail.com', password='password2'),
    User(id=3, first_name='Сидор', last_name='Сидоров', email='sidor@mail.com', password='password3'),
]

# Таблица заказов
orders_db = [
    Order(id=1, user_id=1, product_id=1, order_date='2021-09-01', order_status='В процессе'),
    Order(id=2, user_id=2, product_id=2, order_date='2021-09-02', order_status='Выполнен'),
    Order(id=3, user_id=3, product_id=3, order_date='2021-09-03', order_status='Отменен'),
]


# Модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц
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
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    order_status: str


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    order_status: str


# CRUD операции для каждой из таблиц через создание маршрутов, REST API

# Таблица "Товары"
# Чтение всех
@app.get("/products", response_model=List[ProductOut])
def get_products():
    return products_db


# Чтение одного
@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int):
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


# Запись
@app.post("/products", response_model=ProductOut)
def add_product(product: ProductIn):
    new_product = Product(id=len(products_db) + 1, **product.dict())
    products_db.append(new_product)
    return new_product


# Изменение
@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductIn):
    for i, p in enumerate(products_db):
        if p.id == product_id:
            products_db[i] = Product(id=product_id, **product.dict())
            return products_db[i]
    raise HTTPException(status_code=404, detail="Product not found")


# Удаление
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i, product in enumerate(products_db):
        if product.id == product_id:
            products_db.pop(i)
            return {"message": "Product deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")


# Таблица "Пользователи"
# Чтение всех
@app.get("/users", response_model=List[UserOut])
def get_users():
    return users_db


# Чтение одного
@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


# Запись
@app.post("/users", response_model=UserOut)
def add_user(user: UserIn):
    new_user = User(id=len(users_db) + 1, **user.dict())
    users_db.append(new_user)
    return new_user


# Изменение
@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserIn):
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db[i] = User(id=user_id, **user.dict())
            return users_db[i]
    raise HTTPException(status_code=404, detail="User not found")


# Удаление
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(i)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")


# Таблица "Заказы"
# Чтение всех
@app.get("/orders", response_model=List[OrderOut])
def get_orders():
    return orders_db


# Чтение одного
@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int):
    for order in orders_db:
        if order.id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


# Запись
@app.post("/orders", response_model=OrderOut)
def add_order(order: OrderIn):
    new_order = Order(id=len(orders_db) + 1, **order.dict())
    orders_db.append(new_order)
    return new_order


# Изменение
@app.put("/orders/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order: OrderIn):
    for i, o in enumerate(orders_db):
        if o.id == order_id:
            orders_db[i] = Order(id=order_id, **order.dict())
            return orders_db[i]
    raise HTTPException(status_code=404, detail="Order not found")


# Удаление
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    for i, order in enumerate(orders_db):
        if order.id == order_id:
            orders_db.pop(i)
            return {"message": "Order deleted successfully"}
    raise HTTPException(status_code=404, detail="Order not found")


@validator('email')
def email_validatorr(cls, email):
    if not email.endswith('@example.com'):
        raise ValueError('invalid email domain')
    return email
