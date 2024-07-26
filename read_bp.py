import json, os, sqlite3, traceback

TARGET_DATABASE_FILE = "supcom.db"

def ask_for_int_value(string):

	# function that sanitises user input to make sure that they enter a valid number into parts of my program which require integers, without crashing the program

	while True:
		try:
			integer_input = input(f"{string}")
			int(integer_input)

			return integer_input
		except:
			print("\n\nPLEASE ENTER A VALID NUMERICAL VALUE!\n")


def user_input_valid_check(lower_bound, upper_bound, user_value):

	'''function which checks to make sure that the user doesn't enter a value lower or higher than they are meant to'''

	if int(user_value) > upper_bound or int(user_value) < lower_bound:
		while True:
			retry_user_input = ask_for_int_value(f"\nPlease enter a valid value between {lower_bound} and {upper_bound}: ")
			if int(retry_user_input) <= upper_bound and int(retry_user_input) >= lower_bound:
				print("\nRetried input was successful!\n")
				return retry_user_input
	else:
		return user_value

def add_bp_to_db(connection, bp):
# this query adds the chosen info from the dataset into the sql database for us to work with in there

	try:
		cursor = connection.cursor()
		query = "INSERT INTO Units_T1_Land(ID, Name, Health, DPS, Mass_Cost, Energy_Cost, Range, Speed, Faction_ID) VALUES (?,?,?,?,?,?,?,?,?)"
		# cursor.execute(query, (bp.id, bp.name + " " + bp.faction, + bp.health, bp.DPS, bp.mass_cost, bp.energy_cost, bp.range, bp.speed, bp.faction_ID))
		cursor.execute(query, (bp.id, bp.name, bp.health, bp.DPS, bp.mass_cost, bp.energy_cost, bp.range, bp.speed, bp.faction_ID))
		connection.commit()
		# print("\n Units (BP) were added successfully to database!\n")
	except Exception as error:
		traceback.print_exc()
		# print("\nUh oh, couldn't ADD_BP_TO_DB, something went wrong!")


def test_print(connection, bp):

	# raw test sql query 

	try:
		cursor = connection.cursor()
		query = "SELECT * FROM Units_T1_Land"
		cursor.execute(query)
		results = cursor.fetchall()
		print(results)

	except Exception as error:
		traceback.print_exc()
		print("\nUh oh, couldn't do TEST_PRINT, something went wrong!")

def check_counter(connection, bp):

	# prints out the units table in a nice format, joins data nicely and such

	try:
		cursor = connection.cursor()
		query = "SELECT Units_T1_Land.ID, Units_T1_Land.Name FROM Units_T1_Land;"
		cursor.execute(query)
		results = cursor.fetchall()
		print(f"\n{'ID':<5}{'NAME':<40}\n")
		for info in results:
			print(f"{info[0]:<5}{info[1]:<40}")

		choose_unit = ask_for_int_value("\nPlease enter the unit ID (number) of the unit you would like to check the counters for: ")

		# need to make this update if the user introduces more than 40 total units to the database
		choose_unit = user_input_valid_check(1, 23, choose_unit)

		# query = "SELECT Matchup.Unit_for_ID, Matchup.Unit_against_ID, Matchup.Description, Units_T1_Land.ID, Units_T1_Land.Name FROM Matchup JOIN Units_T1_Land ON Units_T1_Land.ID=Matchup.Unit_for_ID WHERE Unit_for_ID = ?;"
		query = """
		SELECT This_info.Name as This_name, Counters.Name as Counter_name, Matchup.Description FROM Matchup 
		JOIN Units_T1_Land as Counters  ON Matchup.Unit_against_ID=Counters.ID
		JOIN Units_T1_Land as This_info ON Matchup.Unit_for_ID=This_info.ID WHERE Matchup.Unit_for_ID = ?
		"""

		cursor.execute(query, (choose_unit,))
		results = cursor.fetchall()
		print(f"\n\nCHOSEN UNIT \n\n{results[0][0]}")
		print(f"\n{'COUNTERS':<40}{'DESCRIPTIONS':<100}\n")
		
		#print(f"{results[0][0]:<30}{results[0][1]:<40}{results[0][2]:<100}")
		#nothing = ""

		for info in results:
			print(f"{info[1]:<40}{info[2]:<100}")

	except Exception as error:
		traceback.print_exc()
		print("\nUh oh, something went wrong while trying to SHOW_UNITS")


