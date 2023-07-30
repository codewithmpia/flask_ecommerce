from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from .settings import app, db
from .models import User, Order
from .forms import RegisterForm, LoginForm


@app.route("/register/", methods=("GET", "POST"))
def register():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    
    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data 
        email = form.email.data
        password = form.password.data 

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Ce nom d'utilisateur est déjà pris. Veuillez choisir un autre.", "warning")
            return redirect(url_for("register"))
        
        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Vous êtes maintenant inscrit, vous pouvez vous connecté.", "info")

        return redirect(url_for("login"))
    
    elif form.errors:
        flash(form.errors, "warning")

    return render_template("register.html", form=form)


@app.route("/login/", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 

        user = User.query.filter_by(username=username).first()

        if not (user and user.check_password(password)):
            flash("Nom d'utitlisateur ou mot de passe invalide. Veuillez réessayer.", "warning")
            return redirect(url_for("auth.login"))
        
        login_user(user)

        flash("Vous êtes connecté.", "success")
        
        return redirect(url_for("profile"))
    
    elif form.errors:
        flash(form.errors, "warning")

    return render_template("login.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Vous êtes déconnecté.", "success")
        return redirect(url_for("product_list"))
    
    return redirect(url_for("product_list"))


@app.route("/profile/")
@login_required
def profile():
    orders = Order.query.filter_by(username=current_user.username)
    return render_template("profile.html", orders=orders)