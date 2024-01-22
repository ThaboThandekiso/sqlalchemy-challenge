# sqlalchemy-challenge

## The solution for this challenge is presented in the following structure:

1) ../README.md (this file).
2) ../SurfsUp = Folder containing the application files:
    2.1) ../SurfsUp/Resources/ = Folder containg the source data:
    - hawaii.sqlite = File containing the database used in this analysis.
    - hawaii_measurements.csv = Table "measurements" from "hawaii.sqlite" in CSV format.
    - hawaii_stations.csv = Table "stations" from "hawaii.sqlite" in CSV format.
    note: no CSV is used by this program, tables for reference only.

    2.2) ../SurfsUp/climate_starter.ipynb = Notebook-Python file containing the 1St part of the challenge:
    - Setup of the Database connection.
    - Initialization and set up of the Flask App.
    - Queries and convertions to Panda's Dataframes.
    - Plots of (Matplotlib and Pandas.plot) required graphics.

    2.3) ../SurfsUp/app.py = Python file containing the 2nd part of the challenge:
    - Setup of the Database connection.
    - Initialization and set up of the Flask App.
    - Definitions of Routes and its functions.

## Considerations:
- The year (or 12 months) periods to be considered in this program include the same day of the previous year, example: if the last date of the period is 23-aug-2017, the start date will be set as 23-aug-2016 (not 24-aug-2016).
- For the exploratory precipitation analysis, the null values have been dropped out of the dataframe before the output results (graphic and decription).