from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..models import Inventory, StockMovement


inventory_bp = Blueprint("inventory", __name__)


def inventory_to_dict(row):
    return {
        "id": row.id,
        "product_id": row.product_id,
        "product_sku": row.product.sku,
        "product_name": row.product.name,
        "warehouse_id": row.warehouse_id,
        "warehouse_code": row.warehouse.code,
        "location_id": row.location_id,
        "location_code": row.location.code if row.location else None,
        "quantity": row.quantity,
    }


@inventory_bp.get("")
@jwt_required()
def list_inventory():
    query = Inventory.query
    product_id = request.args.get("product_id")
    warehouse_id = request.args.get("warehouse_id")

    if product_id:
        query = query.filter_by(product_id=int(product_id))
    if warehouse_id:
        query = query.filter_by(warehouse_id=int(warehouse_id))

    rows = query.order_by(Inventory.id.desc()).all()
    return jsonify([inventory_to_dict(row) for row in rows])


@inventory_bp.get("/<int:product_id>")
@jwt_required()
def get_product_inventory(product_id):
    rows = Inventory.query.filter_by(product_id=product_id).all()
    return jsonify([inventory_to_dict(row) for row in rows])


@inventory_bp.get("/movements")
@jwt_required()
def list_movements():
    query = StockMovement.query
    product_id = request.args.get("product_id")
    if product_id:
        query = query.filter_by(product_id=int(product_id))

    rows = query.order_by(StockMovement.id.desc()).limit(200).all()
    return jsonify(
        [
            {
                "id": row.id,
                "movement_type": row.movement_type,
                "reference_no": row.reference_no,
                "product_id": row.product_id,
                "warehouse_id": row.warehouse_id,
                "location_id": row.location_id,
                "quantity_delta": row.quantity_delta,
                "created_at": row.created_at.isoformat(),
            }
            for row in rows
        ]
    )

