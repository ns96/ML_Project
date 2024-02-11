# Solar Installation Cost Modeling

Making use of machine learning techniques to predict the cost of installing solar panels on residential homes in California.

## Description

Predictive models that leverages factors like location, utility company, installer, and desired kwh were trained and deployed. The California [Distributed Generation  Interconnection Data Sets](https://www.californiadgstats.ca.gov/downloads/) consisting of over 1M records was used. After cleaning and normalizing the data, models were trained on 410K records and up to 1173 features after one-hot-encoding the categorial variables. The machine learning techniques employed were XGBoost, Random Forest, and TensorFlow Neural Networks. These models allow for identifying which utility/installers offers the best value for solar panel installation, based on desired power output and location. In addition a simple Flask based interactive website was developed to show case model deployment and use. 

![Utilities Map](images/map.png)
[Interactive Map](https://public.tableau.com/views/SolarCostMap/Map?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link)

## Getting Started

### Dependencies for Machine Learning Jupyter Notebooks
1. Scikit-Learn
2. XGBoost

### Dependencies for Flask web-app
1. Flask
2. Flask-CORS
3. SQLAlchemy
4. PostgreSQL or SQlite3


### Clean Dataset and Database Files
1. [Solar Cost Data](https://github.com/ns96/ML_Project/releases/tag/v1.0)

### Installing Database Files 

Database Files Importing.
* PostgresSQL (recommended): 
	1. Using pgAdmin create a database called "SolarCostData"
	2. Run the QuickDBD-SQL.sql
	4. update the flask/app.py with the proper credentials for the PostgreSQL database. Make sure to uncomment this line, and comment the SQLite line.
* SQlite:
	1. Edit the app.py file to point to the location where the SolarCostData.sqlite3 files was installed.

### Executing Flask backend

1. Download source code from GitHub
2. Change to "installation location"/flask directory
3. Execute "python app.py"
4. Open http://localhost:5015/view in Browser 

## Model Performance
?????

## Conclusions

## Authors

Contributors names and contact info

* Elena Lomako
* Cameron Cullen
* Eric Llorente
* Nathan Stevens 

## Version History
* 1.0.2
    * Bug fix for running on Windows
* 1.0.0
    * Initial Release


## License

This project is licensed under the GPL License


## Acknowledgments
Various tutorials, frameworks, libraries, and database tools/engines used:

* [scikit-learn](https://scikit-learn.org/stable/index.html)
* [XGBoost](https://xgboost.ai/)
* [Tableau Public](https://www.tableau.com/products/public)
* [Flask Micro Framework](https://flask.palletsprojects.com/en/3.0.x/)
* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) 
* [Leaflet](https://leafletjs.com/)
* [Plotly](https://plotly.com/javascript/)
* [Grid.js](https://gridjs.io/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [SQlite3](https://www.sqlite.org/index.html)
* [SQLiteStudio](https://sqlitestudio.pl/)
* [DB Browser for SQLite](https://sqlitebrowser.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Dumping PostgreSQL DB](https://www.netguru.com/blog/how-to-dump-and-restore-postgresql-database). On MacOs you may need to run 'export PATH=$PATH:/Library/PostgreSQL/16/bin'
* [Home SRFT -> Kwh](https://www.lifestylesolarinc.com/blog/how-many-kwh-does-a-house-use-per-day)

