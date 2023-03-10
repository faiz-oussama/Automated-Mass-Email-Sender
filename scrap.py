from bs4 import BeautifulSoup
import requests
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

base_url = 'https://www.thewhiskyexchange.com'

productlinks = []

for x in range(1,3):
    content = requests.get('https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={}'.format(x)).text
    soup = BeautifulSoup(content, 'lxml')
    products = soup.find_all("li" , {"class":"product-grid__item"})
    
    
    for product in products:
        link = product.find("a",{"class":"product-card"}).get('href')
        productlinks.append(base_url + link)


product_names = []
Volume = []
alcohool_percentage = []
Price = []
Price_per_Litre = []
Reviews = []

for link in productlinks:

    content = requests.get("{}".format(link)).text
    soup = BeautifulSoup(content,'lxml')

    #Extracting product's names

    name = soup.find("h1",{"class":"product-main__name"})
    product_names.append(name.text)

    for i in range(0,len(product_names)):
        product_names[i] = product_names[i].replace('\n','')

    #Alchool's percentage

    percentage = soup.find("p",{"class":"product-main__data"})
    alcohool_percentage.append(percentage.text.split()[-1])

    #Volume

    v = soup.find("p",{"class":"product-main__data"})
    Volume.append(v.text.split()[0])

    #Price

    price = soup.find("p",{"class":"product-action__price"})
    Price.append(price.text)


    #reviews
        
    try:
        review = soup.find("div", {"class":"review-overview"}).text.replace('\n','') 
        Reviews.append(review)
    except:
        review = 'None'
        Reviews.append(review)




    #price per litre
    
    price_litre = soup.find("p",{"class":"product-action__unit-price"})
    Price_per_Litre.append(price_litre.text)

    for i in range(0,len(Price_per_Litre)):
        Price_per_Litre[i] = Price_per_Litre[i].replace('(','')
        Price_per_Litre[i] = Price_per_Litre[i].replace(')','')
        Price_per_Litre[i] = Price_per_Litre[i].replace('per litre','')
        Price[i] = Price[i].replace('[','') 
        Price[i] = Price[i].replace(']','') 

df = pd.DataFrame(list(zip(product_names,Price,Volume,Price_per_Litre,alcohool_percentage,Reviews)),columns = ['Name','Price','Volume','Price/Litre','Alcohol %','Rating'])
df['Rating'] = df['Rating'].str.extract('(\d+(?:\.\d+)?)', expand=False).astype(float)


file_name = 'E-commerce site.xlsx'
df.to_excel(file_name)
