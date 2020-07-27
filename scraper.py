#!/usr/bin/env python
# coding: utf-8

# ## Web Scraper

# Open the webpage with browser emulator and read the html file:

# In[1]:


import requests
from bs4 import BeautifulSoup

r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content

soup = BeautifulSoup(c,"html.parser")

all = soup.find_all("div", {"class":"propertyRow"})

all[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")


# Iterete into the web page and extract the informations we want from the first page:

# In[12]:


l =[]
for item in all:
    d = {}

    d["Adress"] = item.find_all("span",{"class":"propAddressCollapse"})[0].text
    d["Locality"] = item.find_all("span",{"class":"propAddressCollapse"})[1].text
    d["Price"] = item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
    try:
        d["Beds"] = item.find("span",{"class":"infoBed"}).find("b").text
    except:
        d["Beds"] = None
    try:
        d["Area"] = item.find("span",{"class":"infoSqFt"}).find("b").text
    except:
        d["Area"] = None
    try:
        d["Full Bath"] = item.find("span",{"class":"infoValueFullBath"}).find("b").text
    except:
        d["Full Bath"] = None
    try:
        d["Half Bath"] = item.find("span",{"class":"infoValueHalfBath"}).find("b").text
    except:
        d["Half Bath"] = None
    for column_group in item.find_all("div", {"class":"columnGroup"}):
        for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}), column_group.find_all("span",{"class":"featureName"})):
            if "Lot Size" in feature_group.text:
                d["Lot Size"] = feature_name.text
    l.append(d)


# Import the data in a data frame and save them in a csv file:

# In[15]:


import pandas


# In[17]:


df = pandas.DataFrame(l)


# In[19]:


df.to_csv("Output.csv")


# Extract the informations from several pages:

# In[44]:


base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
l = []
page_nr = soup.find_all("a", {"class":"Page"})[-1].text
for page in range(0, int(page_nr)*10, 10):
    print(base_url+str(page)+".html")
    r = requests.get(base_url+str(page)+".html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c= r.content
    soup = BeautifulSoup(c, "html.parser")
#     print(soup.prettify())
    all = soup.find_all("div", {"class":"propertyRow"})
    for item in all:
        d = {}

        try:
            d["Adress"] = item.find_all("span",{"class":"propAddressCollapse"})[0].text
        except:
            d["Adress"] = None
        try:
            d["Locality"] = item.find_all("span",{"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
        try:
            d["Price"] = item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        except:
            d["Price"] = None
        try:
            d["Beds"] = item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"] = None
        try:
            d["Area"] = item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"] = None
        try:
            d["Full Bath"] = item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Bath"] = None
        try:
            d["Half Bath"] = item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Bath"] = None
        for column_group in item.find_all("div", {"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}), column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        l.append(d)


# In[45]:


import pandas
df= pandas.DataFrame(l)



# In[47]:


df.to_csv("Output.csv")
