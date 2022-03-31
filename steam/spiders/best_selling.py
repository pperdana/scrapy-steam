from re import S
import scrapy
from ..items import SteamItem


class BestSellingSpider(scrapy.Spider):
    name = 'best_selling'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers']

    def get_platform(self, raw_platform):
        platform = [item.split(' ')[-1] for item in raw_platform]
        return platform

    def remove_tag(self, rate):
        try:
            game_rate = rate.replace('<br>', ' ')
        except:
            pass
        else:
            return game_rate

    def get_ori_price(self, raw_tag):
        raw_class = raw_tag.xpath('.//@class').get()
        original_price = ''
        if 'discounted' in raw_class:
            original_price = raw_tag.xpath(
                'normalize-space(.//span/strike/text())').get()
        else:
            original_price = raw_tag.xpath('normalize-space(.//text())').get()
        return original_price

    def get_discount_price(self, raw_tag):
        raw_class = raw_tag.xpath('.//@class').get()
        discount_price = ''
        if 'discounted' in raw_class:
            discount_price = raw_tag.xpath('.//text()').getall()[-1]
        return discount_price

    def get_discount_rate(self, raw_tag):
        raw_class = raw_tag.xpath('.//div[2]/@class').get()
        if 'discounted' in raw_class:
            rate = raw_tag.xpath('.//div[1]/span/text()').get().strip('-')
            return rate

    def parse(self, response):
        steam_item = SteamItem()
        games = response.xpath('//div[@id="search_result_container"]/div/a')
        for game in games:
            steam_item['game_url'] = game.xpath('.//@href').get()
            steam_item['img_url'] = game.xpath(
                './/div[contains(@class, "search_capsule")]/img/@src').get()
            steam_item['game_name'] = game.xpath(
                './/div[contains(@class, "search_name")]/span/text()').get()
            steam_item['release_date'] = game.xpath(
                './/div[contains(@class, "search_released")]/text()').get()
            steam_item['platform'] = self.get_platform(game.xpath(
                './/span[contains(@class, "platform_img" ) or text()="VR Supported"]/@class').getall())
            steam_item['rating'] = self.remove_tag(game.xpath(
                './/div[contains(@class, "search_reviewscore")]/span/@data-tooltip-html').get())
            steam_item['original_price'] = self.get_ori_price(game.xpath(
                './/div[contains(@class, "search_price_discount_combined")]/div[2]'))
            steam_item['discouted_price'] = self.get_discount_price(game.xpath(
                './/div[contains(@class, "search_price_discount_combined")]/div[2]'))
            steam_item['discouted_rate'] = self.get_discount_rate(game.xpath(
                './/div[contains(@class, "search_price_discount_combined")]'))

            yield steam_item

        next_page = response.xpath(
            '//a[@class="pagebtn" and text()=">"]/@href').get()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse
            )
