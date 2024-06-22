from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from flask_mail import Message
from ..database.db import db, Plant, CustomerPlant, CareTask
from .. import mail
from datetime import datetime, timedelta

plants_bp = Blueprint('plants', __name__, url_prefix='/plants', template_folder="templates")

@plants_bp.route("/")
@plants_bp.route("/plants")
def plants():
    search_term = request.args.get('search', '')
    if search_term:
        all_plants = Plant.query.filter(Plant.name.ilike(f'%{search_term}%')).all()
    else:
        all_plants = Plant.query.all()
    return render_template("plants.html", plants=all_plants, search_term=search_term)

@plants_bp.route("/plant/<int:plant_id>")
def plant_detail(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    return render_template("plant_detail.html", plant=plant)

@plants_bp.route("/add_plant_to_my_plants/<int:plant_id>", methods=["POST"])
@login_required
def add_plant_to_my_plants(plant_id):
    new_customer_plant = CustomerPlant(customer_id=current_user.id, plant_id=plant_id)
    db.session.add(new_customer_plant)
    db.session.commit()

    plant = Plant.query.get_or_404(plant_id)
    frequency = int(plant.watering_frequency[:-1]) if plant.watering_frequency[:-1].isdigit() else 1
    interval_days = 7 // frequency

    for i in range(frequency):
        task_date = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=i * interval_days)
        new_task = CareTask(
            plant_id=plant.id,
            task_type='Water',
            task_date=task_date,
            is_completed=False
        )
        db.session.add(new_task)
        db.session.commit()

        # Send email reminder
        send_task_email(current_user.email, plant.name, new_task.id)

    flash("Plant added to your collection!")
    return redirect(url_for("plants.my_plants"))

def send_task_email(email, plant_name, task_id):
    with current_app.app_context():
        msg = Message('Plant Care Reminder', sender='noreply@plantbuddy.com', recipients=[email])
        link = url_for('plants.complete_task', task_id=task_id, _external=True)
        msg.body = f'Reminder: Water your plant {plant_name}. Mark as done: {link}'
        mail.send(msg)

@plants_bp.route("/my_plants")
@login_required
def my_plants():
    user_plants = CustomerPlant.query.filter_by(customer_id=current_user.id).all()
    tasks = CareTask.query.filter(CareTask.plant_id.in_([cp.plant_id for cp in user_plants]), CareTask.is_completed == False).all()
    return render_template("my_plants.html", user_plants=user_plants, tasks=tasks)

@plants_bp.route("/complete_task/<int:task_id>", methods=["POST"])
@login_required
def complete_task(task_id):
    task = CareTask.query.get_or_404(task_id)
    if task.plant.customer_plants[0].customer_id != current_user.id:
        flash("You do not have permission to complete this task.")
        return redirect(url_for("plants.my_plants"))
    
    task.is_completed = True
    task.plant.customer_plants[0].last_watered_date = datetime.now()
    db.session.commit()
    flash("Task marked as completed!")
    return redirect(url_for("plants.my_plants"))

@plants_bp.route("/delete_plant/<int:plant_id>", methods=["POST"])
@login_required
def delete_plant(plant_id):
    customer_plant = CustomerPlant.query.filter_by(customer_id=current_user.id, plant_id=plant_id).first()
    if customer_plant:
        db.session.delete(customer_plant)
        db.session.commit()
        flash("Plant removed from your collection.")
    else:
        flash("Plant not found in your collection.")
    return redirect(url_for("plants.my_plants"))

@plants_bp.route("/tasks")
@login_required
def tasks():
    all_tasks = CareTask.query.all()
    return render_template("tasks.html", tasks=all_tasks)

@plants_bp.route("/add_task", methods=["GET", "POST"])
@login_required
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
        return redirect(url_for("plants.tasks"))

    plants = Plant.query.all()
    return render_template("add_task.html", plants=plants)

@plants_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_new_plant():
    if not current_user.is_admin:
        flash("You do not have permission to add new plants.")
        return redirect(url_for('plants.plants'))
        
    if request.method == "POST":
        name = request.form["name"]
        photo = request.form["photo"]
        description = request.form["description"]
        light = request.form["light"]
        humidity = request.form["humidity"]
        fertilizing = request.form["fertilizing"]
        toxicity = request.form["toxicity"]
        watering_frequency = request.form["watering_frequency"]

        new_plant = Plant(
            name=name,
            photo=photo,
            description=description,
            light=light,
            humidity=humidity,
            fertilizing=fertilizing,
            toxicity=toxicity,
            watering_frequency=watering_frequency
        )
        db.session.add(new_plant)
        db.session.commit()
        flash("Plant added successfully!")
        return redirect(url_for("plants.plants"))

    return render_template("add_plant.html")
