from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Plant, CustomerPlant  # Relative import

plants_bp = Blueprint('plants', __name__)

@plants_bp.route("/")
def plants():
    all_plants = Plant.query.all()
    return render_template("plants.html", plants=all_plants)

@plants_bp.route("/plant/<int:plant_id>")
def plant_detail(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    return render_template("plant_detail.html", plant=plant)

@plants_bp.route("/add_plant/<int:plant_id>")
def add_plant(plant_id):
    # Logic to add plant to the user's collection
    return redirect(url_for('plants.plants'))
