from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
import random
import time
from bs4 import BeautifulSoup
import requests
from currency_converter import CurrencyConverter

scrape_url = 'https://www.amazon.co.uk/Raspberry-Pi-ARM-Cortex-A72-Bluetooth-Micro-HDMI/dp/B07TC2BK1X/ref=sr_1_3?crid=14RXXJE58G8HP&keywords=raspberry+pi+4&qid=1568552215&sprefix=raspberry+%2Caps%2C184&sr=8-3'
headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"
}

class CustomCollector(object):
    def collect(self):
        page_response = requests.get(scrape_url, headers=headers)
        page_content = BeautifulSoup(page_response.content, "html.parser")
        price = page_content.find(id="priceblock_ourprice")
        print(float(price.get_text()[1:]))
        converter = CurrencyConverter()
        price_eur = round(converter.convert(float(price.get_text()[1:]), 'GBP', 'EUR'), 2)
        g = GaugeMetricFamily('amazon_product_price_euro', 'Price of a product on Amazon', labels=['product'])
        g.add_metric(["Raspberry Pi Model 4"], price_eur)
        yield g

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    # Generate some requests.
    while True:
        time.sleep(1)