def show_units(connection, bp):

	# prints out the units table in a nice format, joins data nicely and such

	try:
		cursor = connection.cursor()

		query = """SELECT Units_T1_Land.Name, Units_T1_Land.Health, Units_T1_Land.DPS, Units_T1_Land.Mass_Cost, Units_T1_Land.Energy_Cost, 
	Units_T1_Land.Range, Units_T1_Land.Speed, Faction.Faction_Name FROM Units_T1_Land JOIN Faction ON Units_T1_Land.Faction_ID=Faction.ID;"""
		cursor.execute(query)
		results = cursor.fetchall()
		print(f"\n{'NAME':<40}{'HEALTH':<20}{'DAMAGE/SECOND':<20}{'MASS COST':<20}{'ENERGY COST':<20}{'WEAPON RANGE':<20}{'MAX SPEED':<20}{'FACTION':<20}\n")
		for info in results:
			print(f"{info[0]:<40}{info[1]:<20}{info[2]:<20}{info[3]:<20}{info[4]:<20}{info[5]:<20}{info[6]:<20}{info[7]:<20}")
	except Exception as error:
		traceback.print_exc()
		print("\nUh oh, something went wrong while trying to SHOW_UNITS")

def order_units(connection, bp):

	# function which allows you to order units by a chosen stat

	try:
		print("""\nSTATS TO SORT BY:\n 
  [ 1 ] Health
  [ 2 ] DPS
  [ 3 ] Mass Cost
  [ 4 ] Energy Cost
  [ 5 ] Range
  [ 6 ] Speed
  [ 7 ] Faction """)

		cursor = connection.cursor()

		choose_stat = ask_for_int_value("\nPlease enter the stat ID (number) of the statistic you would like to order the table by: ")
		choose_stat = user_input_valid_check(1, 7, choose_stat)

		column_names = ['Units_T1_Land.Health', 'Units_T1_Land.DPS', 'Units_T1_Land.Mass_Cost', 'Units_T1_Land.Energy_Cost', 'Units_T1_Land.Range', 'Units_T1_Land.Speed', 'Faction.Faction_Name']

		query = f"""
		SELECT Units_T1_Land.Name, Units_T1_Land.Health, 
		Units_T1_Land.DPS, Units_T1_Land.Mass_Cost, 
		Units_T1_Land.Energy_Cost, Units_T1_Land.Range, 
		Units_T1_Land.Speed, Faction.Faction_Name 
		FROM Units_T1_Land JOIN Faction ON Units_T1_Land.Faction_ID=Faction.ID ORDER BY {column_names[int(choose_stat) - 1]};"""
		
		# this is safe from injection and doesn't need to use the ? syntax, because the user input HAS to be a number to get through, and all that the number can be used for is to select from the column names afterwards


		#print(f"'{column_names[int(choose_stat) - 1]}'")
		#connection.set_trace_callback(print)
		cursor.execute(query)
		#connection.set_trace_callback(None)

		results = cursor.fetchall()
		print(f"\n{'NAME':<40}{'HEALTH':<20}{'DAMAGE/SECOND':<20}{'MASS COST':<20}{'ENERGY COST':<20}{'WEAPON RANGE':<20}{'MAX SPEED':<20}{'FACTION':<20}\n")
		for info in results:
			print(f"{info[0]:<40}{info[1]:<20}{info[2]:<20}{info[3]:<20}{info[4]:<20}{info[5]:<20}{info[6]:<20}{info[7]:<20}")
	except Exception as error:
		traceback.print_exc()
		print("\nUh oh, something went wrong while trying to ORDER_UNITS")

def filter_by_faction(connection, bp):

	# function which allows you to order units by a chosen stat

	try:
		print("""\nFACTIONS TO CHOOSE:\n 
  [ 1 ] UEF
  [ 2 ] Cybran
  [ 3 ] Aeon
  [ 4 ] Seraphim """)

		cursor = connection.cursor()

		choose_fac = ask_for_int_value("\nPlease enter the Faction ID (number) of the faction you would like to print units from: ")
		choose_fac = user_input_valid_check(1, 4, choose_fac)

		faction_column_names = ['UEF', 'Cybran', 'Aeon', 'Seraphim']

		print(f"\n\nPRINTING ONLY: {faction_column_names[int(choose_fac) - 1]} Units")

		query = """
		SELECT Units_T1_Land.Name, Units_T1_Land.Health, 
		Units_T1_Land.DPS, Units_T1_Land.Mass_Cost, 
		Units_T1_Land.Energy_Cost, Units_T1_Land.Range, 
		Units_T1_Land.Speed, Faction.Faction_Name 
		FROM Units_T1_Land JOIN Faction ON Units_T1_Land.Faction_ID=Faction.ID WHERE Faction.Faction_Name = ?;"""
		
		# this is safe from injection and doesn't need to use the ? syntax, because the user input HAS to be a number to get through, and all that the number can be used for is to select from the column names afterwards


		#print(f"'{column_names[int(choose_stat) - 1]}'")
		#connection.set_trace_callback(print)
		cursor.execute(query, (faction_column_names[int(choose_fac) - 1],))
		#connection.set_trace_callback(None)

		results = cursor.fetchall()
		print(f"\n{'NAME':<40}{'HEALTH':<20}{'DAMAGE/SECOND':<20}{'MASS COST':<20}{'ENERGY COST':<20}{'WEAPON RANGE':<20}{'MAX SPEED':<20}{'FACTION':<20}\n")
		for info in results:
			print(f"{info[0]:<40}{info[1]:<20}{info[2]:<20}{info[3]:<20}{info[4]:<20}{info[5]:<20}{info[6]:<20}{info[7]:<20}")
	except Exception as error:
		traceback.print_exc()
		print("\nUh oh, something went wrong while trying to FILTER_BY_FACTION")


