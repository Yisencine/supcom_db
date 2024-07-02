''' this is the "routes file" which contains all the routes for my Supreme Commander DB website, 
which allows the user to see and edit stats and matchup data for Tech 1 land units from the video game.'''

TARGET_DATABASE_FILE = "supcom.db"

class data:
	counters = 0
	reset_counters = True
	add_units_submitted = False
	response = {}

from flask import Flask, render_template, request, redirect
import sqlite3

def error_proofing(user_value, lower_bound, upper_bound):

	# function that sanitises user input to make sure that they enter a valid number into parts of my program which require integers, without crashing the program
	try:
		int(user_value)

		if not len(user_value):
			print("too short")
			return False

		if int(user_value) > upper_bound or int(user_value) < lower_bound:
			print("boundary error", user_value, upper_bound, lower_bound)
			return False
			
		return True
	except:
		print("no number")
		return False


app = Flask(__name__)

@app.errorhandler(404)
def not_found(e): 
	# inbuilt function which takes error as parameter - we can have our error 404 page here.
  
  return render_template("404.html") 

@app.route('/')
def home():
	#<section class ="two-column">
	with sqlite3.connect(TARGET_DATABASE_FILE) as connection:
		cursor = connection.cursor()
		query = """SELECT Units_T1_Land.Name, Units_T1_Land.Health, Units_T1_Land.DPS, Units_T1_Land.Mass_Cost, Units_T1_Land.Energy_Cost, 
		Units_T1_Land.Range, Units_T1_Land.Speed, Faction.Faction_Name FROM Units_T1_Land JOIN Faction ON Units_T1_Land.Faction_ID=Faction.ID;"""
		cursor.execute(query)
		results = cursor.fetchall()

		return render_template('home.html', units = results)

		#</section>


@app.route('/counters')
def unit_counters():

	
	# this function allows the user to click buttons which correspond to a unit, and it shows the user the counters to the unit.
	try: 
		with sqlite3.connect(TARGET_DATABASE_FILE) as connection:

			cursor = connection.cursor()


			query = "SELECT Units_T1_Land.ID, Units_T1_Land.Name FROM Units_T1_Land;"

			cursor.execute(query)
			results = cursor.fetchall()

			return render_template('counters.html', data=results)

	except:
		return render_template("404.html") 



@app.route('/counters/<int:id>')
def unit_counter(id):

	# this function is the one that displays the individual pages of unit matchups with a dynamic route system

	try: 
		with sqlite3.connect(TARGET_DATABASE_FILE) as connection:

			cursor = connection.cursor()

			query = """
			SELECT This_info.Name as This_name, Counters.Name as Counter_name, Matchup.Description FROM Matchup 
			JOIN Units_T1_Land as Counters  ON Matchup.Unit_against_ID=Counters.ID
			JOIN Units_T1_Land as This_info ON Matchup.Unit_for_ID=This_info.ID WHERE Matchup.Unit_for_ID = ?
			"""
			cursor.execute(query, (id,))
			results = cursor.fetchall()

			return render_template('counter.html', data=results)
	except:
		return render_template("404.html") 

@app.route('/sort_units/<int:stat>')
def sort_units(stat):

	# this function will allow the user to select a statistic to sort by on the website

	try: 
		with sqlite3.connect(TARGET_DATABASE_FILE) as connection:

			column_names = ['Units_T1_Land.Health', 'Units_T1_Land.DPS', 'Units_T1_Land.Mass_Cost', 'Units_T1_Land.Energy_Cost', 'Units_T1_Land.Range', 'Units_T1_Land.Speed', 'Faction.Faction_Name']
			cursor = connection.cursor()
			query = f"""
				SELECT Units_T1_Land.Name, Units_T1_Land.Health, 
				Units_T1_Land.DPS, Units_T1_Land.Mass_Cost, 
				Units_T1_Land.Energy_Cost, Units_T1_Land.Range, 
				Units_T1_Land.Speed, Faction.Faction_Name 
				FROM Units_T1_Land JOIN Faction ON Units_T1_Land.Faction_ID=Faction.ID ORDER BY {column_names[int(stat) - 1]};"""

			cursor.execute(query)
			results = cursor.fetchall()

			return render_template('sort_units.html', stat = stat, data=results)

	except:
	 	return render_template("404.html") 


