import scrapy
from scrapy.crawler import CrawlerProcess

class AcncSpider(scrapy.Spider):
  name = "acnc"
  allowed_domains = ["acnc.gov.au"]
  start_urls = ['https://www.acnc.gov.au/charity/d1b13eeb1423b79d003ac01b19e92db4']

  def parse(self, response):
    self.log('I just visited: ' + response.url)
    item = {
        'Name': response.css('h1.page-header::text').extract()[0],
        'ABN': response.css('div.field-items > div > a::text')[0].extract(),
        'Address_streetblock': response.css('div.thoroughfare::text')[0].extract(),
        'Address_locality': response.css('span.locality::text')[0].extract(),
        'postcode': response.css('span.postal-code::text')[0].extract(),
        'Email': response.css('div.field-items > div > a::text')[1].extract(),
        'Address For Service email': response.css('div.field-items > div > a::text')[2].extract(),
        'Charity Size': response.css('div.field-items > div::text')[2].extract(),
        'Who the charity helps':response.css('div.field-items > div::text')[3].extract(),
        'Last reported': response.css('span.date-display-single::text')[0].extract(),
        'Next report due': response.css('span.date-display-single::text')[1].extract(),
        'Financial Year End': response.css('div.field-items > div::text')[4].extract(),
        'States': response.css('div.field-items > div::text')[7].extract(),
        # financial overview -- incomes; TGI: total gross income
        'Total_Income': response.css('p::text')[12].extract(),
        'TGI_Government Grants': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[0],
        'TGI_Donations_and_Bequests': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[2],
        'TGI_Goods_or_Services': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[3],
        'TGI_Income_Investments': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[4],
        'TGI_Other Revenues': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[1],
        # financial overview -- expenses
        'Total_Expense': response.css('p::text')[13].extract(),
        'TE_Grants_and_Donations_in_Australia': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[0],
        'TE_Grants_Donations_Outside_of_Australia': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[1],
        'TE_Interest': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[2],
        'TE_Employees': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[4],
        'TE_Other': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[3]

    }
    yield item
    # follow pagination link




'''
# What just happened under the hood?
# Scrapy schedules the scrapy.Request objects returned by the start_requests method of the Spider. Upon receiving a response for each one, 
# it instantiates Response objects and calls the callback method associated with the request (in this case, the parse method) passing the 
# response as argument.

'''

# To read the file as .csv:
# scrapy crawl <your spider name> -o file.csv -t csv

# charity details items
# response.css('div.field-label::text').extract()

# charity details values
# response.css('div.field-items > div > a::text')[0].extract()

# Next page
# abnlink_url = response.css('div.field-items > div > a::attr(href)')[0].extract()
# response.urljoin(abnlink_url)

# total income
# response.css('p > strong::text')[1].extract()

# value of totoal income
# response.css('p::text')[12].extract()

