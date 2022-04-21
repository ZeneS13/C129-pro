from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import requests
import time

url= "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(url)
planet_data=[]
headers=["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity","detection_method"]
def scrape(): 
    for i in range(0,452):
        soup=BeautifulSoup(browser.page_source,"html.parser")
        all_ul_tags=soup.find_all("ul",attrs={"class","exoplanet"})
        for  ul_tags in all_ul_tags:
            li_tags= ul_tags.find_all("li")

            temp=[]
            for index,data_li in enumerate(li_tags):
                
                if index == 0:
                    temp.append(data_li.find_all("a")[0].contents[0])
                else:
                    try:
                        temp.append(data_li.contents[0])
                    except:
                        temp.append(" ")
    
            
            hyperA=li_tags[0]
            link="https://exoplanets.nasa.gov/"+hyperA.find_all("a",href=True)[0]["href"]
            temp.append(link)
            planet_data.append(temp)
        browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print(f"{i}page 1 done")
    

newPlanetData=[]
def scrapeMoreData(link):
    try:
        page=requests.get(link)
        soup=BeautifulSoup(page.content,"html.parser")
        tempList=[]
        all_tr_tags=soup.find_all("tr",attrs={"class","fact_row"})
        for tr_tag in all_tr_tags:
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    tempList.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])

                except:
                    tempList.append(" ")
        newPlanetData.append(tempList)
    except:
        time.sleep(1)
        scrapeMoreData(link)
scrape()
for index,data in enumerate(planet_data):
    scrapeMoreData(data[5])
    print(f"{index+1}page done 2")

finalData=[]

for index,data in enumerate(planet_data):
    new_planet_data_element=newPlanetData[index]
    new_planet_data_element= [e.replace("\n","") for e in new_planet_data_element]
    new_planet_data_element=new_planet_data_element[:7]
    finalData.append(data+new_planet_data_element)

with open("finalData.csv","w") as f:
    csvw=csv.writer(f)
    csvw.writerow(headers)
    csvw.writerows(finalData)







