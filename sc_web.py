# this is the "routes file"

TARGET_DATABASE_FILE = "supcom.db"

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)



# def check_counter(connection):

# 	# prints out the units table in a nice format, joins data nicely and such

# 		cursor = connection.cursor()
# 		query = """
# 		SELECT This_info.Name as This_name, Counters.Name as Counter_name, Matchup.Description FROM Matchup 
# 		JOIN Units_T1_Land as Counters  ON Matchup.Unit_against_ID=Counters.ID
# 		JOIN Units_T1_Land as This_info ON Matchup.Unit_for_ID=This_info.ID WHERE Matchup.Unit_for_ID = 4
# 		"""
# 		cursor.execute(query)
# 		results = cursor.fetchall()
# 		return results

@app.errorhandler(404) 
  
# inbuilt function which takes error as parameter 
def not_found(e): 
  
# defining function 
  return render_template("404.html") 

@app.route('/')
def home():
	#<section class ="two-column">
	return render_template('home.html')

	#</section>

	# I WANT THIS WORKING WITH GRID, THEN I WANT BUTTONS THAT DO STUFF I NEED THEM TO (how do i get it interacting with DB), THEN I WANNA START USING W3 SCHOOLS STUFF TOO TO SEE HOW IT IS. 


@app.route('/counters/<int:id>')

def unit_counter(id):
	try: 
		with sqlite3.connect(TARGET_DATABASE_FILE) as connection:

		
			#data = check_counter(connection)
			#data = ["- Mantis","- MA12", "- Thaam", "- Aurora"]
			cursor = connection.cursor()

			query = """
			SELECT This_info.Name as This_name, Counters.Name as Counter_name, Matchup.Description FROM Matchup 
			JOIN Units_T1_Land as Counters  ON Matchup.Unit_against_ID=Counters.ID
			JOIN Units_T1_Land as This_info ON Matchup.Unit_for_ID=This_info.ID WHERE Matchup.Unit_for_ID = ?
			"""
			cursor.execute(query, (id,))
			results = cursor.fetchall()
			#return results

			return render_template('counter.html', data=results)
	except:
		return render_template("404.html") 


@app.route('/counters')
def unit_counters():

	with sqlite3.connect(TARGET_DATABASE_FILE) as connection:

	
		#data = check_counter(connection)
		#data = ["- Mantis","- MA12", "- Thaam", "- Aurora"]
		cursor = connection.cursor()


		query = "SELECT Units_T1_Land.ID, Units_T1_Land.Name FROM Units_T1_Land;"

		cursor.execute(query)
		results = cursor.fetchall()
		#return results

		return render_template('counters.html', data=results)
		
@app.route('/sort_units')
def sort_units():
	return render_template('sort_units.html')

@app.route('/filter_factions')
def filter_factions():
	return render_template('filter_factions.html')

@app.route('/add_units')
def add_units():
	return render_template('add_units.html')

@app.route('/delete_units')
def delete_units():
	return render_template('delete_units.html')


if __name__ == '__main__':
    app.run(debug=True)


   