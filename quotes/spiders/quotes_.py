import scrapy

class ProductSpider(scrapy.Spider):
    name = 'quotes_'
    start_urls = ['https://www.example.com/product-listing-page']

    async def parse(self, response):
        # Extract product links from the listing page
        product_links = response.css('a.product-link::attr(href)').getall()

        # Limit to 18 products
        for link in product_links[:18]:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_product,
                meta={'playwright': True}
            )

    async def parse_product(self, response):
        # Extract product details
        yield {
            'name': response.css('h1.product-name::text').get(),
            'price': response.css('span.product-price::text').get(),
            'description': response.css('div.product-description::text').get(),
            'rating': response.css('span.product-rating::text').get(),
            'availability': response.css('span.product-availability::text').get(),
            'link': response.url,
        }
