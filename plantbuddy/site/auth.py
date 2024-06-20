from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from ..config import Config, s, client
from ..database.db import db, Customer
from .. import mail
import requests
import json
import os

auth_bp = Blueprint('auth', __name__, template_folder="templates")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('auth.register'))

        existing_user = Customer.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists!')
            return redirect(url_for('auth.register'))

        new_user = Customer(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = Customer.query.filter_by(email=email).first()
        if user is None:
            flash("Email not registered!")
            return redirect(url_for("auth.login"))
        elif not user.check_password(password):
            flash("Invalid password!")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Login successful!")
        return redirect(url_for("main.home"))

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    flash("You have been logged out.")
    return redirect(url_for("main.home"))

@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = Customer.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='password-reset-salt')
            msg = Message('Password Reset Request', sender=Config.MAIL_USERNAME, recipients=[email])
            link = url_for('auth.reset_password', token=token, _external=True)
            msg.body = f'Your link to reset the password is {link}'
            try:
                mail.send(msg)
                flash(f'An email with a reset link has been sent to {email}.')
            except Exception as e:
                flash(f'An error occurred while sending the email: {str(e)}')
        else:
            flash('Email address not found.')
        return redirect(url_for('auth.forgot_password'))
    return render_template('forgot_password.html')

@auth_bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('The reset link has expired.')
        return redirect(url_for('auth.forgot_password'))

    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('auth.reset_password', token=token))

        user = Customer.query.filter_by(email=email).first()
        user.set_password(password)
        db.session.commit()
        flash("Your password has been updated!")
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)

@auth_bp.route('/google_login')
def google_login():
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)

@auth_bp.route('/google_login/callback')
def callback():
    code = request.args.get('code')
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg['token_endpoint']

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    userinfo = userinfo_response.json()
    email = userinfo['email']

    user = Customer.query.filter_by(email=email).first()
    if user is None:
        user = Customer(
            username=userinfo['name'],
            email=email,
        )
        # Set a default random password for Google login users
        user.set_password(os.urandom(24).hex())
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('main.home'))
