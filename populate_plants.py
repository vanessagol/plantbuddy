from . import db
from .models import Plant

# Sample data for 20 plants
plants_data = [
    {
        "name": "Spider Plant",
        "photo": "path/to/spider_plant.jpg",
        "description": "A popular houseplant with long, arching leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Aloe Vera",
        "photo": "path/to/aloe_vera.jpg",
        "description": "A succulent plant known for its medicinal properties.",
        "placement": "Bright, direct light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Peace Lily",
        "photo": "path/to/peace_lily.jpg",
        "description": "A beautiful plant with white flowers.",
        "placement": "Partial-shade",
        "water_demand": "High",
        "fertilizing": "Weekly"
    },
    {
        "name": "Snake Plant",
        "photo": "path/to/snake_plant.jpg",
        "description": "An easy-to-care-for plant with upright leaves.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Low",
        "fertilizing": "Monthly"
    },
    {
        "name": "Pothos",
        "photo": "path/to/pothos.jpg",
        "description": "A trailing plant with heart-shaped leaves.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Philodendron",
        "photo": "path/to/philodendron.jpg",
        "description": "A versatile plant with various leaf shapes.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "ZZ Plant",
        "photo": "path/to/zz_plant.jpg",
        "description": "A hardy plant with thick, waxy leaves.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Fiddle Leaf Fig",
        "photo": "path/to/fiddle_leaf_fig.jpg",
        "description": "A large plant with violin-shaped leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Succulent Mix",
        "photo": "path/to/succulent_mix.jpg",
        "description": "A mix of various succulent plants.",
        "placement": "Bright, direct light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Cactus",
        "photo": "path/to/cactus.jpg",
        "description": "A desert plant with thick, fleshy stems.",
        "placement": "Bright, direct light",
        "water_demand": "Low",
        "fertilizing": "-"
    },
    {
        "name": "Boston Fern",
        "photo": "path/to/boston_fern.jpg",
        "description": "A lush plant with feathery fronds.",
        "placement": "Bright, indirect light",
        "water_demand": "High",
        "fertilizing": "Weekly"
    },
    {
        "name": "Jade Plant",
        "photo": "path/to/jade_plant.jpg",
        "description": "A succulent with round, fleshy leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Low",
        "fertilizing": "Monthly"
    },
    {
        "name": "Rubber Plant",
        "photo": "path/to/rubber_plant.jpg",
        "description": "A plant with large, glossy leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Dracaena",
        "photo": "path/to/dracaena.jpg",
        "description": "A tall plant with slender, arching leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Lucky Bamboo",
        "photo": "path/to/lucky_bamboo.jpg",
        "description": "A plant known for its good luck symbolism.",
        "placement": "Low to bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "-"
    },
    {
        "name": "English Ivy",
        "photo": "path/to/english_ivy.jpg",
        "description": "A trailing plant with lobed leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Calathea",
        "photo": "path/to/calathea.jpg",
        "description": "A plant with beautifully patterned leaves.",
        "placement": "Bright, indirect light",
        "water_demand": "High",
        "fertilizing": "Weekly"
    },
    {
        "name": "Orchid",
        "photo": "path/to/orchid.jpg",
        "description": "A plant with elegant flowers.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Weekly"
    },
    {
        "name": "Bamboo Palm",
        "photo": "path/to/bamboo_palm.jpg",
        "description": "A palm plant with slender, bamboo-like stems.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Monthly"
    },
    {
        "name": "Begonia",
        "photo": "path/to/begonia.jpg",
        "description": "A plant with vibrant, colorful flowers.",
        "placement": "Bright, indirect light",
        "water_demand": "Medium",
        "fertilizing": "Weekly"
    }
]

# Add plants to the database
for plant_data in plants_data:
    plant = Plant(**plant_data)
    db.session.add(plant)

db.session.commit()

print("Plants have been added to the database.")
