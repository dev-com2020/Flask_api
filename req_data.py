import requests
import pandas as pd

csv_file = 'https://static.appseed.us/data/titanic.txt'
r = requests.get(csv_file)
f = open('titanic.csv', 'w')
f.write(r.content.decode('utf-8'))
f.close()

df = pd.read_csv('titanic.csv')
print(df)

