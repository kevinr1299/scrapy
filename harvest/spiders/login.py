import os

from scrapy import FormRequest, Spider


class LoginSpider(Spider):
    name = 'login'
    allowed_domains = [os.environ['HARVEST_DOMAIN']]
    start_urls = [
        f'https://{os.environ["HARVEST_DOMAIN"]}/{os.environ["HARVEST_LOGIN"]}',
    ]

    def parse(self, response):
        token = response.css(
            'input[name="authenticity_token"]::attr(value)'
        ).extract_first()
        product = response.css(
            'input[name="product"]::attr(value)'
        ).extract_first()
        form = response.css(
            'form::attr(action)'
        ).extract_first()
        data = {
            'authenticity_token': token,
            'product': product,
            'email': os.environ['HARVEST_USER'],
            'password': os.environ['HARVEST_PASS'],
        }
        yield FormRequest(
            url=f'https://{os.environ["HARVEST_DOMAIN"]}{form}',
            formdata=data,
            callback=self.parse_schedule,
        )

    def parse_schedule(self, response):
        print(response.body)
