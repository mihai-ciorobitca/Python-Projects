import scrapy
from json import dump

class ProductSpider(scrapy.Spider):
    name = 'laptop' # replace with another product you want to crawl
    allowed_domains = ['emag.ro']
    start_urls = [f'https://www.emag.ro/search/{name}']
    products = []

    def parse(self, response):
        for product in response.css('div.card-v2-wrapper.js-section-wrapper'):
            product_info = {
                'description': product.css('a.card-v2-title.semibold.mrg-btm-xxs.js-product-url::text').get(),
                'price': product.css('p.product-new-price::text').get(),
                'link': product.css('a.card-v2-title.semibold.mrg-btm-xxs.js-product-url::attr(href)').get(),
            }
            self.products.append(product_info)
        next_page = response.css('a[aria-label=Next]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        with open(f'{self.name}.json', 'w') as file:
            dump(self.products, file)