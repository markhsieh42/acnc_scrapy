import scrapy
from scrapy.crawler import CrawlerProcess

class AcncSpider(scrapy.Spider):
  name = "acnc_menu"
  allowed_domains = ["acnc.gov.au"]
  start_urls = ['https://www.acnc.gov.au/charity?items_per_page=60&name_abn%5B0%5D=surf%20club&facet__select__field_beneficiaries=0&facet__select__field_countries=0&facet__select__acnc_search_api_sub_history=0&facet__select__field_status=0']

  def parse(self, response):
    self.log('I just visited: ' + response.url)

    for i in response.css('div.view-content > div > table > tbody > tr.odd'):

        item = {
            'company_name': i.css('td.views-field.views-field-acnc-search-api-title-sort > a::text').extract(),
             
            'status': i.css('td.views-field.views-field-acnc-search-api-status-normalised::text').extract(),
            
            'size': i.css('td.views-field.views-field-field-charity-size.views-align-center::text').extract(),
             
            'suburb/town': i.css('td.views-field.views-field-acnc-search-api-address-locality::text').extract(),
            
            'state': i.css('td.views-field.views-field-acnc-search-api-address-administrative-area::text').extract(),
             
            'ABN': i.css('td.views-field.views-field-acnc-search-api-abn-sort > a::text').extract(),

            'URL': response.urljoin(i.css('td.views-field.views-field-acnc-search-api-title-sort > a::attr(href)').extract_first()),
                   
        }
        yield item
    
    for i in response.css('div.view-content > div > table > tbody > tr.even'):

        item = { 
            'company_name': i.css('td.views-field.views-field-acnc-search-api-title-sort > a::text').extract(),
             
            'status': i.css('td.views-field.views-field-acnc-search-api-status-normalised::text').extract(),
            
            'size': i.css('td.views-field.views-field-field-charity-size.views-align-center::text').extract(),
             
            'suburb/town': i.css('td.views-field.views-field-acnc-search-api-address-locality::text').extract(),
            
            'state': i.css('td.views-field.views-field-acnc-search-api-address-administrative-area::text').extract(),
             
            'ABN': i.css('td.views-field.views-field-acnc-search-api-abn-sort > a::text').extract(),

            'URL': response.urljoin(i.css('td.views-field.views-field-acnc-search-api-title-sort > a::attr(href)').extract_first())
        }
        yield item
    
    # follow pagination link
    next_page_url = response.css('li.next > a::attr(href)').extract_first()
    if next_page_url:
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)



'''
# for each odd terms -- company name, ABN(key to merge dataset)
response.css('tr.odd > td > a::text')[0].extract()               # Name, n from 0 to 29

response.css('tr.odd > td > a::text')[1].extract()               # ABN, n from 0 to 29


# for the rest of the columns (status, size, suburb/town, state)
response.css('tr.odd > td:text')[2+8*0].extract()
.
response.css('tr.odd > td:text')[3+8*0].extract()
.
response.css('tr.odd > td:text')[4+8*0].extract()
.
response.css('tr.odd > td:text')[5+8*0].extract()

'''



'''  # yoyoyo, a NEAT way to write Scrapy !! 
import scrapy
from scrapy.crawler import CrawlerProcess

class AcncSpider(scrapy.Spider):
  name = "acnc_menu2"
  allowed_domains = ["acnc.gov.au"]
  start_urls = ['https://www.acnc.gov.au/charity?items_per_page=60&name_abn%5B0%5D=surf%20club&location%5B0%5D=qld&facet__select__field_beneficiaries=0&facet__select__field_countries=0&facet__select__acnc_search_api_sub_history=0&facet__select__field_status=0']

  def parse(self, response):
    self.log('I just visited: ' + response.url)

    for row in response.css('table.views-table tbody tr'):
        i = {}
    # field specific selectors
        i['company_name'], i['ABN'], i['status'], i['size'], i['suburb/town'], i['state'] = row.css('td')
        for key in i.keys():
            i[key] = i[key].css("*::text").get(default="") 
        yield i
    
    # follow pagination link
    next_page_url = response.css('li.next > a::attr(href)').extract_first()
    if next_page_url:
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)
'''



'''     
    for i in response.css('tr.odd'):
        item = {
            'company_name': i.css('td > a::text')[0].extract(),
            'status': i.css('td::text')[2].extract(),
            'size': i.css('td::text')[3].extract(),
            'suburb/town': i.css('td::text')[4].extract(),
            'state': i.css('td::text')[5].extract(),
        }
        yield item
''' 



'''
    for i in response.css('tr.even'):
        item = {
            'company_name': i.css('td > a::text')[0].extract(),
            'status': i.css('td::text')[2].extract(),
            'size': i.css('td::text')[3].extract(),
            'suburb/town': i.css('td::text')[4].extract(),
            'state': i.css('td::text')[5].extract(),
        }
        yield item
'''  