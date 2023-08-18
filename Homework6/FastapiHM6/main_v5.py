# from fastapi import FastAPI, HTTPException, Path, Query
# from pydantic import BaseModel, EmailStr, validator, ValidationError
# from typing import List
# from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
from typing import List

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


class Product(BaseModel):
    name: str
    description: str
    price: float


class User(BaseModel):
    first_name: str
    last_name: str
    # email: EmailStr
    email: str
    password: str


class Order(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    order_status: str


app = FastAPI()

# Подключение к базе данных
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)

Base = declarative_base()


# Модели таблиц
class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    order_date = Column(String(255), nullable=False)
    order_status = Column(String(255), nullable=False)

    user = relationship("UserDB", backref="orders")
    product = relationship("ProductDB", backref="orders")


# Создание таблиц
Base.metadata.create_all(bind=engine)


# CRUD операции для каждой из таблиц через создание маршрутов, REST API

# Таблица "Товары"
# Чтение всех
@app.get("/products", response_model=List[Product])
def get_products(skip: int = 0):
    session = Session()
    products = session.query(ProductDB).offset(skip).all()
    session.close()
    return products


# Чтение одного
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    session = Session()
    product = session.get(ProductDB, product_id)
    session.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Запись
@app.post("/products", response_model=Product)
def add_product(product: Product):
    session = Session()
    product_db = ProductDB(**product.dict())
    session.add(product_db)
    session.commit()
    session.refresh(product_db)
    session.close()
    return product_db


# Изменение
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    session = Session()
    p = session.get(ProductDB, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    product_dict = product.dict(exclude_unset=True)
    for key, value in product_dict.items():
        setattr(p, key, value)
    session.commit()
    session.refresh(p)
    session.close()
    return p


# Удаление
@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    session = Session()
    p = session.get(ProductDB, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(p)
    session.commit()
    session.close()
    return {"message": "Product deleted successfully"}


# Таблица "Пользователи"
# Чтение всех
@app.get("/users", response_model=List[User])
def get_users(skip: int = 0):
    session = Session()
    users = session.query(UserDB).offset(skip).all()
    session.close()
    return users


# Чтение одного
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    session = Session()
    user = session.get(UserDB, user_id)
    session.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Запись
@app.post("/users", response_model=User)
def add_user(user: User):
    session = Session()
    user_db = UserDB(**user.dict())
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    session.close()
    return user_db


# Изменение
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    session = Session()
    u = session.get(UserDB, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = user.dict(exclude_unset=True)
    for key, value in user_dict.items():
        setattr(u, key, value)
    session.commit()
    session.refresh(u)
    session.close()
    return u


# Удаление
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    session = Session()
    u = session.get(UserDB, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(u)
    session.commit()
    session.close()
    return {"message": "User deleted successfully"}


# Таблица "Заказы"
# Чтение всех
@app.get("/orders", response_model=List[Order])
def get_orders(skip: int = 0):
    session = Session()
    orders = session.query(OrderDB).offset(skip).all()
    session.close()
    return orders


# Чтение одного
@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    session = Session()
    order = session.get(OrderDB, order_id)
    session.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Запись
@app.post("/orders", response_model=Order)
def add_order(order: Order):
    session = Session()
    order_db = OrderDB(**order.dict())
    session.add(order_db)
    session.commit()
    session.refresh(order_db)
    session.close()
    return order_db


# Изменение
@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: Order):
    session = Session()
    o = session.get(OrderDB, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    order_dict = order.dict(exclude_unset=True)
    for key, value in order_dict.items():
        setattr(o, key, value)
    session.commit()
    session.refresh(o)
    session.close()
    return o


# Удаление
@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    session = Session()
    o = session.get(OrderDB, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(o)
    session.commit()
    session.close()
    return {"message": "Order deleted successfully"}


# Передача параметров запроса
@app.get("/predict")
def predict(
        q: str = Query(None, min_length=3, max_length=50, title="Query")
):
    return {"message": q}
