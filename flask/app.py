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

# import machine learning modules
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import xgboost as xgb
import pickle

#################################################
# Database Setup, either sqlite or postgresql
#################################################

# The SQlite engine
db_file = '/Users/ns96/Documents/ML_Project/SolarCostData.sqlite3'
engine = create_engine("sqlite:///" + db_file)

# RECOMMENDED
#engine = create_engine('postgresql+psycopg2://ns96:java100@localhost/SolarCostData')

# make sure we can connect to the database, otherwise exit
try:
  conn = engine.connect()
  conn.close()
except Exception as e:
  print("DB Connection Error\n")    
  print(e)
  sys.exit()


# dictionary to store the saved scalers and optimzed models
utilities  = ['SDGE', 'PGE', 'SCE']
scalers = dict()
models = dict()

# a lookup table containing the most common generator manufacturer
# used by a installer
generator_table = dict()

# store table which has the three most populat city per zip code
# by utilty
top_zipcodes = {
  'SDGE': ['92130', '92028', '91913'], # san diago, fallbrook, chula vista
  'PGE': ['95648','93727','93311'], # lincoln, fresno, bakersfield
  'SCE': ['92336', '92584', '92223'] # fontana, manifee, BEAUMONT
}

def load_models():
  """
  function to load the meachine learning models
  """
  
  for utility in utilities:
    scaler_file = "../models/scaler-" + utility + ".pkl"
    model_file = "../models/xgb_model-" + utility + ".pkl"

    scalers[utility] = pickle.load(open(scaler_file, "rb"))
    models[utility] = pickle.load(open(model_file, "rb"))


def get_generator_table():
  """
  create a look tables which maps installers to the most common 
  generator they use
  """
  
  query = text('SELECT "Installer_Name", "Generator_Manufacturer", '\
               'COUNT("Generator_Manufacturer"), ROUND(AVG("Generator_Quantity")) '\
               'FROM "CA" '\
               'GROUP BY "Installer_Name", "Generator_Manufacturer" '\
               'HAVING "Installer_Name" != \'Other\' '\
               'ORDER BY "Installer_Name", COUNT("Generator_Manufacturer") DESC')
    
  with engine.connect() as conn:
    results = conn.execute(query).fetchall()    
    
    for row in results:
      installer = row[0]
        
      if installer not in generator_table:
        generator_table[installer] = (row[1], int(row[2]), int(row[3])) 

def get_installers(zip_code = '92130'):
  """
  given a city zip code return the top 10 installers and their average 
  generator install cost and utility
  """
  
  utility_query = text('SELECT "Utility" FROM "CA" WHERE "Service_Zip" = \'' + zip_code + '\' LIMIT 1')
  city_query = 'SELECT "Service_City" FROM "CA" WHERE "Service_Zip" = \'' + zip_code + '\' LIMIT 1'

  query = text('SELECT "Service_City", "Installer_Name", COUNT("Installer_Name"), '\
               'ROUND (AVG("System_Size_AC")), '\
               'ROUND(AVG("Total_System_Cost")) '\
               'FROM "CA" '\
               'WHERE "Service_City" = (' + city_query + ') '\
               'GROUP BY "Service_City", "Installer_Name" '\
               'HAVING "Installer_Name" != \'Other\' '\
               'ORDER BY COUNT("Installer_Name") DESC LIMIT 10')
    
  with engine.connect() as conn:
    # get the untility
    utility = conn.execute(utility_query).fetchall()[0][0]
    
    results = conn.execute(query).fetchall()    
    records = list()
    for row in results:
      records.append(row)
    
  
  # return the utility and installer records 
  return utility, records

