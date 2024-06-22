from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_mail import Message
from flask_login import login_required, current_user
from ..database.db import CareTask, BlogPost, db, Customer
from .. import mail

main_bp = Blueprint('main', __name__, template_folder="templates")

@main_bp.route("/")
def index():
    return render_template("home.html")

@main_bp.route("/home")
def home():
    return render_template("home.html")

@main_bp.route("/blog")
def blog():
    posts = BlogPost.query.filter_by(approved=True).all() 
    return render_template("blog.html", posts=posts)

@main_bp.route("/blog/post/<int:post_id>")
def post_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@main_bp.route("/add_blog", methods=["GET", "POST"])
@login_required
def add_blog():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        
        new_post = BlogPost(
            title=title,
            content=content,
            author=current_user,
            approved=False
        )
        db.session.add(new_post)
        db.session.commit()
        
        # Notify admin
        admin_users = Customer.query.filter_by(is_admin=True).all()
        for admin in admin_users:
            msg = Message(
                'New Blog Post Awaiting Approval',
                sender='noreply@plantbuddy.com',
                recipients=[admin.email]
            )
            msg.body = f'New blog post titled "{title}" has been submitted and is awaiting your approval.'
            mail.send(msg)
        
        flash("Your blog post has been submitted for review.")
        return redirect(url_for("main.blog"))
    
    return render_template("add_blog.html")

@main_bp.route("/approve_blog/<int:post_id>", methods=["GET", "POST"])
@login_required
def approve_blog(post_id):
    if not current_user.is_admin:
        flash("You do not have permission to approve blog posts.")
        return redirect(url_for("main.blog"))
    
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == "POST":
        post.approved = True
        db.session.commit()
        flash("Blog post approved.")
        return redirect(url_for("main.admin_approval"))
    
    return render_template("approve_blog.html", post=post)

@main_bp.route("/delete_blog/<int:post_id>", methods=["POST"])
@login_required
def delete_blog(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if not current_user.is_admin and current_user.id != post.author_id:
        flash("You do not have permission to delete this blog post.")
        return redirect(url_for("main.blog"))
    
    db.session.delete(post)
    db.session.commit()
    flash("Blog post deleted.")
    return redirect(url_for("main.blog"))

@main_bp.route("/admin_approval")
@login_required
def admin_approval():
    if not current_user.is_admin:
        flash("You do not have permission to view this page.")
        return redirect(url_for("main.blog"))
    
    posts = BlogPost.query.filter_by(approved=False).all()
    return render_template("admin_approval.html", posts=posts)

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