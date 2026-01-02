from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, ROLES, CITIES
from . import db
from werkzeug.security import generate_password_hash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.get("/login")
def login():
    return render_template("login.html")


@auth_bp.post("/login")
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        flash("Credenciales inválidas", "danger")
        return redirect(url_for("auth.login"))
    login_user(user)
    flash("Has iniciado sesión", "success")
    return redirect(url_for("main.dashboard"))


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login"))


@auth_bp.get("/register")
@login_required
def register():
    if current_user.role != "admin":
        flash("Solo el administrador puede crear usuarios.", "warning")
        return redirect(url_for("main.dashboard"))
    return render_template("register.html", roles=ROLES, cities=CITIES)


@auth_bp.post("/register")
@login_required
def register_post():
    if current_user.role != "admin":
        flash("Solo el administrador puede crear usuarios.", "warning")
        return redirect(url_for("main.dashboard"))
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")
    city = request.form.get("city")
    if role not in ROLES:
        role = "cliente"
    if User.query.filter_by(email=email).first():
        flash("El email ya existe.", "danger")
        return redirect(url_for("auth.register"))
    user = User(name=name, email=email, role=role, city=city)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash("Usuario creado.", "success")
    return redirect(url_for("main.dashboard"))
