import requests
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("API_KEY")
NEWS_URL = "https://newsapi.org/v2/everything"
API_KEY_STOCKPRICE = os.getenv("API_KEY_STOCKPRICE")
STOCK_URL = "https://www.alphavantage.co/query"

company_symbol = "TSLA"
company_symbol= company_symbol.upper()
stock_name = "TESLA"
stock_name = stock_name.title()

API_KEY_STOCKPRICE_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": company_symbol,
    "apikey": API_KEY_STOCKPRICE
}



response_stock = requests.get(STOCK_URL, API_KEY_STOCKPRICE_PARAMS)
response_stock.raise_for_status()


stocks_getprice = response_stock.json()["Time Series (Daily)"]

data_list = [value for (key, value) in stocks_getprice.items()]
yesterday_data = data_list[0]
yesterday_data_closing_price = yesterday_data["4. close"]


day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = day_before_yesterday_data["4. close"]


differance = abs(float(yesterday_data_closing_price) - float(day_before_yesterday_data_closing_price))


diff_percent = (differance/float(yesterday_data_closing_price)) * 100


if diff_percent > 5:

    API_PARAMETER = {
        "q": stock_name,
        "from": datetime.date.today() - datetime.timedelta(days=1),
        "sortBy": "popularity",
        "apiKey": API_KEY,
    }
    response = requests.get(NEWS_URL, params=API_PARAMETER)
    response.raise_for_status()
    news = response.json()
    articles = news["articles"]
    three_articles = articles[:3]

    for stocks in three_articles:
        print(stocks["source"]["name"])
        print(stocks["title"])
        print(stocks["description"])
        print("\n")

else:
    print("All covered up")
