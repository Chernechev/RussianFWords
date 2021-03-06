import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

import time
start_time = time.time()

path = 'test.csv'
data = pd.read_csv(path, index_col='Unnamed: 0')

#Использовать точные формы или леммы?
word_list = data['word']

class FirstSpider(scrapy.Spider):
    name = 'ruscorpora'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'DOWNLOAD_DELAY' : 2}
    
    def start_requests(self):
        yield scrapy.Request('https://ruscorpora.ru/new/search-main.html', callback=self.form_input)
    
    def form_input(self, response):
        words = word_list
            
        for the_word in words:
            
            yield scrapy.FormRequest.from_response(response, formdata={'req': the_word}, callback=self.parse_freq)
    
    def parse_freq(self, response):
        rel_xpath = "/html/body/div[4]/p[3]/span[3]/text()"
        all_xpath = "/html/body/div[4]/p[1]/span[3]/text()"
        rel_freq = response.xpath(rel_xpath).extract_first()
        all_freq = response.xpath(all_xpath).extract_first()
        
        if rel_freq is not None:
            rel_freq = rel_freq.replace(' ', '')
            all_freq = all_freq.replace(' ', '')
            number = (float(rel_freq) / float(all_freq))*1000000
            frequency.append(number)
        else:
            frequency.append(0)
            
frequency = []


crawler = CrawlerProcess()
crawler.crawl(FirstSpider)
crawler.start()

print(f"freq of shape: {len(frequency)}\ndata of shape: {data.shape}")

frequency = [float("{:.3f}".format(x)) for x in frequency]
data['freq'] = frequency
data.to_csv(path)

print("--- %s seconds ---" % (time.time() - start_time))