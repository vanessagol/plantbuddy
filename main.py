from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://(LocalDb)\\MSSQLLocalDB/PflanzenMonitor'
    '?driver=ODBC+Driver+17+for+SQL+Server'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

mail = Mail(app)

def send_email_reminder(task):
    msg = Message('Plant Care Reminder', recipients=[task.plant.owner.email])
    msg.body = f"Reminder: {task.task_type} your plant {task.plant.name} on {task.task_date.strftime('%Y-%m-%d')}."
    mail.send(msg)

db = SQLAlchemy(app)

# Modell für Benutzer
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
            return f'<User {self.username}>'

# Modell für Pflanzen
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    watering_frequency = db.Column(db.Integer, nullable=False)  # in Tagen
    fertilizing_frequency = db.Column(db.Integer, nullable=False)  # in Tagen
    common_issues = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Plant {self.name}>'

# Modell für Pflegeaufgaben
class CareTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # 'Water' or 'Fertilize'
    task_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_completed = db.Column(db.Boolean, default=False)

    plant = db.relationship('Plant', backref=db.backref('care_tasks', lazy=True))

    def __repr__(self):
        return f'<CareTask {self.task_type} for {self.plant.name}>'


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
            watering_frequency=watering_frequency,
            fertilizing_frequency=fertilizing_frequency,
            common_issues=common_issues
        )
        db.session.add(new_plant)
        db.session.commit()
        flash("Plant added successfully!")
        return redirect(url_for("plants"))

    return render_template("add_plant.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists!")
            return redirect(url_for("register"))
        
        if User.query.filter_by(email=email).first():
            flash("Email already registered!")
            return redirect(url_for("register"))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
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
            is_completed=False
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
def home():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)