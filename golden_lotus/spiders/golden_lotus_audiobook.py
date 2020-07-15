import scrapy
import re


def _is_main_content(text):
    return re.match(r'第\d+', text) or re.match(r'金瓶\d+集', text)


def _is_comment_content(text):
    return re.match(r'第\d+', text) or re.match(r'金瓶\d+集', text)


class GoldenLotusAudiobookSpider(scrapy.Spider):
    name = 'golden_lotus_audiobook'
    allowed_domains = ['mp.weixin.qq.com']
    start_urls = ['https://mp.weixin.qq.com/s/eg5kO7Ee3AG6VgsMzKS4ow']

    def parse(self, response):
        for a in response.xpath('//div[@id="js_content"]//a'):
            text = a.xpath('string()').get().strip()
            if _is_main_content(text) or _is_comment_content(text):
                yield response.follow(a, callback=self.parse_content_page, cb_kwargs=dict(title=text), )

    def parse_content_page(self, response, title):
        mpvoice = response.xpath('//mpvoice')
        yield {
            'title': title,
            'filename': mpvoice.attrib['name'],
            'play_length': mpvoice.attrib['play_length'],
            'file_urls': 'https://res.wx.qq.com/voice/getvoice?mediaid=' + mpvoice.attrib['voice_encode_fileid']
        }
