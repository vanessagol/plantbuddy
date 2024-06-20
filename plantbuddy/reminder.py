from flask import render_template, url_for
from flask_mail import Message
from .db.models import Customer, CustomerPlant, CareTask
from . import mail, db
from datetime import datetime, timedelta

def send_reminder():
    customers = Customer.query.all()
    for customer in customers:
        customer_plants = CustomerPlant.query.filter_by(customer_id=customer.id).all()
        for customer_plant in customer_plants:
            plant = customer_plant.plant
            tasks = CareTask.query.filter_by(plant_id=plant.id, is_completed=False).all()
            for task in tasks:
                if task.task_date.date() == datetime.now().date():
                    msg = Message('Plant Care Reminder', sender='plantbuddy@gmail.com', recipients=[customer.email])
                    link = url_for('plants.complete_task', task_id=task.id, _external=True)
                    msg.body = f'Reminder: {task.task_type} your plant {plant.name} today. Mark as done: {link}'
                    mail.send(msg)
                    task.is_completed = True
                    db.session.commit()

def schedule_tasks():
    all_plants = db.Plant.query.all()
    for plant in all_plants:
        if plant.watering_frequency:
            frequency = int(plant.watering_frequency[:-1])
            next_date = datetime.now() + timedelta(days=7//frequency)
            for _ in range(frequency):
                task = CareTask(
                    plant_id=plant.id,
                    task_type='Water',
                    task_date=next_date,
                    is_completed=False,
                    amount=1.0  # Placeholder, adjust as needed
                )
                db.session.add(task)
                next_date += timedelta(days=7//frequency)
            db.session.commit()
