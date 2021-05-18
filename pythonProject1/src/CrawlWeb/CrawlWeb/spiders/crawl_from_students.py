import scrapy



class Crawling(scrapy.Spider):
    name = "get_students"
    start_urls = ["http://112.137.129.87/qldt/?SinhvienLmh%5Bterm_id%5D=030&ajax=sinhvien-lmh-grid&pageSize=5000"]

    def parse(self, response):
        for line in response.xpath("//table[@class='items']/tbody/tr"):
            yield {
                "order": line.xpath(".//td[1]/text()").extract_first(),
                "student_id": line.xpath(".//td[2]/text()").extract_first(),
                "student_name":line.xpath(".//td[3]/text()").extract_first(),
                "DOB": line.xpath(".//td[4]/text()").extract_first(),
                "class_name": line.xpath(".//td[5]/text()").extract_first(),
                "class_id": line.xpath(".//td[6]/text()").extract_first(),
                "subject_name": line.xpath(".//td[7]/text()").extract_first(),
                "group": line.xpath(".//td[8]/text()").extract_first(),
                "credit": line.xpath(".//td[9]/text()").extract_first(),
                "type": line.xpath(".//td[10]/text()").extract_first()
            }
        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(next_page_link, self.parse)