def one_hot_encode(df, train_features):
  """
  one hot encode the catigorical variable and add all the columns the 
  scaler/model was trained otherwise things don't work'
  """
  
  cat_columns = df.dtypes[df.dtypes == "object"].index.tolist()
  enc = OneHotEncoder(sparse_output=False)
  enc_data = enc.fit_transform(df[cat_columns])
  enc_columns = enc.get_feature_names_out().tolist()

  encode_df = pd.DataFrame(enc_data, columns=enc_columns)

  # now lets merge the into the main dataframe then drop original columns
  df = df.merge(encode_df, left_index=True, right_index=True)
  df = df.drop(columns=cat_columns)

  # add all the features that the model was trained on 
  # otherwise scaler/model won't work
  for feature in train_features:
    if feature not in df.columns:
      series = pd.Series(0, index=df.index, name=feature)
      df = pd.concat([df, series], axis=1)
    
  # re-order the feature names to be the same as what the scaler 
  # saw during training
  df = df[train_features]
    
  # return the one hot encoded dataframe
  return df

def predict(utility, data):
  """
  make a prediction provided the utility and dictionary containing 
  variable to prediction on
  """
  # load the scaler and model
  scaler = scalers[utility]
  model = models[utility]

  # convert the dictionary into a dataframe 
  df = pd.DataFrame(data)

  # one hot encode the data and scale it
  train_features = scaler.feature_names_in_
  df = one_hot_encode(df, train_features)
  X_scaled = scaler.transform(df)

  # make a prediction now
  return model.predict(X_scaled)

def make_predictions(zipcode, kw, ecar):
  """
  Predict the installation for solar given a zipcode, desired kw
  and if there is an electrical care
  """
  
  #print("KW", kw)
  
  # store the data to make predictions on
  pred_data = {
    'Service_City': [],
    'Technology_Type': [],
    'System_Size_AC': [],
    'Storage_Size_kW_AC': [],
    'Mounting_Method': [],
    'Installer_Name': [],
    'Third_Party_Owned': [],
    'Electric_Vehicle': [],
    'Generator_Manufacturer': [],
    'Generator_Quantity': []
  }

  # store the information to return user along with the estimate
  estimate_data = {
    'Service_City': [],
    'Installer_Name': [],
    'Installation_Count': [],
    'Avg_Size_AC': [],
    'Avg_Cost': [],
    'My_Size_AC': [],
    'eCar': [],
    'Est_Cost': []
  }
    
  # get the utility and top 10 installers for the particular zipcode
  utility, installers = get_installers(zipcode)
    
  for installer in installers:
    # get the most most common generator manufacturer used by installer
    generator_info = generator_table[installer[1]]

    # populate dictionary that gets returned with cost estimates
    estimate_data['Service_City'].append(installer[0])
    estimate_data['Installer_Name'].append(installer[1])
    estimate_data['Installation_Count'].append(installer[2])
    estimate_data['Avg_Size_AC'].append(installer[3])
    estimate_data['Avg_Cost'].append(int(installer[4]))
    estimate_data['My_Size_AC'].append(kw)
    estimate_data['eCar'].append(ecar)
        
    # populate the dictionary with information for making predictions
    pred_data['Service_City'].append(installer[0])
    pred_data['Technology_Type'].append('Solar')
    pred_data['System_Size_AC'].append(float(kw))
    pred_data['Storage_Size_kW_AC'].append(0)
    pred_data['Mounting_Method'].append('Rooftop')
    pred_data['Installer_Name'].append(installer[1])
    pred_data['Third_Party_Owned'].append('No')
    pred_data['Electric_Vehicle'].append(ecar)
    pred_data['Generator_Manufacturer'].append(generator_info[0]) # the most common generator used by installer
    pred_data['Generator_Quantity'].append(int(generator_info[2])) # the average number of the above generator used

  # now return the estimates and append to the dictionary so it can 
  # be turned info a dataframe
  estimates = predict(utility, pred_data)
  estimate_data['Est_Cost'] = [int(x) for x in estimates]

  return estimate_data

