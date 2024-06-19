from plantbuddy import create_app, db
from plantbuddy.models import Plant

app = create_app()

with app.app_context():
    db.session.query(Plant).delete()
    db.session.commit()
    print("All plants have been removed from the database.")
