import requests
import bs4 as BeautifulSoup
import time
import csv 


COINBUDDY_URL = 'https://coinbuddy.co/coins'

hrefList = []

startPage = 4
maxPages = 5
SLEEP_TIME = 2

for i in range(startPage,maxPages+1):

    if(i == 1):
        page = requests.get(COINBUDDY_URL)
        print(COINBUDDY_URL)
    else:
        page = requests.get(COINBUDDY_URL+"?page="+str(i))
        print(COINBUDDY_URL+"?page="+str(i))

    soup = BeautifulSoup.BeautifulSoup(page.content, 'html.parser')
    table = soup.find(id='coin-table')

    """ 
    Get the data from the table of current page
    """

    for row in table.find_all('tr'):
        columns = row.find_all('td')
        for column in columns:
            a = column.find('a', href=True)
            
            if a is not None: 
                print("href ", a['href'])
                hrefList.append([a['href']])
            
            print(column.get_text())

    time.sleep(SLEEP_TIME)


# opening the csv file in 'w+' mode 
file = open('coin_href_list_4.csv', 'w+', newline ='') 
# writing the data into the file 
with file:     
    write = csv.writer(file) 
    write.writerows(hrefList) 
    
