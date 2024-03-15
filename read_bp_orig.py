import json, os

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
		#get some info from the unit code
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

	def value_from_line(self, line):
		value = line.split("=")[1] #get the bit after the '='
		value = value[1:-1] #remove the first and last character (leading space and trailing comma)
		return value

	def __repr__(self):
		return f"{self.code} ({self.faction} {self.name}): {self.mass_cost}m, {self.energy_cost}e"

def main():
	blueprint_path = "bps"
	blueprint_names = os.listdir(blueprint_path)
	for bp_name in blueprint_names:
		bp = Blueprint(blueprint_path, bp_name)
		print(bp)

if __name__ == "__main__":
	main()