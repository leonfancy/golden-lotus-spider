import scrapy


class GoldenLotusAudiobookSpider(scrapy.Spider):
    name = 'golden_lotus_audiobook'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = ['https://mp.weixin.qq.com/s/eg5kO7Ee3AG6VgsMzKS4ow']

    def parse(self, response):
        for a in response.xpath('//div[@id="js_content"]/p//a'):
            yield {
                'title': a.xpath('string()').get().strip()
            }