def make_predictions_all(kw, ecar):
  """
  Make predictions for the top zipcodes for all utilites
  """
  estimates = []
  
  for key in top_zipcodes:
    zipcode = top_zipcodes[key][0]
    print(key, zipcode)
    
    city_estimates = make_predictions(zipcode, kw, ecar)
    estimates.append(city_estimates)
  
  # merge the diections into one big one
  merged1 = {key: estimates[0][key] + estimates[1][key] for key in estimates[0]}
  merged_estimates = {key: merged1[key] + estimates[2][key] for key in merged1}
  
  #print(str(merged_estimates))
  
  return merged_estimates
  
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
        f"<b>/api/v1.0/zipcodes</b> [ get average install cost by city/zipcodes ]<br/>"
        f"<b>/api/v1.0/estimate/&lt;zipcode&gt;/&lt;kw&gt;/&lt;ecar&gt; </b>[ get cost estimate by zipcode, kw, ecar ]<br/><br/>"
        f"<b>/view </b>[ <a href='/view'> view the basic web UI </a>]<br/>"
    )

@app.route("/api/v1.0/utilities")
def cost_by_utilities():
    """
    Return the avergage install cost by utilities
    """
    query = text('SELECT "Utility", AVG("Total_System_Cost") '\
                 'FROM "CA" GROUP BY "Utility"')
    print(query)
    
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    records = list()
    
    for row in results:
      record = dict()
      record["utility"] = row[0]
      record["avg_cost"] = int(row[1])
      
      records.append(record)
    
    return jsonify(records)

@app.route("/api/v1.0/installers")
def cost_by_installers():
    """ 
    Return the average install cost by installers
    """
    query = text('SELECT "Installer_Name", COUNT("Installer_Name"), '\
                 'AVG("Total_System_Cost") '\
                 'FROM "CA" GROUP BY "Installer_Name"')
    print(query)
    
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    records = list()
    
    for row in results:
      record = dict()
      record["installer"] = row[0]
      record["record_count"] = row[1]
      record["avg_cost"] = int(row[2])
      
      records.append(record)
    
    return jsonify(records)

@app.route("/api/v1.0/cities")
def cost_by_cities():
    """ 
    Return the average install cost by cities
    """
    query = text('SELECT "Service_City", COUNT("Service_City"), '\
                 'AVG("Total_System_Cost") '\
                 'FROM "CA" GROUP BY "Service_City"')
    print(query)
    
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    records = list()
    
    for row in results:
      record = dict()
      record["service_city"] = row[0]
      record["record_count"] = row[1]
      record["avg_cost"] = int(row[2])
      
      records.append(record)
    
    return jsonify(records)

@app.route("/api/v1.0/zipcodes")
def cost_by_zipcodes():
    """ 
    Return the average install cost by zipcodes
    """
    query = text('SELECT "Service_City", "Service_Zip", '\
                 'COUNT("Service_City"), AVG("Total_System_Cost") '\
                 'FROM "CA" GROUP BY "Service_City", "Service_Zip"')
    print(query)
    
    with engine.connect() as conn:
      results = conn.execute(query).fetchall()
    
    records = list()
    
    for row in results:
      record = dict()
      record["service_city"] = row[0]
      record["service_zip"] = row[1]
      record["record_count"] = row[2]
      record["avg_cost"] = int(row[3])
      
      records.append(record)
    
    return jsonify(records)
  
@app.route("/api/v1.0/estimate/<zipcode>/<kw>/<ecar>")
def get_estimate(zipcode, kw, ecar):
    """
    Return an estimate given the zipcode. desired, kwh and technology
    """
    if zipcode != 'all':
      estimates = make_predictions(zipcode, kw, ecar)
    else:
      # make three diffent prediction for three diff utilities then
      # merge dictionaries
      estimates = make_predictions_all(kw, ecar)
    
    return jsonify(estimates)

@app.route("/view")
def view_ui():
    """
    Return the html page to view basic site UI
    """
    
    version = "v1.0.0"
    year = "2018-2023"
    return render_template('index.html', version=version, year=year)

# load ML scalers/models
load_models()

# create a lookup table which maps installer->generators
get_generator_table()

# start the application if it running in the console on port 5015 so localhost
# works on newer macs
if __name__ == '__main__':
  app.run(debug=True, host = '0.0.0.0', port=5015, use_reloader=False)