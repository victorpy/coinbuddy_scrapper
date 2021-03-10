import requests
import bs4 as BeautifulSoup
import csv
import time

""" 
 v1 should be lower than v2 to calculate increase
""" 

def percentageIncreaseChangeCalculator(v1, v2):

    if v1 == 0:
        return 0

    change = ((v2-v1)/v1) * 100

    return change


COINBUDDY_URL = 'https://coinbuddy.co'
SLEEP_TIME = 1


with open('coin_href_list_4.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

lowest = 999999.99
highest = 0.0
exchangeLowest = ''
exchangeHighest = ''
currentPrice = 0

for d in data:

    lowest = 999999.99
    highest = 0.0
    exchangeLowest = ''
    exchangeHighest = ''
    currentPrice = 0

    currentPage = COINBUDDY_URL+d[0]
    print("START "+currentPage)

    try: 
        page = requests.get(currentPage, timeout=6)
    except requests.exceptions.Timeout:
        print("Request timeout for : "+currentPage)
        exit(1)
 

    soup = BeautifulSoup.BeautifulSoup(page.content, 'html.parser')

    """ 
    there are two tables with class table-exchanges, we want to use the second 
    """

    result = soup.find_all("table", class_="table-exchanges")

    if len(result) > 1:
        table = result[1]
    else :
        table = result[0]

    #print(table.prettify())
    exchange = ""

    for row in table.find_all('tr'):
        columns = row.find_all('td')

        try:
            
            """ the first columns elemnts of this table contains the exchange name """
            if columns[0].has_attr("rowspan"):
                if columns[0].find('a'):
                    exchange = columns[0].get_text()

                    if columns[1].get_text() == "USDT":
                        #print("Exchange "+exchange)
                        #print("Buy with "+columns[1].get_text())
                        #print("Exchange %s Price %s" % (exchange, columns[2].get_text()))
                        currentPrice = float(columns[2].get_text().replace('$', '').replace(',',''))
            else:
                     if columns[0].get_text() == "USDT":
                        #print("Exchange "+exchange)
                        #print("Buy with "+columns[0].get_text())
                        #print("Price "+columns[1].get_text())
                        currentPrice = float(columns[1].get_text().replace('$', '').replace(',',''))

            if lowest > currentPrice and currentPrice > 0.0:
                #print("Current low: %.4f" % currentPrice)
                lowest = currentPrice
                exchangeLowest = exchange

            if highest < currentPrice:
                #print("Current high: %.4f" % currentPrice)
                highest = currentPrice
                exchangeHighest = exchange
            
        except IndexError:
            print("Index error, continue")
            continue

    print("Exchange %s Lowest %.4f " % (exchangeLowest, lowest))
    print("Exchange %s Highest %.4f " % (exchangeHighest, highest))

    print("Percentage increase: %.4f " % percentageIncreaseChangeCalculator(lowest, highest))

    print("END "+currentPage)
    time.sleep(SLEEP_TIME)
