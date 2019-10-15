import requests
import pandas as pd
import numpy as np
import matplotlib
import sqlite3 
home_url = "https://data.nba.net/prod/v1/2019/players/201566_profile.json"

response = requests.get(home_url)
content = response.json()

def convert(tup, di):
    for a, b in tup:
        di.setdefault(a,[]).append(b)
    return di

careerStats = []
careerStatsd = {}
for keys in content["league"]["standard"]["stats"]["careerSummary"].items():
    careerStats += [keys]
convert(careerStats, careerStatsd)


stats_2019 = []
stats_2019d = {}
for keys in content["league"]["standard"]["stats"]["latest"].items():
    stats_2019 += [keys]
convert(stats_2019, stats_2019d)

f = open('russ_career_stats.db', "r") 
lines = f.readlines() 
lines = [[row] for row in lines]
columns = lines[0]
body = lines[1:]  
connection = sqlite3.connect("russ_career_stats.db")
cursor = connection.cursor()  
SQL = """DROP TABLE IF EXISTS russ_career_stats; """

cursor.execute(SQL)

SQL ="""CREATE TABLE russ_career_stats ("""   
for column in columns:       
    SQL =  SQL + column.strip()       
    SQL = SQL + "); "
cursor.execute(SQL)
connection.commit() 

for line in body:
    line = line[0].split(',')
    entry = line.strip() 
    print(entry) 
SQL ="INSERT INTO russ_career_stats VALUES ( "      
for val in entry:         
    SQL += val + ", " 
SQL += ");"         
cursor.execute(SQL)

df = pd.read_sql_query("SELECT * FROM russ_career_stats", connection)

indexes = ["stats"]
careerdf = pd.DataFrame(data = careerStatsd, index = indexes)


df2019_stats = pd.DataFrame(data = stats_2019d, index = indexes)



plt.plot(careerStatsd, indexes)
        
