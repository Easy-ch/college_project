from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from sqlalchemy import Index

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    isAuthorized = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    phone_number = Column(String(15), nullable=True, unique=True)

    order = relationship("Order", back_populates="user", lazy="selectin")
    email_logs = relationship("EmailLog", back_populates="user", cascade="all, delete-orphan", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("username", name="uq_user_username"),
    )



class Product(Base):
    __tablename__ = "products"

    id  = Column(Integer, primary_key=True, index=True)                # id товара
    sku = Column(String, unique=True, nullable=False)                  # Уникальный артикул
    name = Column(String, nullable=False)                               # Название товара
    description = Column(Text, nullable=True)                                  # Описание товара
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False) # Категория товара
    price = Column(Float, nullable=False)                                # Цена


    cart_items = relationship("Cart", back_populates="product", lazy="selectin")
    images = relationship("ProductImage", back_populates="product", lazy="selectin", cascade="all, delete-orphan")
    category = relationship("Category", back_populates="products")

class Category(Base):
    __tablename__ = "categories"

    id        = Column(Integer, primary_key=True, index=True)               # id категории
    name      = Column(String, nullable=False, unique=True)                 # Название категории
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True) # Иерархия категорий
    description = Column(Text, nullable=True)                               # Описание категории

    parent = relationship("Category", remote_side=[id], back_populates="children", lazy="selectin")
    children = relationship("Category", back_populates="parent", lazy="selectin", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="category", lazy="selectin")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) # Ссылка на товар
    image_path = Column(String, nullable=False)                             # Путь к изображению

    product = relationship("Product", back_populates="images", lazy="selectin")



class Cart(Base):
    __tablename__ = "cart"

    id  = Column(Integer, primary_key=True, index=True)
    user_id  = Column(Integer, ForeignKey("users.id"), nullable=False)    # id пользователя
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) # id товара
    quantity = Column(Integer, nullable=False, default=1)                 # Количество
    user = relationship("User", lazy="selectin")
    product = relationship("Product", back_populates="cart_items", lazy="selectin")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="В ожидании подтверждения")
    name = Column(String, nullable=False)
    phone = Column(String(15), nullable=False)
    comment = Column(Text, nullable=True)

    user = relationship("User", back_populates="order", lazy="selectin")
    items = relationship("OrderItem", back_populates="order", lazy="selectin")




class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items", lazy="selectin")
    product = relationship("Product", lazy="selectin")




class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    last_email_time = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="email_logs", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("user_id", name="uq_email_log_user_id"),
    )




class BlockedRoute(Base):
    __tablename__ = "blocked_routes"

    id = Column(Integer, primary_key=True, index=True)
    route = Column(String, nullable=False, unique=True)
    expire_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5))

    __table_args__ = (
        Index("ix_blocked_routes_expire_at", expire_at),
    )



