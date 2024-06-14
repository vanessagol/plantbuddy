from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Plant, CustomerPlant  # Relative import

plants_bp = Blueprint('plants', __name__)

@plants_bp.route("/")
def plants():
    all_plants = Plant.query.all()
    return render_template("plants.html", plants=all_plants)

@plants_bp.route("/add", methods=["GET", "POST"])
def add_plant():
    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        water_need = request.form["water_need"]
        fertilizer_need = request.form["fertilizer_need"]
        common_issues = request.form.get("common_issues")

        new_plant = Plant(
            name=name,
            location=location,
            water_need=water_need,
            fertilizer_need=fertilizer_need,
            common_issues=common_issues
        )
        db.session.add(new_plant)
        db.session.commit()
        flash("Plant added successfully!")
        return redirect(url_for("plants.plants"))

    return render_template("add_plant.html")
