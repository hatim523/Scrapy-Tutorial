import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").get(),
                'author': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall(),
            }

        next_links = response.css(".next a::attr(href)").getall()
        authors_found = response.css("span a::attr(href)").getall()
        for link in next_links:
            yield response.follow(link, callback=self.parse)

        for author in authors_found:
            yield response.follow(author, callback=self.parse_authors)

    def parse_authors(self, response, **kwargs):
        author_name = response.css(".author-title::text").get().strip()
        birth_date = response.css(".author-born-date::text").get()
        birth_place = response.css(".author-born-location::text").get().strip("in ")
        description = response.css(".author-description::text").get().strip()

        yield {
            "author_name": author_name,
            "birth_date": birth_date,
            "birth_place": birth_place,
            "description": description,
        }