@app.route('/filter_factions/<int:fac>')
def filter_factions(fac):

	faction_column_names = ['UEF', 'Cybran', 'Aeon', 'Seraphim']
	# this function will allow the user to select one of four factions to filter by (and only show them those units and their stats)
	try:
		with sqlite3.connect(TARGET_DATABASE_FILE) as connection:
			cursor = connection.cursor()
			query = """
				SELECT Units_T1_Land.Name, Units_T1_Land.Health, 
				Units_T1_Land.DPS, Units_T1_Land.Mass_Cost, 
				Units_T1_Land.Energy_Cost, Units_T1_Land.Range, 
				Units_T1_Land.Speed, Faction.Faction_Name 
				FROM Units_T1_Land JOIN Faction ON Units_T1_Land.Faction_ID=Faction.ID WHERE Faction.Faction_Name = ?;"""
			cursor.execute(query, (faction_column_names[int(fac) - 1],))
			results = cursor.fetchall()

	except:
	  	return render_template("404.html") 

	

	return render_template('filter_factions.html', fac = fac, data=results)


@app.route('/add_units')
def add_units():
	if data.reset_counters:
		 data.counters = 0
	data.reset_counters = True

	# this function will allow the user to add their own custom units and hopefully even add their own custom matchup data to the database

	with sqlite3.connect(TARGET_DATABASE_FILE) as connection:
		cursor = connection.cursor()
		query = "SELECT Units_T1_Land.ID, Units_T1_Land.Name FROM Units_T1_Land;"
		cursor.execute(query)
		results = cursor.fetchall()




	return render_template('add_units.html', counters=data.counters, units = results, response=data.response)


@app.route('/add_units', methods = ['POST'])
def add_units_submitted():

	submission_error = False
	

	response = list(request.form)
	if response[0] == "add counter":  # user wants to add a counter
		data.counters += 1
	else:
		response = request.form
		print(response)


		if not error_proofing(response['Health'], 0, 50):
			submission_error = True
		if not error_proofing(response['DPS'], 0, 10000):
			submission_error = True
		if not error_proofing(response['Mass_Cost'], 0, 500000):
			submission_error = True
		if not error_proofing(response['Energy_Cost'], 0, 20000000):
			submission_error = True
		if not error_proofing(response['Range'], 0, 250):
			submission_error = True
		if not error_proofing(response['Speed'], 0, 50):
			submission_error = True

			print(response)

			# need to stop fac ID input from crashing but also tell the user what is wrong.
		if not 'Faction_ID' in response:
			submission_error = True
		elif not error_proofing(response['Faction_ID'], 0, 5):
			submission_error = True

		if submission_error:
			data.reset_counters = False
			data.response = response
			return redirect("add_units#bottom")
			submission_error = False
		
			# user_input_valid_check(1, 4, response)

		with sqlite3.connect(TARGET_DATABASE_FILE) as connection:
			cursor = connection.cursor()
			query = "INSERT INTO Units_T1_Land(Name, Health, DPS, Mass_Cost, Energy_Cost, Range, Speed, Faction_ID) VALUES (?,?,?,?,?,?,?,?)"
			cursor.execute(query, (response["Name"], response["Health"], response["DPS"], response["Mass_Cost"], response["Energy_Cost"], response["Range"], response["Speed"], response["Faction_ID"]))

			unit_name = response["Name"]
			query = f"SELECT ID FROM Units_T1_Land WHERE Name = '{unit_name}';"
			cursor.execute(query)
			new_id = cursor.fetchall()[0][0]
			
			


			# all info gets reset when + button gets clicked

			for counter in range(data.counters):
				query2 = "INSERT INTO Matchup(Unit_for_ID, Unit_against_ID, Description) VALUES (?,?,?)"
				cursor.execute(query2, (new_id, response[f"counter_name{counter}"], response[f"counter_description{counter}"]))

			connection.commit()
		data.counters = 0

	response = request.form


	
	# print(response["Faction_ID"])
	# this function will allow the user to add their own custom units and hopefully even add their own custom matchup data to the database
	# return render_template('add_units.html', counters=data.counters)

	data.reset_counters = False
	data.response = response

	return redirect("add_units#bottom")

@app.route('/delete_units')
def delete_units():

	# this function will allow the user to delete pre-existing and added unit entries, and hopefully corresponding matchup data too
	with sqlite3.connect(TARGET_DATABASE_FILE) as connection:
		cursor = connection.cursor()
		query = "SELECT Units_T1_Land.ID, Units_T1_Land.Name FROM Units_T1_Land;"
		cursor.execute(query)
		results = cursor.fetchall()

	return render_template('delete_units.html', units = results)

@app.route('/delete_units', methods = ['POST'])
def delete_units_submitted():

	with sqlite3.connect(TARGET_DATABASE_FILE) as connection:
		cursor = connection.cursor()
		response = request.form
		query = "DELETE FROM Units_T1_Land WHERE ID = ?"
		cursor.execute(query, (response["unit_name"],))

	return redirect("/delete_units")

if __name__ == '__main__':
	# runs the main function thing
    app.run(debug=True)


   