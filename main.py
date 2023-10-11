import requests
import datetime
import os
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
News_Api_Key = os.environ['News_Api_Key']
Stock_Api_Key = os.environ['Stock_Api_Key']

yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
before_yesterday= str(datetime.date.today() - datetime.timedelta(days=2))


# fetch stock data
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
Stock_params = {
    "symbol": STOCK,
    "function": "TIME_SERIES_DAILY",
    "apikey": Stock_Api_Key
}
stock_response = requests.get(STOCK_ENDPOINT, params=Stock_params)
stock_data = stock_response.json()

yesterday_close = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])

# fetch two days ago close
two_day_close = float(stock_data["Time Series (Daily)"][before_yesterday]["4. close"])

# calculate difference
price_diff = yesterday_close - two_day_close

if price_diff > 0:
    direction = "🔺"
else:
    direction = "🔻"


abs_diff = abs(price_diff)
percent_change = (abs_diff/two_day_close)*100
fetch_news = False

if percent_change > 4:
    fetch_news = True

News_params = {
    "qInTitle": COMPANY_NAME,
    "apikey": News_Api_Key,
    "sortby": "popularity"
}
news_response = requests.get(NEWS_ENDPOINT, params=News_params)
news_response.raise_for_status()
news_data = news_response.json()

three_articles = news_data["articles"][:3]
formatted_slice = [f"{STOCK}: {direction} %\nHeadline: {article['title']}. \nBreif: {article['description']}"for article in three_articles]


# fetch news
if fetch_news:
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    for article in formatted_slice:
        message = client.messages.create(
            body=article,
            from_='+18449062538',
            to=os.environ['My Phone #']
        )
        print(message.sid)
