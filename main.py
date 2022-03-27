import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY = "M2MDR5DW55LFRRQI"
NEWS_API_KEY = "066dec4d8d8245f9a9932ff9cb81bdf3"
txt = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=TSLA&interval=5min&apikey=M2MDR5DW55LFRRQI"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "outputsize": "full",
    "apikey": API_KEY,
}

today = datetime.today()
yesterday = today - timedelta(days=1)
day_before_yesterday = today - timedelta(days=2)

response = requests.get(STOCK_ENDPOINT, params= stock_params)
js = response.json()

yesterday_date = yesterday.date()
day_before_yesterday_date = day_before_yesterday.date()

try:
    yesterday_closing_price = js['Time Series (Daily)'][str(yesterday_date)]['4. close']
except KeyError:
    yesterday_closing_price = js['Time Series (Daily)'][str(day_before_yesterday_date)]['4. close']
    day_before_yesterday = today - timedelta(days = 3)
    day_before_yesterday_date = day_before_yesterday.date()
    day_before_yesterday_price = js['Time Series (Daily)'][str(day_before_yesterday_date)]['4. close']

day_before_yesterday_price = js['Time Series (Daily)'][str(day_before_yesterday_date)]['4. close']

difference_between_prices = abs(float(yesterday_closing_price) - float(day_before_yesterday_price))

percentage_difference = difference_between_prices / float(yesterday_closing_price) * 100

news_params = {
    "q": "Tesla",
    "apiKey": NEWS_API_KEY,
}

news_response = requests.get(NEWS_ENDPOINT, params=news_params)
news_js = news_response.json()
print(news_js)

news_response = requests.get(NEWS_ENDPOINT, params=news_params)
news_js = news_response.json()

article1_title = news_js["articles"][0]['title']
article1_description = news_js["articles"][0]['description']
article2_title = news_js["articles"][1]['title']
article2_description = news_js["articles"][1]['title']
article3_title = news_js["articles"][2]['title']
article3_description = news_js["articles"][2]['description']

article_list = [article1_title,
                article1_description,
                article2_title,
                article2_description,
                article3_title,
                article3_description]

print(article_list)


def raise_or_decrease():
    if yesterday_closing_price >= day_before_yesterday_price:
        return "🔺"
    else:
        return "🔻"


raise_or_decrease_symbol = raise_or_decrease()

fstring = f"{raise_or_decrease_symbol} + sajt + {raise_or_decrease_symbol}"

message = f"TSLA: {raise_or_decrease_symbol}{round(percentage_difference, 1)}%\n" \
          f"Headline: {article1_title} (TSLA)?.\nBrief: {article1_description}\n" \
          f"Headline: {article2_title} (TSLA)?.\nBrief: {article2_description}\n" \
          f"Headline: {article3_title} (TSLA)?.\nBrief: {article3_description}"

print(message)

message1 = f"TSLA: {raise_or_decrease_symbol}{round(percentage_difference, 1)}%\n" \
          f"Headline: {article1_title} (TSLA)?.\nBrief: {article1_description}\n"

message2 = f"TSLA: {raise_or_decrease_symbol}{round(percentage_difference, 1)}%\n" \
          f"Headline: {article2_title} (TSLA)?.\nBrief: {article2_description}\n"

message3 = f"TSLA: {raise_or_decrease_symbol}{round(percentage_difference, 1)}%\n" \
          f"Headline: {article3_title} (TSLA)?.\nBrief: {article3_description}\n"

def send_news():
    account_sid = 'ACbd9813b45569690fde904d382b0a9f20'
    auth_token = '63ee1595e2244ec98b6569231a7ffd00'
    # proxy_client = TwilioHttpClient()
    # proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token)
    sms_message1 = client.messages \
        .create(
        body=message1,
        from_='+15736853430',
        to='+***********'
    )

    sms_message2 = client.messages \
        .create(
        body=message2,
        from_='+15736853430',
        to='+***********'
    )

    sms_message3 = client.messages \
        .create(
        body=message3,
        from_='+15736853430',
        to='+***********'
    )

if percentage_difference >= 5:
    send_news()
