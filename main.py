import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes.json"}
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            if quote.xpath("span/small/text()").get() == "Steve Martin"\
            or quote.xpath("span/small/text()").get() == "Albert Einstein":
                q = quote.xpath("span[@class='text']/text()").get()[1:-1]
                yield {
                    "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small/text()").get(),
                    "quote": q
                }


class AuthorsSpider(scrapy.Spider):
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    authors = ["Albert-Einstein/", "Steve-Martin/"]

    def parse(self, response):
        for author in response.xpath("/html//div[@class='author-details']"):
                yield {
                    "fullname": author.xpath("h3[@class='author-title']/text()").get().split("\n")[0],
                    "born_date": author.xpath("p/span[@class='author-born-date']/text()").get(),
                    "born_location": author.xpath("p/span[@class='author-born-location']/text()").get(),
                    "description": author.xpath("div[@class='author-description']/text()").get().split("\n")[1].strip()
                }

        for n in range(0, len(self.authors)):
            url = f"{self.start_urls[0]}author/{self.authors[n]}"
            yield scrapy.Request(url=url)

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.crawl(AuthorsSpider)
process.start()