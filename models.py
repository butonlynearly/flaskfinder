from sqlalchemy import Column, types
import extensions *

class Character(db.Model):

	id = Column(db.Integer, primary_key=True)
	user = Column(db.Integer)
	charname = Column(db.String(80))
	charclass = Column(db.String(40))
	charlevel = Column(db.Integer)
	character = Column(db.PickleType())
	d_created = Column(db.DateTime)
