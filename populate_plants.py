from plantbuddy import create_app, db
from plantbuddy.models import Plant

app = create_app()

plants_data = [
    {
        "name": "Spider Plant",
        "photo": "static/images/plants/spider_plant.png",
        "description": "A popular houseplant with long, arching leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Aloe Vera",
        "photo": "static/images/plants/aloe_vera.jpg",
        "description": "A succulent plant known for its medicinal properties.",
        "placement": "Bright, direct light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Peace Lily",
        "photo": "static/images/plants/peace_lily.jpg",
        "description": "A beautiful plant with white flowers.",
        "placement": "Partial-shade",
        "water_demand": "High",
        "fertilizing": "Weekly"
    },
    {
        "name": "Snake Plant",
        "photo": "static/images/plants/snake_plant.jpg",
        "description": "An easy-to-care-for plant with upright leaves.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Low",
        "fertilizing": "Monthly"
    },
    {
        "name": "Pothos",
        "photo": "static/images/plants/pothos.jpg",
        "description": "A trailing plant with heart-shaped leaves.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Philodendron",
        "photo": "static/images/plants/philodendron.jpg",
        "description": "A versatile plant with various leaf shapes.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "ZZ Plant",
        "photo": "static/images/plants/zz_plant.jpg",
        "description": "A hardy plant with thick, waxy leaves.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Fiddle Leaf Fig",
        "photo": "static/images/plants/fiddle_leaf_fig.jpg",
        "description": "A large plant with violin-shaped leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Succulent Mix",
        "photo": "static/images/plants/succulent_mix.jpg",
        "description": "A mix of various succulent plants.",
        "placement": "Bright, direct light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Cactus",
        "photo": "static/images/plants/cactus.jpg",
        "description": "A desert plant with thick, fleshy stems.",
        "placement": "Bright, direct light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Boston Fern",
        "photo": "static/images/plants/boston_fern.jpg",
        "description": "A lush plant with feathery fronds.",
        "placement": "Bright, indirect light",
        "water_demand": "High",
        "fertilizing": "Weekly"
    },
    {
        "name": "Jade Plant",
        "photo": "static/images/plants/jade_plant.jpg",
        "description": "A succulent with round, fleshy leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Low",
        "fertilizing": "Monthly"
    },
    {
        "name": "Rubber Plant",
        "photo": "static/images/plants/rubber_plant.jpg",
        "description": "A plant with large, glossy leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Dracaena",
        "photo": "static/images/plants/dracaena.jpg",
        "description": "A tall plant with slender, arching leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Lucky Bamboo",
        "photo": "static/images/plants/lucky_bamboo.jpg",
        "description": "A plant known for its good luck symbolism.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "-"
    },
    {
        "name": "English Ivy",
        "photo": "static/images/plants/english_ivy.jpg",
        "description": "A trailing plant with lobed leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Calathea",
        "photo": "static/images/plants/calathea.jpg",
        "description": "A plant with beautifully patterned leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "High",
        "fertilizing": "Weekly"
    },
    {
        "name": "Orchid",
        "photo": "static/images/plants/orchid.jpg",
        "description": "A plant with elegant flowers.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Weekly"
    },
    {
        "name": "Bamboo Palm",
        "photo": "static/images/plants/bamboo_palm.jpg",
        "description": "A palm plant with slender, bamboo-like stems.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Begonia",
        "photo": "static/images/plants/begonia.jpg",
        "description": "A plant with vibrant, colorful flowers.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Weekly"
    }
]

with app.app_context():
    for plant_data in plants_data:
        plant = Plant(**plant_data)
        db.session.add(plant)

    db.session.commit()

    print("Plants have been added to the database.")
