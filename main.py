from flask import render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Customer, Plant, CareTask  # Relative import
from .plant_management import plants_bp  # Relative import
from . import create_app, mail  # Relative import

app = create_app()

def send_email_reminder(task):
    msg = Message('Plant Care Reminder', recipients=[task.plant.customer.email])
    msg.body = f"Reminder: {task.task_type} your plant {task.plant.name} on {task.task_date.strftime('%Y-%m-%d')}."
    mail.send(msg)

@app.route("/plants")
def plants():
    all_plants = Plant.query.all()
    return render_template("plants.html", plants=all_plants)

@app.route("/add_plant", methods=["GET", "POST"])
def add_plant():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        watering_frequency = request.form["watering_frequency"]
        fertilizing_frequency = request.form["fertilizing_frequency"]
        common_issues = request.form.get("common_issues")

        new_plant = Plant(
            name=name,
            location=location,
            water_need=watering_frequency,
            fertilizer_need=fertilizing_frequency,
            common_issues=common_issues
        )
        db.session.add(new_plant)
        db.session.commit()
        flash("Plant added successfully!")
        return redirect(url_for("plants"))

    return render_template("add_plant.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        existing_user = Customer.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists!')
            return redirect(url_for('register'))

        new_user = Customer(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/google_login')
def google_login():
    # Implement your Google login logic here
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = Customer.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash("Invalid email or password!")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        flash("Login successful!")
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/tasks")
def tasks():
    all_tasks = CareTask.query.all()
    return render_template("tasks.html", tasks=all_tasks)

@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        plant_id = request.form["plant_id"]
        task_type = request.form["task_type"]
        task_date = datetime.strptime(request.form["task_date"], '%Y-%m-%d')

        new_task = CareTask(
            plant_id=plant_id,
            task_type=task_type,
            task_date=task_date,
            is_completed=False,
            amount=1.0  # Placeholder, adjust as needed
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!")
        return redirect(url_for("tasks"))

    plants = Plant.query.all()
    return render_template("add_task.html", plants=plants)

@app.route("/send_reminders")
def send_reminders():
    tasks = CareTask.query.filter_by(is_completed=False).all()
    for task in tasks:
        if task.task_date.date() == datetime.now(timezone.utc).date():
            send_email_reminder(task)
    flash("Reminders sent!")
    return redirect(url_for("tasks"))

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