def add_unit(connection, bp):

	new_unit_name = input("\n Enter new unit name: ")

	new_unit_HP = ask_for_int_value("\n Enter new unit health value: ")
	new_unit_HP = user_input_valid_check(1, 1000000, new_unit_HP)

	new_unit_DPS = ask_for_int_value("\n Enter new unit DPS value: ")
	new_unit_DPS = user_input_valid_check(1, 100000, new_unit_DPS)

	new_unit_MC = ask_for_int_value("\n Enter new unit mass cost value: ")
	new_unit_MC = user_input_valid_check(1, 1000000, new_unit_MC)

	new_unit_EC = ask_for_int_value("\n Enter new unit energy cost value: ")
	new_unit_EC = user_input_valid_check(1, 50000000, new_unit_EC)

	new_unit_WR = ask_for_int_value("\n Enter new weapon range value: ")
	new_unit_WR = user_input_valid_check(1, 100000, new_unit_WR)

	new_unit_MS = ask_for_int_value("\n Enter new max speed value: ")
	new_unit_MS = user_input_valid_check(1, 100000, new_unit_MS)

	new_unit_FAC = ask_for_int_value("\n Enter new faction ID (1 = UEF, 2 = Cybran, 3 = Aeon, 4 = Seraphim: ")
	new_unit_FAC = user_input_valid_check(1, 4, new_unit_FAC)

	'''allows the user to pretty safely add games to the table'''

	try:
		cursor = connection.cursor()
		query = "INSERT INTO Units_T1_Land(Name, Health, DPS, Mass_Cost, Energy_Cost, Range, Speed, Faction_ID) VALUES (?,?,?,?,?,?,?,?)"
		cursor.execute(query, (new_unit_name, new_unit_HP, new_unit_DPS, new_unit_MC, new_unit_EC, new_unit_WR, new_unit_MS, new_unit_FAC))
		connection.commit()
		print("\nUnit was added successfully!\n")
	except Exception as error:
		traceback.print_exc()
		print("\nUh oh, couldn't ADD_UNIT, something went wrong!")


def delete_unit(connection, bp):

	'''allows the user to fairly safely remove games from the table'''

	try:

		cursor = connection.cursor()
		query = "SELECT Units_T1_Land.ID, Units_T1_Land.Name FROM Units_T1_Land;"
		cursor.execute(query)
		results = cursor.fetchall()
		print(f"\n{'ID':<5}{'NAME':<40}\n")
		for info in results:
			print(f"{info[0]:<5}{info[1]:<40}")

		choose_del = ask_for_int_value("\nPlease enter the unit ID (number) of the unit you would like to delete: ")

		
		choose_del = user_input_valid_check(1, 1000, choose_del)


		cursor = connection.cursor()
		query = "DELETE FROM Units_T1_Land WHERE ID = ?"
		cursor.execute(query, (choose_del,))
		num_rows_affected = cursor.rowcount
		if num_rows_affected == 0:
			print("\nCould not find and DELETE_UNIT (likely chosen game does not exist)!")
		else:
			connection.commit()
			print("\nChosen unit was deleted successfully!\n")
	except Exception as error:
		traceback.print_exc()
		print("Uh oh, something went wrong while trying to DELETE_UNITS (likely chosen game does not exist)")


