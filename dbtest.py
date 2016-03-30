from flask import Flask, request, render_template, url_for, jsonify, abort, make_response
import os, json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, types
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import JSON
import datetime

app = Flask('pathfinder')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
app.debug = True

class Character(db.Model):

	id = Column(db.Integer, primary_key=True)
	user = Column(db.Integer)
	cdata = db.Column(JSON())
	
	@property
	def url(self):
		return url_for('character', id=self.id)


#db.drop_all()
#db.create_all()


character = [
	{
		"character": {
			"demographics": {
				"name": "Dukane",
				"race": "human",
				"sex": "male"
			},
			"progressions": [{
				"characterClass": "fighter",
				"hitpoints": "10"
			}, {
				"characterClass": "fighter",
				"hitpoints": "5"
			}, {
				"characterClass": "fighter",
				"hitpoints": "6"
			}],
			"abilities": [{
				"name": "strength",
				"score": "15"
			}, {
				"name": "dexterity",
				"score": "10"
			}, {
				"name": "costitution",
				"score": "14"
			}, {
				"name": "intelligence",
				"score": "13"
			}, {
				"name": "wisdom",
				"score": "12"
			}, {
				"name": "charisma",
				"score": "8"
			}],
			"skills": [{
				"name": "Athletics",
				"ranks": "1",
				"ability": "strength",
				"c": "true"
			}]
		}
	}
]

def char():
	#f = open(r'D:\codehome\flaskkingdom\sheetmod.json' ,'r')
	#json.load loads json from file or file like object
	#json.loads loads json from a given string or unicode object
	#json_data = json.load(f)
	#c = json.dumps(json_data['character'])
	#parsed = json.load(json_data)
	#newchar = Character(user = json_data['user'],
	#				charname = json_data['charname'],
	#				character = json.dumps(json_data['character']))
	newchar = Character(cdata = character[0])
	db.session.add(newchar)
	db.session.commit()
	#results = Character.cdata[('sheet', 'demographics', 'name')]
	#results = Character.query.with_entities(Character.cdata[('character', 'demographics', 'name')]).all()
	#print results
	#return render_template('index.html')
	
#char()


@app.route('/')
def index():	
	#results = Character.query.all()
	#return jsonify({'character_list': results})
	#return jsonify(results)
	results = Character.query.with_entities(Character.id, Character.cdata[('character', 'demographics', 'name')]).all()
	#randvar = jsonify(character = results) 
	randvar = json.dumps(results)
	#return jsonify(character=results)
	return render_template('index.html', randvar=randvar)



if __name__ == '__main__':
	port = int(os.environ.get("PORT", 3000)) # I like port 3000 :)
        app.run(host='127.0.0.1', port=port) 

	