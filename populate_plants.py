from plantbuddy import create_app, db
from plantbuddy.models import Plant, Customer, BlogPost
from werkzeug.security import generate_password_hash
import os

app = create_app()

def populate_db():
    plants_data = [
        {
            "name": "Spider Plant",
            "photo": "static/images/plants/spider_plant.png",
            "description": "A popular houseplant with long, arching leaves. The Spider Plant is also known for its tremendous air purifying qualities, making it a healthy addition to your home as well.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Non-toxic to humans and pets.",
            "watering_frequency": "2x"
        },
        {
            "name": "Aloe Vera",
            "photo": "static/images/plants/aloe_vera.jpg",
            "description": "A succulent plant known for its medicinal properties.",
            "light": "Bright, direct light",
            "humidity": "Low",
            "fertilizing": "-",
            "toxicity": "Non-toxic to humans but can be mildly toxic to pets.",
            "watering_frequency": "1x"
        },
        {
            "name": "Peace Lily",
            "photo": "static/images/plants/peace_lily.jpg",
            "description": "A beautiful plant with white flowers.",
            "light": "Partial-shade",
            "humidity": "High",
            "fertilizing": "Weekly",
            "toxicity": "Toxic to cats and dogs.",
            "watering_frequency": "3x"
        },
        {
            "name": "Snake Plant",
            "photo": "static/images/plants/snake_plant.jpg",
            "description": "An easy-to-care-for plant with upright leaves.",
            "light": "Low to bright, indirect light",
            "humidity": "Low",
            "fertilizing": "Monthly",
            "toxicity": "Mildly toxic to pets if ingested.",
            "watering_frequency": "1x"
        },
        {
            "name": "Pothos",
            "photo": "static/images/plants/pothos.jpg",
            "description": "A trailing plant with heart-shaped leaves.",
            "light": "Low to bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        },
        {
            "name": "Philodendron",
            "photo": "static/images/plants/philodendron.jpg",
            "description": "A versatile plant with various leaf shapes.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        },
        {
            "name": "ZZ Plant",
            "photo": "static/images/plants/zz_plant.jpg",
            "description": "A hardy plant with thick, waxy leaves.",
            "light": "Low to bright, indirect light",
            "humidity": "Low",
            "fertilizing": "-",
            "toxicity": "Toxic to pets and humans if ingested.",
            "watering_frequency": "1x"
        },
        {
            "name": "Fiddle Leaf Fig",
            "photo": "static/images/plants/fiddle_leaf_fig.jpg",
            "description": "A large plant with violin-shaped leaves.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        },
        {
            "name": "Succulent Mix",
            "photo": "static/images/plants/succulent_mix.jpg",
            "description": "A mix of various succulent plants.",
            "light": "Bright, direct light",
            "humidity": "Low",
            "fertilizing": "-",
            "toxicity": "Varies by species.",
            "watering_frequency": "1x"
        },
        {
            "name": "Cactus",
            "photo": "static/images/plants/cactus.jpg",
            "description": "A desert plant with thick, fleshy stems.",
            "light": "Bright, direct light",
            "humidity": "Low",
            "fertilizing": "-",
            "toxicity": "Non-toxic.",
            "watering_frequency": "1x"
        },
        {
            "name": "Boston Fern",
            "photo": "static/images/plants/boston_fern.jpg",
            "description": "A lush plant with feathery fronds.",
            "light": "Bright, indirect light",
            "humidity": "High",
            "fertilizing": "Weekly",
            "toxicity": "Non-toxic.",
            "watering_frequency": "3x"
        },
        {
            "name": "Jade Plant",
            "photo": "static/images/plants/jade_plant.jpg",
            "description": "A succulent with round, fleshy leaves.",
            "light": "Bright, indirect light",
            "humidity": "Low",
            "fertilizing": "Monthly",
            "toxicity": "Mildly toxic to pets.",
            "watering_frequency": "1x"
        },
        {
            "name": "Rubber Plant",
            "photo": "static/images/plants/rubber_plant.jpg",
            "description": "A plant with large, glossy leaves.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        },
        {
            "name": "Dracaena",
            "photo": "static/images/plants/dracaena.jpg",
            "description": "A tall plant with slender, arching leaves.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        },
        {
            "name": "Lucky Bamboo",
            "photo": "static/images/plants/lucky_bamboo.jpg",
            "description": "A plant known for its good luck symbolism.",
            "light": "Low to bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "-",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        },
        {
            "name": "English Ivy",
            "photo": "static/images/plants/english_ivy.jpg",
            "description": "A trailing plant with lobed leaves.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        },
        {
            "name": "Calathea",
            "photo": "static/images/plants/calathea.jpg",
            "description": "A plant with beautifully patterned leaves.",
            "light": "Bright, indirect light",
            "humidity": "High",
            "fertilizing": "Weekly",
            "toxicity": "Non-toxic to pets.",
            "watering_frequency": "3x"
        },
        {
            "name": "Orchid",
            "photo": "static/images/plants/orchid.jpg",
            "description": "A plant with elegant flowers.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Weekly",
            "toxicity": "Non-toxic.",
            "watering_frequency": "2x"
        },
        {
            "name": "Bamboo Palm",
            "photo": "static/images/plants/bamboo_palm.jpg",
            "description": "A palm plant with slender, bamboo-like stems.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Monthly",
            "toxicity": "Non-toxic.",
            "watering_frequency": "2x"
        },
        {
            "name": "Begonia",
            "photo": "static/images/plants/begonia.jpg",
            "description": "A plant with vibrant, colorful flowers.",
            "light": "Bright, indirect light",
            "humidity": "Medium",
            "fertilizing": "Weekly",
            "toxicity": "Toxic to pets if ingested.",
            "watering_frequency": "2x"
        }
    ]

    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password_hash": generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'admin')),
        "is_admin": True
    }

    blog_post_data = {
        "title": "Welcome to PlantBuddy!",
        "content": "This is the first blog post on PlantBuddy. Stay tuned for more updates!",
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

with app.app_context():
    populate_db()
