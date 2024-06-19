from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import db, Plant, CustomerPlant, Customer, CareTask
from flask_login import login_required, current_user
from datetime import datetime

plants_bp = Blueprint('plants', __name__)
@plants_bp.route("/")
@plants_bp.route("/")
def plants():
    all_plants = Plant.query.all()
    print("Database URI: ", db.engine.url)  # Print database URI
    print("All Plants: ", all_plants)  # Detailed debugging line
    for plant in all_plants:
        print(f"Plant: {plant.name}, Photo: {plant.photo}")
    return render_template("plants.html", plants=all_plants)

@plants_bp.route("/plant/<int:plant_id>")
def plant_detail(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    print(f"Plant Photo Path: {plant.photo}")  # Debugging line
    return render_template("plant_detail.html", plant=plant)

@plants_bp.route("/add_plant", methods=["GET", "POST"])
@login_required
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
            water_demand=watering_frequency,  # corrected attribute
            fertilizing=fertilizing_frequency,  # corrected attribute
            description=common_issues
        )
        db.session.add(new_plant)
        db.session.commit()
        flash("Plant added successfully!")
        return redirect(url_for("plants.plants"))

    return render_template("add_plant.html")

@plants_bp.route("/my_plants")
@login_required
def my_plants():
    user_plants = CustomerPlant.query.filter_by(customer_id=current_user.id).all()
    return render_template("my_plants.html", user_plants=user_plants)

@plants_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_new_plant():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        watering_frequency = request.form["watering_frequency"]
        fertilizing_frequency = request.form["fertilizing_frequency"]
        common_issues = request.form.get("common_issues")

        new_plant = Plant(
            name=name,
            location=location,
            water_demand=watering_frequency,  # corrected attribute
            fertilizing=fertilizing_frequency,  # corrected attribute
            description=common_issues
        )
        db.session.add(new_plant)
        db.session.commit()
        flash("Plant added successfully!")
        return redirect(url_for("plants.plants"))

    return render_template("add_plant.html")

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
            is_completed=False,
            amount=1.0  # Placeholder, adjust as needed
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully!")
        return redirect(url_for("plants.tasks"))

    plants = Plant.query.all()
    return render_template("add_task.html", plants=plants)