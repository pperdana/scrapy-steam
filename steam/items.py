# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamItem(scrapy.Item):
    game_url = scrapy.Field()
    img_url = scrapy.Field()
    game_name = scrapy.Field()
    release_date = scrapy.Field()
    platform = scrapy.Field()
    rating = scrapy.Field()
    original_price = scrapy.Field()
    discouted_price = scrapy.Field()
    discouted_rate = scrapy.Field()
