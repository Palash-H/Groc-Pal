from models import Product
from models import db
from sqlalchemy import asc, desc

def create_product(data):
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    return product


def get_product(product_id):
    return Product.query.get_or_404(product_id)





def get_all_products(filters=None, sort_by=None, order=None):
    query = Product.query

    if filters:

        if filters.get("category_id") is not None:
            query = query.filter(Product.category_id == filters["category_id"])

        if filters.get("min_price") is not None:
            query = query.filter(Product.price >= filters["min_price"])

        if filters.get("max_price") is not None:
            query = query.filter(Product.price <= filters["max_price"])

        if filters.get("in_stock") is True:
            query = query.filter(Product.quantity > 0)

    if sort_by:
        column = getattr(Product, sort_by, None)

        if column:
            if order == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

    return query.all()


def update_product(product_id, data):
    product = Product.query.get_or_404(product_id)

    for key, value in data.items():
        setattr(product, key, value)

    db.session.commit()
    return product


def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()