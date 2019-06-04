import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 10000
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/bitcoin_price_update/with/key/bvGy8ZZ91agHmK1LTmFZB1'
IFTTT_WEBHOOKS_SPREADSHEET = 'https://maker.ifttt.com/trigger/add_btc_spreadsheet/with/key/bvGy8ZZ91agHmK1LTmFZB1'



def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    return float(response_json[0]['price_usd'])  

def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)

def post_ifttt_webhook2(event, value):
    data = {'value1' : value}
    ifttt_event_url = IFTTT_WEBHOOKS_SPREADSHEET.format(event)
    requests.post(ifttt_event_url, json=data)

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    return '<br>'.join(rows)

def format_bitcoin_history_G(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        row = '{}: ${}\n'.format(date, price)
        rows.append(row)
    return '\n'.join(rows)

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            post_ifttt_webhook2('add_btc_spreadsheet', format_bitcoin_history_G(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        time.sleep(5 * 60)

if __name__ == '__main__':
    main()