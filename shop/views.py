from flask import render_template, request, session, redirect, url_for, flash
from flask_login import current_user, login_required

from .settings import app, db
from .import models
from .import forms 


@app.route("/")
@app.route("/products/")
@app.route("/products/<string:category_slug>/<int:category_id>/")
def product_list(category_slug=None, category_id=None):
    category = None
    categories = models.Category.query.all()
    products = models.Product.query.filter_by(
        available=True).order_by(models.Product.created_on.desc())

    if category_slug and category_id:
        category = models.Category.query.get_or_404(category_slug, category_id)
        products = products.filter_by(category_id=category.id)

    return render_template(
        "product_list.html",
        category=category,
        categories=categories,
        products=products
    )


@app.route("/products/<int:product_id>/<string:product_slug>/", methods=("GET", "POST"))
def product_detail(product_id, product_slug):
    product = models.Product.query.get_or_404(product_id, product_slug)
    form = forms.QuantityForm()

    return render_template(
        "product_detail.html", 
        product=product, 
        form=form
    )


@app.route("/cart/")
def cart_list():
    total = 0

    if "cart" not in session:
        session["cart"] = []

    cart = session.get("cart", [])

    for item in cart:
        total += (item["price"] * item["quantity"])

    return render_template(
        "cart.html", 
        cart=cart,
        total=total
    )


@app.route("/cart/add/<int:product_id>/", methods=("GET", "POST"))
def add_to_cart(product_id):
    product = models.Product.query.get_or_404(product_id)

    form = forms.QuantityForm()

    if request.method == "POST" and form.validate_on_submit():
        quantity = form.quantity.data 

        for cart_item in session["cart"]:
            if cart_item["id"] == product.id:
                cart_item["quantity"] += 1

                return redirect(url_for("cart_list"))
            
        session["cart"].append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "image": product.image1,
            "quantity": quantity
        })

        return redirect(url_for("cart_list"))
    
    elif form.errors:
        flash(form.errors, "warning")

    return redirect(request.referrer)


@app.route("/cart/remove/<int:item_index>/")
def remove_from_cart(item_index):
    cart = session["cart"]

    if 0 <= item_index < len(cart):
        del cart[item_index]

    return redirect(url_for("cart_list"))


@app.route("/cart/clear/")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart_list"))


@app.route("/checkout/")
@login_required
def checkout():
    cart = session.get("cart", [])

    if len(cart) > 0:
        for product in cart:
            order = models.Order(
                user_id=int(current_user.id),
                product_id=int(product["id"]),
                quantity=int(product["quantity"]),
                total=float(float(product["price"]) * int(product["quantity"]))
            )
            db.session.add(order)
            db.session.commit()

            session.pop("cart", None)

        return render_template("partials/confirmation_order.html")

    return redirect(url_for("cart_list"))

