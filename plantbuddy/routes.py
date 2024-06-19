from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_mail import Message
from datetime import datetime, timezone
from .models import CareTask
from . import mail

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("home.html")

@main_bp.route("/home")
def home():
    return render_template("home.html")

# @main_bp.route("/blog")
# def blog():
#     # posts = BlogPost.query.all()  # Fetch all blog posts from the database
#     return render_template("blog.html", posts=posts)

@main_bp.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")

@main_bp.route("/send_reminders")
def send_reminders():
    tasks = CareTask.query.filter_by(is_completed=False).all()
    for task in tasks:
        if task.task_date.date() == datetime.now(timezone.utc).date():
            send_email_reminder(task)
    flash("Reminders sent!")
    return redirect(url_for("main.tasks"))

def send_email_reminder(task):
    msg = Message('Plant Care Reminder', recipients=[task.plant.customer.email])
    msg.body = f"Reminder: {task.task_type} your plant {task.plant.name} on {task.task_date.strftime('%Y-%m-%d')}."
    mail.send(msg)

def clear_flashes():
    if '_flashes' in session:
        del session['_flashes']

