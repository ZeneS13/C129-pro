from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

start_url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'

page = requests.get(start_url)

soup = bs(page.text,'html.parser')

starTable = soup.find_all('table')

temp_list= []

table_rows = starTable[7].find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text.rstrip() for i in td]
    temp_list.append(row)

StarNames = []
Distance =[]
Mass = []
Radius =[]


for i in range(0,len(temp_list)):
    
    StarNames.append(temp_list[i][0])
    Distance.append(temp_list[i][5])
    Mass.append(temp_list[i][7])
    Radius.append(temp_list[i][8])

df = pd.DataFrame(list(zip(StarNames,Distance,Mass,Radius,)),columns=['Star_name','Distance','Mass','Radius'])
print(df)

df.to_csv('dwarfStar.csv')