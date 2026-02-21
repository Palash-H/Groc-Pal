from flask.views import MethodView
from flask_smorest import Blueprint
from flask_smorest import abort
from flask import request
from flask_jwt_extended import jwt_required
from utils.roles import admin_required
from schemas.product_schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema
)
from services.product_service import (
    create_product,
    get_product,
    get_all_products,
    update_product,
    delete_product
)

blp = Blueprint(
    "Products",
    "products",
    url_prefix="/api/v1/products",
    description="Product CRUD Operations"
)


@blp.route("/")
class ProductList(MethodView):


    @blp.response(200, ProductResponseSchema(many=True))
    @jwt_required()
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        category_id = request.args.get("category_id", type=int)
        min_price = request.args.get("min_price", type=float)
        max_price = request.args.get("max_price", type=float)
        in_stock = request.args.get("in_stock")

        if in_stock is not None:
            in_stock = in_stock.lower() == "true"

        sort_by = request.args.get("sort_by")
        order = request.args.get("order", "asc")

        filters = {
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock
        }

        products = get_all_products(filters, sort_by, order)

        start = (page - 1) * per_page
        end = start + per_page

        return products[start:end]

    @blp.arguments(ProductCreateSchema)
    @blp.response(201, ProductResponseSchema)
    @admin_required()
    def post(self, new_data):
        return create_product(new_data)


@blp.route("/<int:product_id>")
class ProductDetail(MethodView):

    @blp.response(200, ProductResponseSchema)
    @jwt_required()
    def get(self, product_id):
        return get_product(product_id)

    @blp.arguments(ProductUpdateSchema)
    @blp.response(200, ProductResponseSchema)
    @admin_required()
    def put(self, update_data, product_id):
        return update_product(product_id, update_data)

    @admin_required()
    def delete(self, product_id):
        delete_product(product_id)
        return {"message": "Deleted successfully"}, 204