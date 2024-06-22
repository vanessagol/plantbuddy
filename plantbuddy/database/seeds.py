from werkzeug.security import generate_password_hash
from .db import Plant, Customer, BlogPost, db
import os

def populate_db():
    plants_data = [
        {
            "name": "Grünlilie",
            "photo": "static/images/plants/spider_plant.png",
            "description": "Eine beliebte Zimmerpflanze mit langen, gebogenen Blättern. Die Grünlilie ist auch für ihre hervorragenden luftreinigenden Eigenschaften bekannt und somit eine gesunde Ergänzung für Ihr Zuhause.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Nicht giftig für Menschen und Haustiere.",
            "watering_frequency": "2x"
        },
        {
            "name": "Aloe Vera",
            "photo": "static/images/plants/aloe_vera.jpg",
            "description": "Eine Sukkulente, die für ihre medizinischen Eigenschaften bekannt ist.",
            "light": "Helles, direktes Licht",
            "humidity": "Niedrig",
            "fertilizing": "-",
            "toxicity": "Nicht giftig für Menschen, aber leicht giftig für Haustiere.",
            "watering_frequency": "1x"
        },
        {
            "name": "Einblatt",
            "photo": "static/images/plants/peace_lily.jpg",
            "description": "Eine schöne Pflanze mit weißen Blüten.",
            "light": "Halbschatten",
            "humidity": "Hoch",
            "fertilizing": "Wöchentlich",
            "toxicity": "Giftig für Katzen und Hunde.",
            "watering_frequency": "3x"
        },
        {
            "name": "Bogenhanf",
            "photo": "static/images/plants/snake_plant.jpg",
            "description": "Eine pflegeleichte Pflanze mit aufrechten Blättern.",
            "light": "Schwach bis hell, indirektes Licht",
            "humidity": "Niedrig",
            "fertilizing": "Monatlich",
            "toxicity": "Leicht giftig für Haustiere bei Einnahme.",
            "watering_frequency": "1x"
        },
        {
            "name": "Efeutute",
            "photo": "static/images/plants/pothos.jpg",
            "description": "Eine rankende Pflanze mit herzförmigen Blättern.",
            "light": "Schwach bis hell, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        },
        {
            "name": "Philodendron",
            "photo": "static/images/plants/philodendron.jpg",
            "description": "Eine vielseitige Pflanze mit verschiedenen Blattformen.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        },
        {
            "name": "Glücksfeder",
            "photo": "static/images/plants/zz_plant.jpg",
            "description": "Eine robuste Pflanze mit dicken, wachsartigen Blättern.",
            "light": "Schwach bis hell, indirektes Licht",
            "humidity": "Niedrig",
            "fertilizing": "-",
            "toxicity": "Giftig für Haustiere und Menschen bei Einnahme.",
            "watering_frequency": "1x"
        },
        {
            "name": "Geigenfeige",
            "photo": "static/images/plants/fiddle_leaf_fig.jpg",
            "description": "Eine große Pflanze mit geigenförmigen Blättern.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        },
        {
            "name": "Sukkulenten-Mix",
            "photo": "static/images/plants/succulent_mix.jpg",
            "description": "Ein Mix aus verschiedenen Sukkulenten.",
            "light": "Helles, direktes Licht",
            "humidity": "Niedrig",
            "fertilizing": "-",
            "toxicity": "Je nach Art unterschiedlich.",
            "watering_frequency": "1x"
        },
        {
            "name": "Kaktus",
            "photo": "static/images/plants/cactus.jpg",
            "description": "Eine Wüstenpflanze mit dicken, fleischigen Stämmen.",
            "light": "Helles, direktes Licht",
            "humidity": "Niedrig",
            "fertilizing": "-",
            "toxicity": "Nicht giftig.",
            "watering_frequency": "1x"
        },
        {
            "name": "Bostonfarn",
            "photo": "static/images/plants/boston_fern.jpg",
            "description": "Eine üppige Pflanze mit federartigen Wedeln.",
            "light": "Helles, indirektes Licht",
            "humidity": "Hoch",
            "fertilizing": "Wöchentlich",
            "toxicity": "Nicht giftig.",
            "watering_frequency": "3x"
        },
        {
            "name": "Jadepflanze",
            "photo": "static/images/plants/jade_plant.jpg",
            "description": "Eine Sukkulente mit runden, fleischigen Blättern.",
            "light": "Helles, indirektes Licht",
            "humidity": "Niedrig",
            "fertilizing": "Monatlich",
            "toxicity": "Leicht giftig für Haustiere.",
            "watering_frequency": "1x"
        },
        {
            "name": "Gummibaum",
            "photo": "static/images/plants/rubber_plant.jpg",
            "description": "Eine Pflanze mit großen, glänzenden Blättern.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        },
        {
            "name": "Drachenbaum",
            "photo": "static/images/plants/dracaena.jpg",
            "description": "Eine hohe Pflanze mit schlanken, gebogenen Blättern.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        },
        {
            "name": "Glücksbambus",
            "photo": "static/images/plants/lucky_bamboo.jpg",
            "description": "Eine Pflanze, die für ihr Symbol des Glücks bekannt ist.",
            "light": "Schwach bis hell, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "-",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        },
        {
            "name": "Efeu",
            "photo": "static/images/plants/english_ivy.jpg",
            "description": "Eine rankende Pflanze mit gelappten Blättern.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        },
        {
            "name": "Korbmarante",
            "photo": "static/images/plants/calathea.jpg",
            "description": "Eine Pflanze mit wunderschön gemusterten Blättern.",
            "light": "Helles, indirektes Licht",
            "humidity": "Hoch",
            "fertilizing": "Wöchentlich",
            "toxicity": "Nicht giftig für Haustiere.",
            "watering_frequency": "3x"
        },
        {
            "name": "Orchidee",
            "photo": "static/images/plants/orchid.jpg",
            "description": "Eine Pflanze mit eleganten Blüten.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Wöchentlich",
            "toxicity": "Nicht giftig.",
            "watering_frequency": "2x"
        },
        {
            "name": "Bergpalme",
            "photo": "static/images/plants/bamboo_palm.jpg",
            "description": "Eine Palmenpflanze mit schlanken, bambusartigen Stielen.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Monatlich",
            "toxicity": "Nicht giftig.",
            "watering_frequency": "2x"
        },
        {
            "name": "Begonie",
            "photo": "static/images/plants/begonia.jpg",
            "description": "Eine Pflanze mit lebhaften, bunten Blüten.",
            "light": "Helles, indirektes Licht",
            "humidity": "Mittel",
            "fertilizing": "Wöchentlich",
            "toxicity": "Giftig für Haustiere bei Einnahme.",
            "watering_frequency": "2x"
        }
    ]

    admin_data = {
        "username": "admin",
        "email": "plantbudddy@gmail.com",
        "password_hash": generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin')),
        "is_admin": True
    }

    blog_post_data = {
        "title": "Willkommen bei PlantBuddy!",
        "content": "Dies ist der erste Blogeintrag über PlantBuddy. Bleiben Sie dran für weitere Updates! \n Fragen? Feedback? Wir möchten alles hören! Senden Sie uns eine Nachricht an info@plantbuddy.com ",
        "author_email": admin_data["email"]
    }

    if not Plant.query.first():  # Check if the database is empty
        for plant_data in plants_data:
            plant = Plant(**plant_data)
            db.session.add(plant)

        admin = Customer(**admin_data)
        db.session.add(admin)

        blog_post = BlogPost(
            title=blog_post_data["title"],
            content=blog_post_data["content"],
            author=admin,
            approved=True
        )
        db.session.add(blog_post)

        db.session.commit()

        print("Plants, admin user, and blog post have been added to the database.")
    else:
        print("Database is not empty, skipping population.")
