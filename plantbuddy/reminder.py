from flask import render_template
from flask_mail import Message
from .models import Customer, CustomerPlant, Plant
from . import mail, db
from datetime import datetime

def send_reminder():
    customers = Customer.query.all()
    for customer in customers:
        customer_plants = CustomerPlant.query.filter_by(customer_id=customer.id).all()
        if customer_plants:
            msg = Message('Plant Care Reminder', sender='plantbudddy@gmail.com', recipients=[customer.email])
            msg.html = render_template('email/reminder.html', user=customer, plants=[cp.plant for cp in customer_plants])
            mail.send(msg)
            for customer_plant in customer_plants:
                customer_plant.last_watered_date = datetime.utcnow()
            db.session.commit()
