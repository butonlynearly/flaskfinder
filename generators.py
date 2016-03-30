import os
from datetime import datetime
import random
import math
import pickle
import csv

"""
a = Dice(6,1).roll()
b = Dice(6,3).rolls()
"""
class Dice:
	def __init__(self, type, times):
		self._times = times
		self._type = type
		
	def roll(self):
		return random.randint(1,self._type)
		
	def rolls(self):
		strresults = []
		results = []
		for i in range(self._times):
			strresults.append(random.randint(1,self._type))
		results = [int(i) for i in strresults]
		return results



"""Add ability to select race"""
class Name_Gen:

	def firstname(self):
		names = []
		f = open(r'D:\codehome\OOKingdom\names\dwarf_first.txt' ,'r')
		names = f.readlines()
		return random.choice(names)
	
	def lastname(self):
		names = []
		f = open(r'D:\codehome\OOKingdom\names\dwarf_last.txt' ,'r')
		names = f.readlines()
		return random.choice(names)

	def fullname(self):
		fname = self.firstname()
		lname = self.lastname()
		full_name = fname.strip() + " " + lname.strip()
		return full_name	
		

class Attr_Gen:

	attr = {'strength': 0, 'dexterity': 0, 'constitution': 0, 'intelligence': 0, 'wisdom': 0, 'charisma': 0}
	modifiers = {}	
	
	# accepts npc, npchero or pchero, threedsix, normalized
	def getattr(self, stat):
		if stat == "threedsix":
			return Attr_Gen().threedsix()
		elif stat == "normalized":
			return Attr_Gen().normalized()
		elif stat == "npc":
			return Attr_Gen().pregen("npc")
		elif stat == "npchero":
			return Attr_Gen().pregen("npchero")
		elif stat == "pchero":
			return Attr_Gen().pregen("pchero")
		else:
			return "Error interpreting getattr value"

	def getmod(self):
		for k,v in self.attr.items():
			mod = math.floor((v-10) / 2)
			self.modifiers[k + "_" + 'bonus'] = mod

	def threedsix(self):
		for k, v in self.attr.items():
			result = sum(Dice(6,3).rolls())
			self.attr[k] = result
		for k,v in self.attr.items():
			mod = math.floor((v-10) / 2)
			self.modifiers[k + "_" + 'bonus'] = mod
		combined = dict(list(self.attr.items()) + list(self.modifiers.items()))
		return combined

	def normalized(self):
		statlist = list()
		for i in range(6):
			statlist.append(random.randint(5,16)+2)
		for k,v in self.attr.items():
			self.attr[k] = statlist.pop(0)
		self.getmod()
		combined = dict(list(self.attr.items()) + list(self.modifiers.items()))
		return combined

	def pregen(self, type):
	# accepts npc, npchero or pchero
		if type is None:
			type = random.choice("npc","npchero","pchero")

		if type == "npc":
			statlist = [13,12,11,10,9,8]
			return statlist
		elif type == "npchero":
			statlist = [15,14,13,12,10,8]	
			return statlist
		elif type == "pchero":
			statlist = [18,17,16,15,14,13]
			return statlist
		else:
			print "pregen accepts character types of npc, npchero or pchero"
	
		random.shuffle(statlist)
		for k,v in self.attr.items():
			self.attr[k] = statlist.pop(0)
		self.getmod()
		combined = dict(list(self.attr.items()) + list(self.modifiers.items()))
		return combined

	
class NPC():
		def __init__(self,stat = None,amount = None):
			self._stat = stat
			self._amount = amount
			
		def create(self):
			print self._amount
			d = {}
			name = Name_Gen().fullname()
			#attr = Attr_Gen().normalized()
			attr = Attr_Gen().getattr(self._stat)
			attr['name'] = name
			character = attr
			return character
			
		def createmany(self):
			print self._amount
			d = {}
			for i in range(self._amount):
				name = Name_Gen().fullname()
				#attr = Attr_Gen().normalized()
				attr = Attr_Gen().getattr(self._stat)
				attr['name'] = name
				d[i] = attr
			return d
			
def Create_Rulers():
	kingdom_leaders = {}
	role = 0
	leader_roles = ['Ruler', 'Consort', 'Councilor', 'General', 'Grand Diplomat', 'Heir', 'High Priest', 'Magister', 'Marshal', 'Royal Enforcer', 'Spymaster', 'Treasurer', 'Viceroy', 'Warden']
	while len(leader_roles) > 0:
		char = NPC("normalized", 1).create()
		"""RANDOMIZE THE LIST OF LEADER ROLES"""
		role = leader_roles.pop()
		kingdom_leaders[role] = char
	return kingdom_leaders
	
"""pickle loader"""
def write_obj(name):
	with open('kingdom_leaders.picle', 'wb') as f:
		pickle.dump(kingdom_leaders, f, pickle.HIGHEST_PROTOCOL)
	

def load_obj(name):
    with open('obj/' + name + '.pkl', 'r') as f:
        return pickle.load(f)

def Write_CSV(object, filename):
			w = csv.writer(open(filename, "w"))
			for key, val in object.items():
				w.writerow([key, val])
				
def Read_CSV(filename):
	dict = {}
	for key, val in csv.reader(open(filename)):
		dict[key] = val
	

if __name__ == "__main__":
	#newchar = NPC("threedsix",2).create()
	#newchar = NPC("threedsix",2).createmany()
	#print newchar
	Create_Rulers()
