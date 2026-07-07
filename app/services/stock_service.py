from datetime import datetime

from ..extensions import db
from ..models import (
    Inventory,
    StockInItem,
    StockInOrder,
    StockMovement,
    StockOutItem,
    StockOutOrder,
)


def generate_order_no(prefix):
    return f"{prefix}{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"


def get_inventory_row(product_id, warehouse_id, location_id):
    query = Inventory.query.filter_by(
        product_id=product_id,
        warehouse_id=warehouse_id,
    )
    if location_id is None:
        query = query.filter(Inventory.location_id.is_(None))
    else:
        query = query.filter_by(location_id=location_id)
    return query.first()


def apply_stock_in(data):
    items = data.get("items") or []
    if not items:
        raise ValueError("items_required")

    order = StockInOrder(
        order_no=data.get("order_no") or generate_order_no("IN"),
        supplier_name=data.get("supplier_name"),
        remark=data.get("remark"),
    )
    db.session.add(order)
    db.session.flush()

    for item_data in items:
        product_id = int(item_data["product_id"])
        warehouse_id = int(item_data["warehouse_id"])
        location_id = item_data.get("location_id")
        location_id = int(location_id) if location_id else None
        quantity = int(item_data["quantity"])

        if quantity <= 0:
            raise ValueError("quantity_must_be_positive")

        item = StockInItem(
            order_id=order.id,
            product_id=product_id,
            warehouse_id=warehouse_id,
            location_id=location_id,
            quantity=quantity,
        )
        db.session.add(item)

        inventory = get_inventory_row(product_id, warehouse_id, location_id)
        if not inventory:
            inventory = Inventory(
                product_id=product_id,
                warehouse_id=warehouse_id,
                location_id=location_id,
                quantity=0,
            )
            db.session.add(inventory)
        inventory.quantity += quantity

        db.session.add(
            StockMovement(
                movement_type="IN",
                reference_no=order.order_no,
                product_id=product_id,
                warehouse_id=warehouse_id,
                location_id=location_id,
                quantity_delta=quantity,
            )
        )

    db.session.commit()
    return order


def apply_stock_out(data):
    items = data.get("items") or []
    if not items:
        raise ValueError("items_required")

    order = StockOutOrder(
        order_no=data.get("order_no") or generate_order_no("OUT"),
        customer_name=data.get("customer_name"),
        remark=data.get("remark"),
    )
    db.session.add(order)
    db.session.flush()

    for item_data in items:
        product_id = int(item_data["product_id"])
        warehouse_id = int(item_data["warehouse_id"])
        location_id = item_data.get("location_id")
        location_id = int(location_id) if location_id else None
        quantity = int(item_data["quantity"])

        if quantity <= 0:
            raise ValueError("quantity_must_be_positive")

        inventory = get_inventory_row(product_id, warehouse_id, location_id)
        if not inventory or inventory.quantity < quantity:
            raise ValueError("insufficient_inventory")

        item = StockOutItem(
            order_id=order.id,
            product_id=product_id,
            warehouse_id=warehouse_id,
            location_id=location_id,
            quantity=quantity,
        )
        db.session.add(item)

        inventory.quantity -= quantity
        db.session.add(
            StockMovement(
                movement_type="OUT",
                reference_no=order.order_no,
                product_id=product_id,
                warehouse_id=warehouse_id,
                location_id=location_id,
                quantity_delta=-quantity,
            )
        )

    db.session.commit()
    return order

