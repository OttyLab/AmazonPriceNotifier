import os
import sys
import requests
from bs4 import BeautifulSoup

if 'SLACK_API_TOKEN' not in os.environ:
    print('slack API token not found')
    sys.exit(1)
elif 'SLACK_CHANNEL_NAME' not in os.environ:
    print('slack channel name not found')
    sys.exit(1)
elif 'PRODUCT_ID' not in os.environ:
    print('product id not found')
    sys.exit(1)
elif 'PRICE' not in os.environ:
    print('price not found')
    sys.exit(1)
else:
    slack_api_token = os.environ['SLACK_API_TOKEN']
    slack_channel_name = os.environ['SLACK_CHANNEL_NAME']
    product_id = os.environ['PRODUCT_ID']
    price = int(os.environ['PRICE'])


agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
header = {
    'User-Agent': agent
}

res = requests.get(f'https://www.amazon.co.jp/dp/{product_id}/', headers=header) #calibarn
soup = BeautifulSoup(res.text, 'html.parser')

elems = soup.select('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole')

if not elems:
    print('element not found')
    sys.exit(1)

current_price = int(elems[0].contents[0].replace(',', ''))

if current_price > price:
    print(f'{current_price} is higher than {price}')
    exit(1)

data = {
    'token': slack_api_token,
    'channel': slack_channel_name,
    'text': f'{price}'
}

res = requests.post('https://slack.com/api/chat.postMessage', data)
print(res)
