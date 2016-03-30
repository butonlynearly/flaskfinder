from flask import Flask, request, render_template, url_for, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, fields, marshal_with, reqparse, marshal
import os, json
from generators import Attr_Gen, Name_Gen, Create_Rulers
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, types
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.dialects.postgresql import JSON
from flask_marshmallow import Marshmallow
import datetime

app = Flask('pathfinder')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.debug = True
api = Api(app)

Session = sessionmaker(autocommit=False,
					   autoflush=False,
					   bind=(db))
session = scoped_session(Session)

class Character(db.Model):

	id = Column(db.Integer, primary_key=True)
	user = Column(db.Integer)
	cdata = db.Column(JSON())
	
	@property
	def url(self):
		return url_for('character', id=self.id)
	
"""
#api definition
GET /character/api/v*/characters - Retrieve list of characters by user
GET /character/api/v*/characters/[character_id] - Retrieve a character
POST /character/api/v*/characters - Create a new character
PUT /character/api/v*/characters/[character_id] - Update an existing character
DELETE /character/api/v*/characters/[character_id] - Delete a character

"""
"""
# flask-restful
character_fields = {
	'id': fields.Integer,
	'cdata': fields.String
}

character_list_fields = {
    # Wrap list inside an object because of security reasons:
    # http://flask.pocoo.org/docs/0.10/security/#json-security
    'items': fields.List(fields.Nested(character_fields)),
}

class CharacterListAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('character', type=str, required=True,
			help = 'No character provided', location = 'json')

	@marshal_with(character_list_fields)	
	# returns cdata: null, id: 0
	def get(self):
		results = Character.query.with_entities(Character.id, Character.cdata[('character', 'demographics', 'name')]).all()
		return {
			'items': results,
		}
		#return {'characters': [marshal(results, character_fields) for result in results]}
		
	def post(self):
		pass
		
		args = self.reqparse.parse_args()
		character = {
			'character': args['character'],
			}
		characters.append(character)
		return {'character': marshal(character, character_fields)}, 201
		
"""

character_fields = {
    'id': fields.Integer,
    'cdata': fields.String
}

character_list_fields = {
    # Wrap list inside an object because of security reasons:
    # http://flask.pocoo.org/docs/0.10/security/#json-security
    'items': fields.List(fields.Nested(character_fields)),
}

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@api.resource('/characters')
class CharacterListAPI(Resource):
    @marshal_with(character_list_fields)
    def get(self):
		characters = Character.query.all()
		#characters = Character.query.with_entities(Character.id, Character.cdata[('character', 'demographics', 'name')]).all()
		return {
            'items': characters,
        }
		
class CharacterAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		
	def get(self, id):
		pass
		
	"""	
	def put(self, id):
		task = filter(lambda t: t['id'] == id, characters)
		if len(character) == 0:
			abort(404)
		character = character[0]
		args = self.reqparse.parse_args()
		for k, v in args.iteritems():
			if v != None:
				character[k] = v
		return jsonify( { 'character': make_public_character(character) } )
		
	"""	
	def delete(self, id):
		pass
		
api.add_resource(CharacterListAPI, '/character/api/v0.1/characters', endpoint='characters')

@app.route('/api/name', methods=['GET'])
def get_name():
		name = Name_Gen().fullname()
		return jsonify({'name': name})
				
@app.route('/api/characters', methods=['GET'])
def get_character():
		results = Character.query.with_entities(Character.id, Character.charname)
		#results = Character.query.all()
		#return jsonify({'character_list': results})
		return jsonify(results)
		
@app.route('/')
def index():
	name = Name_Gen().fullname()
	return render_template('index.html',name=name)
	
@app.route('/api/v0/vc', methods=['GET'])
def vc():
		#results = json.dumps(Character.query.with_entities(Character.sheet))
		#results = Character.query.all()
		#return jsonify({'character_list': results})
		results = Character.query.with_entities(Character.sheet).first()
		return results

"""		
class CharacterSchema(ma.ModelSchema):
	class Meta:
		model = Character
	
character_fields = {
	'character': fields.String
}

character_schema = CharacterSchema()

#access generator content
@app.route('/')
def index():
	name = Name_Gen().fullname()
	return render_template('index.html',name=name)
	
@app.route('/api/rulers', methods=['GET'])
def get_rulers():
		rulers = Create_Rulers()
		return jsonify({'rulers': rulers})

@app.route('/vc', methods=['GET'])
def vc():
	#results = Character.query.with_entities(Character.sheet)
	results = Character.query.with_entities(Character.id, Character.charname)
	return render_template('vc.html',results=results)
"""

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 3000)) # I like port 3000 :)
        app.run(host='127.0.0.1', port=port) 
