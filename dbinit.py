import app
from app import db
import models

db = SQLAlchemy(app)

db.drop_all()
db.create_all()

if __name__ == __main__:
	app.run()