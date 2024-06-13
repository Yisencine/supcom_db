''' this is the "routes file" which contains all the routes for my Supreme Commander DB website, 
which allows the user to see and edit stats and matchup data for Tech 1 land units from the video game.'''

TARGET_DATABASE_FILE = "supcom.db"

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.errorhandler(404) 
def not_found(e): 
	# inbuilt function which takes error as parameter - we can have our error 404 page here.
  
  return render_template("404.html") 

@app.route('/')
def home():
	#<section class ="two-column">
	return render_template('home.html')

	#</section>


@app.route('/counters')
def unit_counters():

	
	# this function allows the user to click buttons which correspond to a unit, and it shows the user the counters to the unit.

	with sqlite3.connect(TARGET_DATABASE_FILE) as connection:

		cursor = connection.cursor()


		query = "SELECT Units_T1_Land.ID, Units_T1_Land.Name FROM Units_T1_Land;"

		cursor.execute(query)
		results = cursor.fetchall()

		return render_template('counters.html', data=results)



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

	# this function will allow the user to add their own custom units and hopefully even add their own custom matchup data to the database

	return render_template('add_units.html')

@app.route('/add_units', methods = ['POST'])
def form():

	response = request.form
	# this function will allow the user to add their own custom units and hopefully even add their own custom matchup data to the database

	return render_template('add_units.html')

@app.route('/delete_units')
def delete_units():

	# this function will allow the user to delete pre-existing and added unit entries, and hopefully corresponding matchup data too

	return render_template('delete_units.html')


if __name__ == '__main__':
	# runs the main function thing
    app.run(debug=True)


   