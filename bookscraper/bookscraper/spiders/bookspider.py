import scrapy
from bookscraper.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                next_page_url = 'https://books.toscrape.com/' + relative_url
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(next_page_url, callback = self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is None:
            pass

        if 'catalogue/' in next_page:
            next_page_url = 'https://books.toscrape.com/' + next_page
        else:
            next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        yield response.follow(next_page_url, callback = self.parse)
    
    def parse_book_page(self, response):

        book = BookItem()

        table = response.css('table tr')

        book['url'] = response.url
        book['title'] = response.css('article.product_page h1::text').get()
        book['product_type'] = table[1].css('td::text').get()
        book['price_excl_tax'] = table[2].css('td::text').get()
        book['price_incl_tax'] = table[3].css('td::text').get()
        book['tax'] = table[4].css('td::text').get()
        book['availability'] = table[5].css('td::text').get()
        book['num_reviews'] = table[6].css('td::text').get()
        book['stars'] = response.css('p.star-rating').attrib['class']
        book['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book['description'] = response.xpath("//div[@id='product_description']/following-sibling::p[1]/text()").get()
        book['price'] = response.css('p.price_color ::text').get()

        yield book
