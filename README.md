# Overview

This is a demonstration project showing the use of Python to interact with a cloud database. I developed this program to gain experience storing data in and querying data from cloud databases. 

The program itself is based on a previous data analysis project I completed. The program performs plotting and statistical comparisons on CBC data for patients with and without COVID. This project moves the locally stored data to a cloud database and includes the following functionality for interacting with the database: querying, modifying, adding, and deleting data. 

When a user requests a plot or statistical comparison, the resulting figure or statistic is displayed and stored locally. The data itself is not held locally - only the figure or statistic. The local data can be cleared to force the program to make a fresh query of the database. This compromise was made to keep querying within the Firestore limits for free use. Additionally, only a subset of the full dataset was uploaded to Firestore due to read/write limits for free use.

[Software Demo Video](http://youtube.link.goes.here)

# Original Data Citation

FAPESP (2020). FAPESP COVID-19 Data Sharing/BR, Available from https://repositoriodatasharingfapesp.uspdigital.usp.br/

# Cloud Database

The cloud database for this project is a Firestore database with Cloud Firestore. Firestore is a NoSQL database.

The database is structured into two primary collections: 
* TestUnits
    * This collection has two documents: Patient and CBC. Each document contains a map with key-value pairs, where each key is the parameter associated with the document and the value is the units of measure used for that parameter.
    * Ex: Patient document has five fields: Age, COVID, Date, ID, and Sex.
* TestResults
    * This collection contains a unique document for each test result. A document contains the map of each patient field and a nested map with the results for each analyte in a CBC.

# Development Environment

* Visual Studio Code v1.63.2

* Python 3.9.7
    * Pandas v1.4.0
    * SciPy v1.7.3
    * NumPy v1.22.1
    * Matplotlib v3.5.1
    * Google-Cloud-Firestore v2.3.4

# Useful Websites

* [Get to know Cloud Firestore - Firebase YouTube playlist](https://youtube.com/playlist?list=PLl-K7zZEsYLluG5MCVEzXAQ7ACZBCuZgZ)
* [Google Cloud Firestore Documentation](https://cloud.google.com/firestore/docs)
* [Google Cloud Firestore Python Client](https://googleapis.dev/python/firestore/latest/index.html)
* [Python Documentation, v.3.9](https://docs.python.org/3.9/)
* [Pandas Documentation, v1.4.0](https://pandas.pydata.org/docs/index.html)
* [SciPy Documentation, v1.7.3](https://docs.scipy.org/doc/scipy/index.html#)
* [NumPy Documentation, v1.22](https://numpy.org/doc/stable/)
* [Matplotlib Documentation, v3.5.1](https://matplotlib.org/stable/index.html)

# Future Work

* Improve database structure to reduce number of queries in each request.
* Expand database to include additional lab tests.
* Improve statistical test options to include t-test if data is normally distributed and one-tailed options.
* Improve data upload functions to ensure data is in a valid format.
* Add function to batch upload new data from a file.
* Add logging for queries.