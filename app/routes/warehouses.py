from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..extensions import db
from ..models import Location, Warehouse


warehouses_bp = Blueprint("warehouses", __name__)


def warehouse_to_dict(warehouse):
    return {
        "id": warehouse.id,
        "code": warehouse.code,
        "name": warehouse.name,
        "address": warehouse.address,
        "is_active": warehouse.is_active,
    }


def location_to_dict(location):
    return {
        "id": location.id,
        "warehouse_id": location.warehouse_id,
        "code": location.code,
        "name": location.name,
    }


@warehouses_bp.get("/warehouses")
@jwt_required()
def list_warehouses():
    warehouses = Warehouse.query.order_by(Warehouse.id.desc()).all()
    return jsonify([warehouse_to_dict(warehouse) for warehouse in warehouses])


@warehouses_bp.post("/warehouses")
@jwt_required()
def create_warehouse():
    data = request.get_json() or {}
    if not data.get("code") or not data.get("name"):
        return jsonify({"error": "code_and_name_required"}), 400

    warehouse = Warehouse(
        code=data["code"], name=data["name"], address=data.get("address")
    )
    db.session.add(warehouse)
    db.session.commit()
    return jsonify(warehouse_to_dict(warehouse)), 201


@warehouses_bp.get("/locations")
@jwt_required()
def list_locations():
    locations = Location.query.order_by(Location.id.desc()).all()
    return jsonify([location_to_dict(location) for location in locations])


@warehouses_bp.post("/locations")
@jwt_required()
def create_location():
    data = request.get_json() or {}
    if not data.get("warehouse_id") or not data.get("code"):
        return jsonify({"error": "warehouse_id_and_code_required"}), 400

    location = Location(
        warehouse_id=int(data["warehouse_id"]),
        code=data["code"],
        name=data.get("name"),
    )
    db.session.add(location)
    db.session.commit()
    return jsonify(location_to_dict(location)), 201