# the class is like a template which you can fill lots of data into, when you know there's gonna be a lot of files using the same variables as each other.
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
	FACTION_IDS = {
		"Unknown": 0,
		"UEF": 1,
		"Cybran": 2,
		"Aeon": 3,
		"Seraphim": 4,
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

		self.faction_ID = self.FACTION_IDS[self.faction]

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
		self.is_test_unit = False
		self.faction_ID
		self.id = 0
		self.is_PD = False

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
				except IndexError:
					self.name = desc

			if line.startswith("UnitName"):
				desc = self.value_from_line(line)

				try:
					personal_name = desc.split(">")[1]
					personal_name = personal_name.split("\"")[0]
					self.name = f"{personal_name} ({name})"
					#print(self.name)
				except IndexError:
					self.personal_name = desc

			# all of these elif statements scan the file for information/statistics which can then be assigned to variables and used within the class
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

			#this extra elif statement is because several files randomly use single quotes instead of double quotes
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

			elif "test unit" in self.name.lower():
				self.is_test_unit = True

			elif "point defense" in self.name.lower(): 
				# print("is pd")
				self.is_PD = True
			

			elif line.startswith("RateOfFire = ") and not line.startswith("RateOfFire = {"):
				#print(self.rof)
				self.rof = float(self.value_from_line(line))
				if self.damage != -1:
					if self.code == "XSL0103":
						self.damage *= 5
						# print(f"{self.rof}*{self.damage} (5x projectiles for sera mobile light arty)")
					if self.code == "UAL0106":
						self.damage *= 3
						# print(f"{self.rof}*{self.damage} (3x projectiles for aeon light assault bot)")
					self.DPS += self.rof * self.damage
					self.damage = -1
					self.rof = -1
			

	def value_from_line(self, line):
		value = line.split("=")[1] #get the bit after the '='
		value = value[1:-1] #remove the first and last character (leading space and trailing comma)
		return value

	def __repr__(self):
		return f"{self.code} ({self.name} {self.faction}): {self.mass_cost} mass, {self.energy_cost} energy, {self.health}HP, {self.speed} Speed, {self.DPS}DPS, {self.range} Range, Tech {self.tech_level}, {self.field}, {self.faction_ID}."

def main():
	
	# the following lines locate and scan the database files (where we are extracting the data values from)

	blueprint_path = "bps"

	all_bps = dict()

	blueprint_names = os.listdir(blueprint_path)

	print("\n\nWELCOME to my Supreme Commander database!\n")

	for bp_name in blueprint_names:
		bp = Blueprint(blueprint_path, bp_name)
		
		# if bp.tech_level == "1":

		# 	all_bps[bp.code] = bp
		# 	print(bp)
		#if bp.faction == "UEF":

		
		# this filters for and prints the chosen selection of units from the database which we are using 

		if bp.tech_level == 1 and bp.unit_type == "Land" and bp.is_engi == False and bp.is_test_unit == False or bp.is_PD == True and bp.tech_level == 1:
		#if bp.faction == "UEF" and "Experimental" in bp.name:
			all_bps[bp.code] = bp
			# print(bp)

	while True:
		with sqlite3.connect(TARGET_DATABASE_FILE) as connection:
			cursor = connection.cursor()
			id = 0 

			wipe = "DELETE FROM Units_T1_Land;"
			cursor.execute(wipe)

			for bp in all_bps.values():
				if bp.tech_level == 1 and bp.unit_type == "Land" and bp.is_engi == False or bp.is_PD == True and bp.tech_level == 1:
					id += 1
					bp.id = id
					add_bp_to_db(connection, bp)

			# makes the connection to the chosen database file and then prints all the units chosen through a filter
			user_input = input("\n- [0] test print SELECT * FROM Units_T1_Land\n- [1] Print all units\n- [2] Check the counters for a chosen unit\n- [3] Sort units by a chosen statistic\n- [4] Filter units by chosen faction\n- [5] Insert fully custom unit\n- [6] Delete chosen unit\n- [7] Exit database\n\nEnter Here: ")
			
			# [5] allow user to Insert custom unit data into the database - extra functionality could be cool

			if user_input == "0":
				test_print(connection, bp)

			elif user_input == "1":
				show_units(connection, bp)

			elif user_input == "2":
				check_counter(connection, bp)

				# print unit names and units ids, ask the user to enter the unit id of the unit they want to view matchups for
				# then use the user inputted number to grab the unit counters and descriptions from the matchups table (each counter on a new line)

			elif user_input == "3":
				order_units(connection, bp)

			elif user_input == "4":
				filter_by_faction(connection, bp)

			elif user_input == "5":
	
				add_unit(connection, bp)

			elif user_input == "6":
				
				delete_unit(connection, bp)

			#SELECT Matchup.Description, Counters.Name as Counter_name, This_info.Name as This_name FROM Matchup 
    		#JOIN Units_T1_Land as Counters  ON Matchup.Unit_against_ID=Counters.ID
   			#JOIN Units_T1_Land as This_info ON Matchup.Unit_for_ID=This_info.ID WHERE Matchup.Unit_against_ID = 6

			elif user_input == "7":
				# allows the user to easily exit the program when they want to

				print("\nExiting now - thank you for using my Supreme Commander units database!\n")
				break

			elif user_input == "fish":
				print("\nFish are great, but please enter a valid input sir.")

			else:
				print("\nInvalid input, please try again.")

			#this uses the same filter as above to decide which units get added to the SQL database (the add_bp_to_db function is commented out while not under use)

			
					

			#print(all_bps["UEL0001"].name)

if __name__ == "__main__":
	main()