import scrapy
from scrapy.crawler import CrawlerProcess

class AcncSpider(scrapy.Spider):
  name = "acnc_menu_detail"
  allowed_domains = ["acnc.gov.au"]
  start_urls = ['https://www.acnc.gov.au/charity?items_per_page=60&name_abn%5B0%5D=surf%20club&facet__select__field_beneficiaries=0&facet__select__field_countries=0&facet__select__acnc_search_api_sub_history=0&facet__select__field_status=0']

  def parse(self, response): 
    urls_odd = response.css('tr.odd > td > a::attr(href)').extract()
    for url in urls_odd:
        url = response.urljoin(url)
        yield scrapy.Request(url=url, callback = self.parse_details)


    urls_even = response.css('tr.even > td > a::attr(href)').extract()
    for url in urls_even:
        url = response.urljoin(url)
        yield scrapy.Request(url=url, callback = self.parse_details)


    # follow pagination link
    next_page_url = response.css('li.next > a::attr(href)').extract_first()
    if next_page_url:
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

  def parse_details(self, response):
      yield {
        'Name': response.css('h1.page-header::text').extract()[0],
        'ABN': response.css('div.field.field-name-field-abn.field-type-text.field-label-inline.clearfix > div.field-items > div > a::text').extract(),
        'Address_streetblock': response.css('div.field.field-name-field-address.field-type-addressfield.field-label-inline.clearfix > div.field-items > div > div.street-block > div::text').extract(),
        'Address_locality': response.css('div.field.field-name-field-address.field-type-addressfield.field-label-inline.clearfix > div.field-items > div > div.addressfield-container-inline.locality-block.country-AU > span.locality::text').extract(),
        'postcode': response.css('div.field.field-name-field-address.field-type-addressfield.field-label-inline.clearfix > div.field-items > div > div.addressfield-container-inline.locality-block.country-AU > span.postal-code::text').extract(),
        'Email': response.css('div.field.field-name-field-email.field-type-text.field-label-inline.clearfix > div.field-items > div > a::text').extract(),
        'Address For Service email': response.css('div.field.field-name-field-afs-email.field-type-text.field-label-inline.clearfix > div.field-items > div > a::text').extract(),
        'Charity Size': response.css('div.field.field-name-field-charity-size.field-type-text.field-label-inline.clearfix > div.field-items > div::text').extract(),
        'Who the charity helps':response.css('div.field.field-name-field-beneficiaries.field-type-taxonomy-term-reference.field-label-inline.clearfix > div.field-items > div::text').extract(),
        'Date established': response.css('div.field.field-name-field-date-established.field-type-datetime.field-label-inline.clearfix > div.field-items > div > span::text').extract(),
        'Last reported': response.css('div.field.field-name-field-last-reported.field-type-datetime.field-label-inline.clearfix > div.field-items > div > span::text').extract(),
        'Next report due': response.css('div.field.field-name-field-next-report-due.field-type-datetime.field-label-inline.clearfix > div.field-items > div > span::text').extract(),
        'Financial Year End': response.css('div.field.field-name-field-financial-year-end.field-type-text.field-label-inline.clearfix > div.field-items > div::text').extract(),
        'States': response.css('div.field.field-name-field-operating-in.field-type-taxonomy-term-reference.field-label-inline.clearfix > div.field-items > div::text').extract(),
        
        # financial overview -- incomes; TGI: total gross income
        'Total_Income': response.css('div > div > div > p:nth-child(3)::text').extract(),
        'TGI_Government Grants': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[0],
        'TGI_Donations_and_Bequests': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[2],
        'TGI_Goods_or_Services': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[3],
        'TGI_Income_Investments': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[4],
        'TGI_Other Revenues': response.css('div::attr(data-numbers)')[0].extract().strip().split(',')[1],

        # financial overview -- expenses
        'Total_Expense': response.css('div > div > div > p:nth-child(6)::text').extract(),
        'TE_Grants_and_Donations_in_Australia': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[0],
        'TE_Grants_Donations_Outside_of_Australia': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[1],
        'TE_Interest': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[2],
        'TE_Employees': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[4],
        'TE_Other': response.css('div::attr(data-numbers)')[1].extract().strip().split(',')[3]
      }