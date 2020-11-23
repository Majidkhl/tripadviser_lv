import scrapy
from urllib.parse import urljoin
import logging


class LasvegasSpider(scrapy.Spider):
    name = 'lasvegas'
    #allowed_domains = ['www.tripadvisor.fr']
    start_urls = ['https://www.tripadvisor.fr/Hotels-g45963-Las_Vegas_Nevada-Hotels.html']

    def parse(self, response):
        all_hotels = response.xpath('//div[@data-prwidget-name="meta_hsx_responsive_listing"]')
        hotel_names = all_hotels.xpath('//a[@class="property_title prominent "]')
        hotel_price = response.xpath('//div[@class="price-wrap "]/div[@class="price __resizeWatch"]')

        for hotel in hotel_names:
            name = hotel.xpath('.//text()').get()
            link = hotel.xpath('.//@href').get()
            absolute_link = response.urljoin(link)
            #price = hotel_price('.//text()').get()


            yield{
                'hotel_name': name,
                'hotel_link': absolute_link
                #'hotel_price': price
                }

            yield response.follow(url=absolute_link, callback=self.parse_comment, meta={'hotel_name': name})

    def parse_comment(self, response):
        logging.info(response.url)
        comment = response.xpath('//q[@class="IRsGHoPm"]')
        name = response.request.meta['hotel_name']
        for commentaire in comment:
            webcomment = commentaire.xpath('.//span/text()').get()

            # yield {
            #     'hotel_nmae': name,
            #     'webcomment': webcomment,
            #     }







