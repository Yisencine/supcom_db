import json, os, sqlite3, traceback

TARGET_DATABASE_FILE = "supcom.db"

def unformatted_units(connection):

	'''just an example function to showcase how bad the table looks without any formatting'''

	cursor = connection.cursor()
	query = "SELECT * FROM Units_T1_Land)"
	cursor.execute(query)
	results = cursor.fetchall()
	print(results)

# its like a template which you can fill lots of data into, when you know there's gonna be a lot of files using the same variables as each other.
# you make instances with the "self." structure and can access and manipulate them more easily than a dictonary. You can also define methods within. Classes are great!

# e.g. with a dictionary you would have to make a seperate dictionary for each unit because you can't instance/reuse the same variables between each unit- 
# so you'd end up with a dictionary within a dictionary, which is more complicated to work with. Again, classes are great!

class Blueprint:
	FACTIONS = { #2nd character of unit code
		"E": "UEF",
		"R": "Cybran",
		"A": "Aeon",
		"S": "Seraphim"
	}
	UNIT_TYPE = { #3rd character of unit code
		"L": "Land",
		"A": "Air",
		"S": "Navy",
		"B": "Building",
	}
	def __init__(self, file_path, file_name):
		#get some info from the unit code (in the file name)
		self.code = file_name.split("_")[0]
		if self.code[1] in self.FACTIONS.keys():
			self.faction = self.FACTIONS[self.code[1]]
		else:
			self.faction = "Unknown"
		if self.code[2] in self.UNIT_TYPE.keys():
			self.unit_type = self.UNIT_TYPE[self.code[2]]
		else:
			self.unit_type = "Unknown"

		#search the .bp file for the rest of the info
		#firstly define default values in case proper values aren't found in the file
		self.name = "Unknown"
		self.energy_cost = -1
		self.mass_cost = -1
		self.tech_level = -1 
		self.field = "Unknown"
		self.health = -1 
		self.speed = 0
		self.DPS = 0
		self.range = -1
		self.damage = -1
		self.rof = -1
		self.is_engi = False


		#open the files based on the OS that the user is using, in read mode rather than write mode
		with open(os.path.join(file_path, file_name), "r") as f:
			lines = f.readlines()

		#search the file for keywords line by line
		for line in lines:
			line = line.strip() #remove trailing/leading whitespace

			if line.startswith("Description"):
				desc = self.value_from_line(line)
				try:
					name = desc.split(">")[1]
					name = name.split("\"")[0]
					self.name = name
				except IndexError:
					self.name = desc
			elif line.startswith("BuildCostEnergy"):
				self.energy_cost = int(self.value_from_line(line))
			elif line.startswith("BuildCostMass"):
				self.mass_cost = int(self.value_from_line(line))

			elif line.startswith("\"LAND") and len(line) < 12:
				self.field = "Land"
			elif line.startswith("\"AIR") and len(line) < 12:
				self.field = "Air"
			elif line.startswith("\"NAVAL") and len(line) < 12:
				self.field = "Naval"
			elif line.startswith("\"STRUCTURE") and len(line) < 16:
				self.field = "Structure"
			
			elif line.startswith("\"TECH") and len(line) < 9:
		
				self.tech_level = int(line[5])

			#this is because several files randomly use single quotes instead of double quotes
			elif line.startswith("\'TECH") and len(line) < 12:
				#the len < 12 used to be len < 8 idk why it kinda broke - the given lines are less than 8 char. and it worked before?
				self.tech_level = int(line[5])

			#we check for false positives with the "target priorities section"
			elif line.startswith("\"EXPERIMENTAL") and self.tech_level == -1:
				self.tech_level = 4
			 

			elif line.startswith("Health") and len(line) < 16:
				self.health = int(self.value_from_line(line))

			elif line.startswith("MaxSpeed") and len(line) < 16:
				self.speed = float(self.value_from_line(line))

			elif line.startswith("MaxRadius") and len(line) < 16:
				self.range = int(self.value_from_line(line))

			elif line.startswith("MaxBuildDistance") and self.range == -1:
				self.range = int(self.value_from_line(line))
				self.is_engi = True

			elif line.startswith("Damage = ") and not line.startswith("Damage = {"):
				#print(self.damage)

				self.damage = float(self.value_from_line(line))
			

			elif line.startswith("RateOfFire = ") and not line.startswith("RateOfFire = {"):
				#print(self.rof)
				self.rof = float(self.value_from_line(line))
				if self.damage != -1:
					if self.code == "XSL0103":
						self.damage *= 5
						print(f"{self.rof}*{self.damage} (5x projectiles for sera mobile light arty)")
					if self.code == "UAL0106":
						self.damage *= 3
						print(f"{self.rof}*{self.damage} (3x projectiles for aeon light assault bot)")
					self.DPS += self.rof * self.damage
					self.damage = -1
					self.rof = -1
			

	def value_from_line(self, line):
		value = line.split("=")[1] #get the bit after the '='
		value = value[1:-1] #remove the first and last character (leading space and trailing comma)
		return value

	def __repr__(self):
		return f"{self.code} ({self.faction} {self.name}): {self.mass_cost} mass, {self.energy_cost} energy, {self.health}HP, {self.speed} Speed, {self.DPS}DPS, {self.range} Range, Tech {self.tech_level}, {self.field}."

def main():
	blueprint_path = "bps"

	all_bps = dict()

	blueprint_names = os.listdir(blueprint_path)
	for bp_name in blueprint_names:
		bp = Blueprint(blueprint_path, bp_name)
		
		# if bp.tech_level == "1":

		# 	all_bps[bp.code] = bp
		# 	print(bp)
		#if bp.faction == "UEF":

		if bp.tech_level == 1 and bp.unit_type == "Land" and bp.is_engi == False or bp.name == "Point Defense" and bp.tech_level == 1:
		#if bp.faction == "UEF" and "Experimental" in bp.name:
			all_bps[bp.code] = bp
			print(bp)

	#print(all_bps["UEL0001"].name)

if __name__ == "__main__":
	main()