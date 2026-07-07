from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="admin", nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(TimestampMixin, db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(32), default="pcs", nullable=False)
    low_stock_threshold = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Warehouse(TimestampMixin, db.Model):
    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class Location(TimestampMixin, db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    code = db.Column(db.String(80), nullable=False, index=True)
    name = db.Column(db.String(255))

    warehouse = db.relationship("Warehouse", backref="locations")
    __table_args__ = (db.UniqueConstraint("warehouse_id", "code"),)


class Inventory(TimestampMixin, db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    quantity = db.Column(db.Integer, default=0, nullable=False)

    product = db.relationship("Product")
    warehouse = db.relationship("Warehouse")
    location = db.relationship("Location")
    __table_args__ = (
        db.UniqueConstraint("product_id", "warehouse_id", "location_id"),
    )


class StockInOrder(TimestampMixin, db.Model):
    __tablename__ = "stock_in_orders"

    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(80), unique=True, nullable=False, index=True)
    supplier_name = db.Column(db.String(255))
    remark = db.Column(db.String(500))

    items = db.relationship(
        "StockInItem", back_populates="order", cascade="all, delete-orphan"
    )


class StockInItem(db.Model):
    __tablename__ = "stock_in_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("stock_in_orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship("StockInOrder", back_populates="items")
    product = db.relationship("Product")
    warehouse = db.relationship("Warehouse")
    location = db.relationship("Location")


class StockOutOrder(TimestampMixin, db.Model):
    __tablename__ = "stock_out_orders"

    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(80), unique=True, nullable=False, index=True)
    customer_name = db.Column(db.String(255))
    remark = db.Column(db.String(500))

    items = db.relationship(
        "StockOutItem", back_populates="order", cascade="all, delete-orphan"
    )


class StockOutItem(db.Model):
    __tablename__ = "stock_out_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("stock_out_orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship("StockOutOrder", back_populates="items")
    product = db.relationship("Product")
    warehouse = db.relationship("Warehouse")
    location = db.relationship("Location")


class StockMovement(db.Model):
    __tablename__ = "stock_movements"

    id = db.Column(db.Integer, primary_key=True)
    movement_type = db.Column(db.String(20), nullable=False)
    reference_no = db.Column(db.String(80), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey("warehouses.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    quantity_delta = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    product = db.relationship("Product")
    warehouse = db.relationship("Warehouse")
    location = db.relationship("Location")

