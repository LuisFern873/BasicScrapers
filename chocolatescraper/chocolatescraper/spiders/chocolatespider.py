import scrapy
from chocolatescraper.items import ChocolateProduct

class ChocolatespiderSpider(scrapy.Spider):
    name = 'chocolatespider'
    allowed_domains = ['chocolate.co.uk']
    start_urls = ['https://www.chocolate.co.uk/collections/all']

    def parse(self, response):

        products = response.css('product-item')

        chocolate = ChocolateProduct()

        for product in products:
            chocolate['name'] = product.css('a.product-item-meta__title::text').get()
            chocolate['price'] = response.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>£','').replace('</span>','')
            chocolate['url'] = product.css('div.product-item-meta a').attrib['href']
            yield chocolate
        
        next_page = response.xpath("//nav[@class='pagination__nav']/a[@rel='next']/@href").get()

        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(next_page_url, callback = self.parse)
        
