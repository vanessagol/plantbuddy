from flask import request, render_template, redirect, url_for, flash, Blueprint
plants_bp = Blueprint('plants_bp', __name__)
from models import Plant, db


# Erstelle ein Blueprint für das Pflanzenmanagement
plants_bp = Blueprint('plants_bp', __name__)

@plants_bp.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        water_need = request.form.get('water_need')
        fertilizer_need = request.form.get('fertilizer_need')
        common_issues = request.form.get('common_issues')

        new_plant = Plant(name=name, location=location, water_need=water_need, 
                          fertilizer_need=fertilizer_need, common_issues=common_issues)
        db.session.add(new_plant)
        db.session.commit()
        flash('Pflanze erfolgreich hinzugefügt!')
        return redirect(url_for('plants_bp.display_plants'))

    return render_template('add_plant.html')

@plants_bp.route('/plants')
def display_plants():
    plants = Plant.query.all()
    return render_template('plants.html', plants=plants)
