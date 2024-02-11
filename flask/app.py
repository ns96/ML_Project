# Basic flask app for accessing the The Distributed Generation 
# Interconnection Data Sets which provides information on Solar and 
# Battery storage information

# @author Nathan Stevens
# @version 1.0 02/06/2024

# Import the dependencies.
import sys
from sqlalchemy import create_engine, text
from flask import Flask, jsonify, render_template
from flask_cors import CORS

#################################################
# Database Setup, either sqlite or postgresql
#################################################

# The SQlite engine
#db_file = '/Users/ns96/Documents/ML_Project/SolarCostData.sqlite3'
#engine = create_engine("sqlite:///" + db_file)

# RECOMMENDED
engine = create_engine('postgresql+psycopg2://ns96:java100@localhost/SolarCostData')

# make sure we can connect to the database, otherwise exit
try:
  conn = engine.connect()
  conn.close()
except Exception as e:
  print("DB Connection Error\n")    
  print(e)
  sys.exit()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    
    return (
        f"<b>Available Routes:</b><br/><br>"
        f"<b>/api/v1.0/utilities</b> [ get average install cost by utility ]<br/>"
        f"<b>/api/v1.0/installers</b> [ get average install cost by installers ]<br/>"
        f"<b>/api/v1.0/cities</b> [ get average install cost by cities ]<br/>"
        f"<b>/api/v1.0/zipcodes</b> [ get average install cost by zipcodes ]<br/>"
        f"<b>/api/v1.0/city/&lt;city&gt</b> [ get average install cost for a city ]<br/>"
        f"<b>/api/v1.0/zipcode/&lt;zipcode&gt</b> [ get average install cost for zip code ]<br/>"
        f"<b>/api/v1.0/estimate/&lt;zipcode&gt;/&lt;kw&gt;/&lt;ecar&gt; </b>[ get cost estimate by zipcode, kw, ecar ]<br/><br/>"
        f"<b>/view </b>[ <a href='/view'> view the basic web UI </a>]<br/>"
    )

@app.route("/api/v1.0/utilities")
def cost_by_utilities():
    """
    Return the avergage install cost by utilities
    """
    query = text('')
    print(query)
    
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    records = dict()
    
    for row in results:
      record = dict()
      record["state"] = row[0]
      record["count"] = row[1]
      record["discharges"] = row[2]
      record["avg_payments"] = int(row[3])
      record["avg_medicare"] = int(row[4])
      record["avg_difference"] = int(row[3] - row[4])
      
      # calcuate the percent medicare payments
      pct = int((row[4]/row[3])*100)
      record["pct_medicare"] = pct
      
      records[row[0]] = record # add to dictionary
    
    return jsonify(records)

@app.route("/api/v1.0/installers")
def cost_by_installers():
    """ 
    Return the average install cost by installers
    """
    query = text('SELECT "Category", COUNT(*) '\
                 'FROM "DRG" '\
                 'GROUP BY "Category" '\
                 'ORDER BY COUNT(*) DESC')
    print(query)
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    categories = []
    for row in results:
      categories.append({row[0]: row[1]})
    
    return jsonify(categories)

@app.route("/api/v1.0/cities")
def cost_by_cities():
    """ 
    Return the average install cost by cities
    """
    query = text("")
    print(query)
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    definitions = []
    for row in results:
      definition = dict()
      definition["value"] = row[0]
      definition["text"] = row[1]
      definitions.append(definition)
    
    return jsonify(definitions)

@app.route("/api/v1.0/zipcodes")
def cost_by_zipcodes():
    """ 
    Return the average install cost by zipcodes
    """
    query = text("")
    print(query)
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    definitions = []
    for row in results:
      definition = dict()
      definition["value"] = row[0]
      definition["text"] = row[1]
      definitions.append(definition)
    
    return jsonify(definitions)

@app.route("/api/v1.0/city/<city>")
def cost_for_city(city):
    """ 
    Return the average install cost for a particular city
    """
    query = text("")
    print(query)
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    definitions = []
    for row in results:
      definition = dict()
      definition["value"] = row[0]
      definition["text"] = row[1]
      definitions.append(definition)
    
    return jsonify(definitions)

@app.route("/api/v1.0/zipcode/<zipcode>")
def cost_for_zipcode(zipcode):
    """
    Return the average install cost for a particular zipcode
    """
    query = text('')
    
    print(query)
    
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    providers = []
    for row in results:
      provider = dict()
      
      provider["state"] = row[0]
      provider["name"] = row[1]
      provider["drg_count"] = row[2]
      provider["discharges"] = row[3]
      provider["avg_payments"] = int(row[4])
      provider["avg_medicare"] = int(row[5])
      provider["avg_difference"] = int(row[4] - row[5])
      
      # calcuate the percent medicare payments
      pct = int((row[5]/row[4])*100)
      provider["pct_medicare"] = pct
      provider["latitude"] = row[6]
      provider["longitude"] = row[7]
      
      providers.append(provider)
    
    return jsonify(providers)
  
@app.route("/api/v1.0/estimate/<zipcode>/<kw>/<ecar>")
def get_estimate(zipcode, kw, ecar):
    """
    Return an estimate given the zipcode. desired, kwh and technology
    """
    query = text('SELECT COUNT(*) FROM "CA"')
    print(query)
    
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    estimates = []
    for row in results:
      estimate = dict()
      
      estimate["cost"] = row[0]
      estimates.append(estimate)
    
    return jsonify(estimates)

@app.route("/view")
def view_ui():
    """
    Return the html page to view basic site UI
    """
    
    version = "v1.0.0"
    year = "2018-2023"
    return render_template('index.html', version=version, year=year)

# start the application if it running in the console on port 5015 so localhost
# works on newer macs
if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port=5015, use_reloader=False)