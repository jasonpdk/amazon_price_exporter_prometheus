from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
import time
from bs4 import BeautifulSoup
import requests
from currency_converter import CurrencyConverter

scrape_urls = [
        'https://www.amazon.co.uk/Raspberry-Pi-ARM-Cortex-A72-Bluetooth-Micro-HDMI/dp/B07TC2BK1X/ref=sr_1_3?crid=14RXXJE58G8HP&keywords=raspberry+pi+4&qid=1568552215&sprefix=raspberry+%2Caps%2C184&sr=8-3'
]

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"
}

class CustomCollector(object):
    def collect(self):
        g = GaugeMetricFamily('amazon_product_price_euro', 'Price of a product on Amazon', labels=['product'])
        for url in scrape_urls:
            page_response = requests.get(url, headers=headers)
            page_content = BeautifulSoup(page_response.content, "html.parser")
            title = page_content.find(id="productTitle").get_text().strip()
            price = float(page_content.find(id="priceblock_ourprice").get_text()[1:])
            converter = CurrencyConverter()
            price_eur = round(converter.convert(price, 'GBP', 'EUR'), 2)
            g.add_metric([title], price_eur)
        yield g

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    # Generate some requests.
    while True:
        time.sleep(1)
